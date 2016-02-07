# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2016 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import threading
from ZODB.utils import u64
from ZODB import POSException

from zope.interface import directlyProvides
from ZODB.interfaces import IStorageWrapper
from zope.interface import implementer
from zope.interface import providedBy

from .registry import Registry
from .url import URL
from util import string_types
from .notavailable import notAvailable
from indexedbuffer import IndexedBuffer


z64 = '\0' * 8


@implementer(IStorageWrapper)
class ZOCacheStorage(object):

    copied_methods = (
        'getName', 'getSize', 'history', 'isReadOnly',
        'lastTransaction', 'new_oid', 'sortKey',
        'temporaryDirectory',
        'supportsUndo', 'undo', 'undoLog', 'undoInfo',
#        'tcp_begin', 'tpc_abort', 'tpc_finish', 'tpc_vote', 'checkCurrentSerialInTransaction',

# For proof of concept.
        'loadBefore', 'loadSerial', 'pack',
        'restore', 'openCommittedBlobFile', 'loadBlob',
        'iterator', 'storeBlob', 'restoreBlob', 'references',
        'copyTransactionsFrom', 'record_iternext', 'deleteObject',
    )

    def __init__(self, base, name_or_url=None, driver=None):
        self._base = base
        self._registry = Registry()

        self._driver = driver
        if self._driver is None:
            if isinstance(name_or_url, string_types):
                url = URL.from_string(name_or_url)
            elif isinstance(name_or_url, URL):
                url = name_or_url
            else:
                raise AttributeError(
                    'Invalid type for name_or_url %r' % name_or_url
                )

            driver_cls = self._registry.drivers.get(url.drivername, None)
            if not driver_cls:
                self._base.close()
                raise KeyError('Unknown driver %r' % url.drivername)

            ok, msg = driver_cls.available()
            if not ok:
                self._base.close()
                raise KeyError(msg)

            self._driver = driver_cls(url)

        # Copy methods and register this storage driver.
        for name in self.copied_methods:
            v = getattr(self._base, name, None)
            if v is not None:
                setattr(self, name, v)

        self._tqueue = IndexedBuffer()
        self._commit_lock = threading.Lock()

        # Provide all interfaces self._base provides.
        directlyProvides(self, providedBy(self._base))

        base.registerDB(self)

#    def __getattr__(self, name):
#        return getattr(self._base, name)

    def __len__(self):
        return len(self._base)

    @property
    def driver(self):
        return self._driver

    def tpc_vote(self, transaction):
        return self._base.tpc_vote(transaction)

    def tpc_begin(self, transaction, tid=None, status=' '):
        result = self._base.tpc_begin(transaction, tid, status)

        self._tqueue.reset()
        self._tqueue.transaction = transaction

        return result

    def tpc_abort(self, transaction):
        result = self._base.tpc_abort(transaction)

        self._tqueue.reset()

        return result

    def tpc_finish(self, transaction, f=None):
        def cache_transaction_data(tid):
            # This happens within the storages transaction commit lock.
            for int_oid, data in self._tqueue.dump_and_reset():
                self.driver.store(
                    int_oid, tid, data,
                    _debug_stored_by="transaction_finish"
                )

            if f is not None:
                f(tid)

        result = self._base.tpc_finish(transaction, cache_transaction_data)

        return result

    def checkCurrentSerialInTransaction(self, oid, serial, transaction):
        return self._base.checkCurrentSerialInTransaction(
            oid,
            serial,
            transaction
        )

    def getTid(self, oid):
        return self._base.getTid(oid)

    def close(self):
        self._base.close()
        self.driver.close()

    def load(self, oid, version=''):
        int_oid = u64(oid)

        # Try to load from the current transaction first.
        if self._tqueue.transaction:
            result = self._tqueue.load(int_oid)
            if result is not None:
                return result, self._tqueue.tid

        # Next try from the cache driver.
        result = self.driver.load(int_oid)
        if result != notAvailable:
            return result[0], result[1]

        # Load from the storage and save into the cache.
        result = self._base.load(oid, version)
        self.driver.store(
            int_oid, result[1], result[0],
            _debug_stored_by="save_after_load"
        )

        return result

    def store(self, oid, oldserial, data, version, transaction):
        if self.isReadOnly():
            raise POSException.ReadOnlyError()
        assert not version

        int_oid = u64(oid)
        prev_tid_int = z64
        if oldserial:
            prev_tid_int = oldserial

        if self._tqueue.transaction:
            self._tqueue.store(int_oid, data)
        else:
            self.driver.store(
                int_oid, prev_tid_int, data,
                _debug_stored_by="no_transaction_store"
            )

        return self._base.store(oid, oldserial, data, version, transaction)

    #
    # IStorageWrapper implementation
    #
    def registerDB(self, db):
        self.db = db
        self._db_transform = db.transform_record_data
        self._db_untransform = db.untransform_record_data

    # This will get called when registerDB hasn't been called.
    _db_transform = _db_untransform = lambda self, data: data

    def invalidateCache(self):
        """ For IStorageWrapper
        """
        return self.db.invalidateCache()

    def invalidate(self, transaction_id, oids, version=''):
        """ For IStorageWrapper
        """
        return self.db.invalidate(transaction_id, oids, version)

    def references(self, record, oids=None):
        """ For IStorageWrapper
        """
        return self.db.references(record, oids)

    def transform_record_data(self, data):
        """ For IStorageWrapper
        """
        return self._db_transform(data)

    def untransform_record_data(self, data):
        """ For IStorageWrapper
        """
        return self._db_untransform(data)

    # END IStorageWrapper implementation

    @property
    def _addr(self):
        """ Hack for tests """
        return self._base._addr

    @property
    def _info(self):
        """ Another hack for tests """
        return self._base._info

    @property
    def _iterator_ids(self):
        """ Another hack for tests """
        return self._base._iterator_ids

    @property
    def _server(self):
        """ Another hack for tests """
        return self._base._server

    @property
    def _server_addr(self):
        """ Another hack for tests """
        return self._base._server_addr

    @property
    def _storage(self):
        """ Another hack for tests """
        return self._base._storage

    def notifyDisconnected(self):
        """ Another hack for tests """
        return self._base.notifyDisconnected()


class ZConfig:

    _factory = ZOCacheStorage

    def __init__(self, config):
        self.config = config
        self.name = config.getSectionName()

    def open(self):
        base = self.config.base.open()
        url = self.config.url

        return self._factory(base, url)
