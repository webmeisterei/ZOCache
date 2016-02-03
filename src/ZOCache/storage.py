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

from zope.interface import directlyProvides
from ZODB.interfaces import IStorageWrapper
from zope.interface import implementer
from zope.interface import providedBy

from .registry import Registry
from .url import URL
from util import string_types


@implementer(IStorageWrapper)
class ZOCacheStorage(object):

    copied_methods = (
        'close', 'getName', 'getSize', 'history', 'isReadOnly',
        'lastTransaction', 'new_oid', 'sortKey',
        'tpc_abort', 'tpc_begin', 'tpc_finish', 'tpc_vote',
        'temporaryDirectory',
        'supportsUndo', 'undo', 'undoLog', 'undoInfo',

# For proof of concept.
        'load', 'loadBefore', 'loadSerial', 'pack',
        'store', 'restore', 'openCommittedBlobFile', 'loadBlob',
        'iterator', 'storeBlob', 'restoreBlob', 'invalidateCache',
        'invalidate', 'references',
        'copyTransactionsFrom'
    )

    def __init__(self, base, name_or_url=None, driver=None):
        self._base = base
        self._registry = Registry()

        if isinstance(name_or_url, string_types):
            self._url = URL.from_string(name_or_url)
        elif isinstance(name_or_url, URL):
            self._url = name_or_url
        else:
            raise ValueError('Invalid type for name_or_url %r' % name_or_url)

        self._driver = driver
        if self._driver is None:
            driver_cls = self._registry.drivers.get(self._url.drivername, None)
            if not driver_cls:
                self._base.close()
                raise KeyError('Unknown driver %r' % self._url.drivername)

            ok, msg = driver_cls.available()
            if not ok:
                self._base.close()
                raise KeyError(msg)

            self._driver = driver_cls(self._url)

        # Copy methods and register this storage driver.
        for name in self.copied_methods:
            v = getattr(self._base, name, None)
            if v is not None:
                setattr(self, name, v)

        directlyProvides(self, providedBy(self._base))

        base.registerDB(self)

    def __getattr__(self, name):
        return getattr(self._base, name)

    def __len__(self):
        return len(self._base)

    def registerDB(self, db):
        self.db = db
        self._db_transform = db.transform_record_data
        self._db_untransform = db.untransform_record_data

    _db_transform = _db_untransform = lambda self, data: data

    def transform_record_data(self, data):
        """ For IStorageWrapper
        """
        return self._transform(self._db_transform(data))

    def untransform_record_data(self, data):
        """ For IStorageWrapper
        """
        return self._db_untransform(self._untransform(data))


class ZConfig:

    _factory = ZOCacheStorage

    def __init__(self, config):
        self.config = config
        self.name = config.getSectionName()

    def open(self):
        base = self.config.base.open()
        url = self.config.url

        return self._factory(base, url)
