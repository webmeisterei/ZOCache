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

from ZODB.utils import u64


z64 = '\0' * 8


class BasicCacheDriverTests(object):
    """Assumes theres a self._storage object"""

    def checkA_DriverStoreAndLoad(self):
        int_oid = u64(self._storage.new_oid())
        data = 'Hello World!'
        self.assertEqual(
            True,
            self._storage.driver.store(int_oid, z64, data)
        )
        self.assertEqual(
            z64,
            self._storage.driver.load(int_oid)[1]
        )
        self.assertEqual(
            data,
            self._storage.driver.load(int_oid)[0]
        )
