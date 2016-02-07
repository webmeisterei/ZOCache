# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) Zope Foundation and Contributors.
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
from zope.testing import setupstack

import ZOCache
import doctest
import transaction
import unittest
import ZEO.tests.testZEO
import ZODB.config
import ZODB.FileStorage
import ZODB.interfaces
import ZODB.MappingStorage
import ZODB.tests.StorageTestBase
import ZODB.tests.testFileStorage
import ZODB.utils
import zope.interface.verify
from . import mockcachedriver


# For PEP8 checks
_ = transaction
_ = zope.interface.verify
_ = mockcachedriver


def test_config():
    r"""

To configure a ZOCache, import ZOCache and use the
zocachestorage tag:

    >>> config = '''
    ...     %import ZOCache
    ...     <zodb>
    ...         <zocachestorage>
    ...             <filestorage>
    ...                 path data.fs
    ...                 blob-dir blobs
    ...             </filestorage>
    ...             url mock://user:password@localhost:1313/db
    ...         </zocachestorage>
    ...     </zodb>
    ... '''
    >>> db = ZODB.config.databaseFromString(config)

    >>> conn = db.open()
    >>> conn.root()['a'] = 1
    >>> transaction.commit()
    >>> conn.root()['b'] = ZODB.blob.Blob('Hi\nworld.\n')
    >>> transaction.commit()

    >>> db.close()

    >>> db = ZODB.config.databaseFromString(config)
    >>> conn = db.open()
    >>> conn.root()['a']
    1
    >>> conn.root()['b'].open().read()
    'Hi\nworld.\n'
    >>> db.close()
    """


class Dummy:

    def invalidateCache(self):
        print 'invalidateCache called'

    def invalidate(self, *args):
        print 'invalidate', args

    def references(self, record, oids=None):
        if oids is None:
            oids = []
        oids.extend(record.decode('hex').split())
        return oids

    def transform_record_data(self, data):
        return data.encode('hex')

    def untransform_record_data(self, data):
        return data.decode('hex')


def test_wrapping():
    r"""
Make sure the wrapping methods do what's expected.

    >>> s = ZOCache.ZOCacheStorage(
    ...     ZODB.MappingStorage.MappingStorage(),
    ...     "mock://user:password@localhost:1313/db"
    ... )
    >>> zope.interface.verify.verifyObject(ZODB.interfaces.IStorageWrapper, s)
    True

    >>> s.registerDB(Dummy())
    >>> s.invalidateCache()
    invalidateCache called

    >>> s.invalidate('1', range(3), '')
    invalidate ('1', [0, 1, 2], '')

    >>> data = ' '.join(map(str, range(9)))
    >>> transformed = s.transform_record_data(data)
    >>> transformed
    '3020312032203320342035203620372038'

    >>> s.untransform_record_data(transformed) == data
    True

    >>> s.references(transformed)
    ['0', '1', '2', '3', '4', '5', '6', '7', '8']

    >>> l = range(3)
    >>> s.references(transformed, l)
    [0, 1, 2, '0', '1', '2', '3', '4', '5', '6', '7', '8']

    >>> l
    [0, 1, 2, '0', '1', '2', '3', '4', '5', '6', '7', '8']

    """


class FileStorageZOCacheTests(ZODB.tests.testFileStorage.FileStorageTests):

    def open(self, **kwargs):
        self._storage = ZOCache.ZOCacheStorage(
            ZODB.FileStorage.FileStorage('FileStorageTests.fs', **kwargs),
            "mock://user:password@localhost:1313/db"
        )


class FileStorageZOCacheTestsWithBlobsEnabled(
        ZODB.tests.testFileStorage.FileStorageTests):

    def open(self, **kwargs):
        if 'blob_dir' not in kwargs:
            kwargs = kwargs.copy()
            kwargs['blob_dir'] = 'blobs'
        ZODB.tests.testFileStorage.FileStorageTests.open(self, **kwargs)
        self._storage = ZOCache.ZOCacheStorage(
            self._storage,
            "mock://user:password@localhost:1313/db"
        )


class FileStorageZOCacheRecoveryTest(
        ZODB.tests.testFileStorage.FileStorageRecoveryTest):

    def setUp(self):
        ZODB.tests.StorageTestBase.StorageTestBase.setUp(self)

        self._storage = ZOCache.ZOCacheStorage(
            ZODB.FileStorage.FileStorage("Source.fs", create=True),
            "mock://user:password@localhost:1313/db"
        )

        self._dst = ZOCache.ZOCacheStorage(
            ZODB.FileStorage.FileStorage("Dest.fs", create=True),
            "mock://user:password@localhost:1313/db"
        )


class FileStorageZEOZOCacheTests(ZEO.tests.testZEO.FileStorageTests):
    _expected_interfaces = (
        ('ZODB.interfaces', 'IStorageRestoreable'),
        ('ZODB.interfaces', 'IStorageIteration'),
        ('ZODB.interfaces', 'IStorageUndoable'),
        ('ZODB.interfaces', 'IStorageCurrentRecordIteration'),
        ('ZODB.interfaces', 'IExternalGC'),
        ('ZODB.interfaces', 'IStorage'),
        ('zope.interface', 'Interface'),
        )

    def _wrap_client(self, client):
        return ZOCache.ZOCacheStorage(
            client,
            "mock://user:password@localhost:1313/db"
        )


def test_suite():
    suite = unittest.TestSuite()
    for class_ in (FileStorageZOCacheTests,
                   FileStorageZOCacheTestsWithBlobsEnabled,
                   FileStorageZOCacheRecoveryTest,
                   FileStorageZEOZOCacheTests):

        s = unittest.makeSuite(class_, "check")
        s.layer = ZODB.tests.util.MininalTestLayer(
            'mock_zocachestoragetests.%s' % class_.__name__)
        suite.addTest(s)

    suite.addTest(doctest.DocTestSuite(
        setUp=setupstack.setUpDirectory, tearDown=setupstack.tearDown
        ))
    return suite
