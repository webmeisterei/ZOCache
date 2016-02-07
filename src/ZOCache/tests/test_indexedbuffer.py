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

import random
import unittest
import ZODB.tests.util
from ..indexedbuffer import IndexedBuffer


class TestIndexedBuffer(unittest.TestCase):

    _test_data = [
        '0 Hello',
        '1 World',
        '2 ((U\x10ZODB.tests.MinPOq\x01U\x05MinPOq\x02tq\x03Nt.}q\x04U\x05valueq\x05(U\x08Thread-2q\x06K\x08tq\x07s.',  # noqa
        '3 ((U\x10ZODB.tests.MinPOq\x01U\x05MinPOq\x02tq\x03Nt.}q\x04U\x05valueq\x05(U\x08Thread-2q\x06K\ttq\x07s.',  # noqa
        '4 ((U\x10ZODB.tests.MinPOq\x01U\x05MinPOq\x02tq\x03Nt.}q\x04U\x05valueq\x05(U\x08Thread-2q\x06K\x01tq\x07s.',  # noqa
        '5 ((U\x10ZODB.tests.MinPOq\x01U\x05MinPOq\x02tq\x03Nt.}q\x04U\x05valueq\x05(U\x08Thread-1q\x06K\x04tq\x07s.',  # noqa
        '6 (cpersistent.mapping\nPersistentMapping\nq\x01Nt.}q\x02U\x04dataq\x03}q\x04s.',  # noqa
        '7 Any text',
        '8 Text',
        '9 Text'
    ]

    def setUp(self):
        self._len_testdata = len(self._test_data)

    def check_A_StoreAndDump(self):
        with IndexedBuffer() as ib:
            for i in xrange(1, self._len_testdata):
                ib.store(i, self._test_data[i])

            num_iter = xrange(1, self._len_testdata).__iter__()
            for int_oid, data in ib.dump_and_reset():
                i = num_iter.next()
                self.assertEqual(int_oid, i, "int_oid not equal")
                self.assertEqual(data, self._test_data[i], "data not equal")

    def check_B_SerialLoad(self):
        with IndexedBuffer() as ib:
            for i in xrange(0, self._len_testdata):
                ib.store(i, self._test_data[i])

            for i in xrange(0, self._len_testdata):
                data = ib.load(i)
                self.assertEqual(data, self._test_data[i], "data not equal")

    def check_C_RandomLoad(self):
        with IndexedBuffer() as ib:
            for i in xrange(0, 50):
                ib.store(i, self._test_data[i % self._len_testdata])

            for _ in xrange(1, 100):
                i = random.randint(0, 49)
                data = ib.load(i)
                self.assertEqual(
                    data,
                    self._test_data[i % self._len_testdata],
                    "data not equal"
                )


def test_suite():
    suite = unittest.TestSuite()
    s = unittest.makeSuite(TestIndexedBuffer, "check")
    s.layer = ZODB.tests.util.MininalTestLayer(
        'indexedbuffer.%s' % TestIndexedBuffer.__name__)
    suite.addTest(s)

    return suite
