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
from zope.interface import implementer
from ..interfaces import IZOCacheDriver
from ..registry import Registry
from ..notavailable import notAvailable
from ..url import URL


@implementer(IZOCacheDriver)
class MockCacheDriver(object):
    name = 'mock'

    def __init__(self, url):
        self._url = URL.from_string(url)

        self._cache = {}

        self._lock = threading.Lock()

    @property
    def url(self):
        return self._url

    @classmethod
    def available(cls):
        return (True, '',)

    def close(self):
        pass

    def load(self, int_oid):
        with self._lock:
            key = int_oid
            if key not in self._cache:
                return notAvailable

            return self._cache[key]

    def store(self, int_oid, b_prev_tid, data):
        with self._lock:
            key = int_oid
            self._cache[key] = data


Registry.register(MockCacheDriver)
