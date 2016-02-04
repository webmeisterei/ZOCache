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
from ..driver.mixin import ZOCacheDriverMixin
from ..interfaces import IZOCacheDriver
from ..registry import Registry


@implementer(IZOCacheDriver)
class MockCacheDriver(ZOCacheDriverMixin):
    name = 'mock'

    @classmethod
    def available(cls):
        return (True, '',)

    def close(self):
        pass


Registry.register(MockCacheDriver)
