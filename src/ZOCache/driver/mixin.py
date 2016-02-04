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
"""  """

from ..url import URL
from ..util import string_types


class ZOCacheDriverMixin(object):

    def __init__(self, name_or_url):
        if isinstance(name_or_url, string_types):
            self._url = URL.from_string(name_or_url)
        elif isinstance(name_or_url, URL):
            self._url = name_or_url
        else:
            raise ValueError(
                'Invalid type for name_or_url %r' % name_or_url
            )

    @property
    def url(self):
        return self._url
