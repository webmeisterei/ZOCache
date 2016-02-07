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

import zope.interface


class IZOCacheDriver(zope.interface.Interface):
    """ A cache driver stores and loads oid's from the cache.

    WARNING: Cache drivers need to be thread safe.
    """

    name = zope.interface.Attribute('The drivers name.')
    url = zope.interface.Attribute('The drivers connection url.')

    def available():
        """
        :return: Tuple with 2 values,
                 Bool success/error and a success/error message.
        """

    def close():
        """ Closes all connections. """

    def load(int_oid):
        """Load the given object from cache if possible.

        :return: the serialized data or `ZOCache.notAvailable`
        """

    def store(int_oid, b_prev_tid, data):
        """Store the given data as str(oid).

        :return: True on success else False.
        """
