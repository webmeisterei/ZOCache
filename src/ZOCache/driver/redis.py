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

from zope.interface import implementer
from ..interfaces import IZOCacheDriver
from ..registry import Registry
from ..url import URL

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


@implementer(IZOCacheDriver)
class RedisCacheDriver(object):
    name = 'redis'

    def __init__(self, url):
        self._url = URL.from_string(url)

    @property
    def url(self):
        return self._url

    @classmethod
    def available(cls):
        if not REDIS_AVAILABLE:
            return (False, 'Please install the \"redis\" python module.',)

        return (True, '',)

    def close(self):
        pass


Registry.register(RedisCacheDriver)
