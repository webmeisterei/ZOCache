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
from ..notavailable import notAvailable
from ..url import URL

from threading import local

try:
    from pymemcache.client.base import Client
    MEMCACHED_AVAILABLE = True
except ImportError:
    MEMCACHED_AVAILABLE = False


@implementer(IZOCacheDriver)
class MemcachedCacheDriver(object):
    """ memcached cache driver for ZOCache

    The url should look like:

        memcached://<hostname>:<port>/<key_prefix>?timeout=10&validate=true&debug=true
    """

    name = 'memcached'

    def __init__(self, url):
        self._url = URL.from_string(url)
        self._local = local()

    @property
    def url(self):
        return self._url

    @classmethod
    def available(cls):
        if not MEMCACHED_AVAILABLE:
            return (False, 'Please install the \"pymemcache\" python module.',)

        return (True, '\"pymemcache\" available',)

    @property
    def _client(self):
        client = getattr(self._local, 'client', None)
        if client:
            return client

        url = self.url

        timeout = 10  # TODO: Good default?
        if 'timeout' in url.query:
            timeout = float(url.query['timeout'])

        key_prefix = 'zc'
        if url.database:
            key_prefix = url.database

        ignore_exc = False
        if ('ignore_exc' in url.query and
                url.query['ignore_exc'].lower() == 'true'):
            ignore_exc = True

        self._validate = False
        if ('validate' in url.query and
                url.query['validate'].lower() == 'true'):
            self._validate = True

        self._debug = False
        if ('debug' in url.query and
                url.query['debug'].lower() == 'true'):
            self._debug = True

        client = Client(
            (url.host, url.port,),
            timeout=timeout,
            ignore_exc=ignore_exc,
            default_noreply=False,
            key_prefix=key_prefix
        )
        self._local.client = client
        return client

    def close(self):
        return

    def load(self, int_oid):
        result = self._client.get(str(int_oid))
        if result is None:
            if self._debug:
                print('load: %d notAvailable' % int_oid)
            return notAvailable

        if self._debug:
            print('load: %d %r %r' % (
                int_oid,
                result[:8],
                result[8:])
            )

        return str(result[8:]), str(result[:8])

    def store(self, int_oid, b_prev_tid, data, _debug_stored_by=''):
        client = self._client

        if not data:
            if self._debug:
                print('nosto: %d %r %r %r' % (
                    int_oid,
                    b_prev_tid + ' ' * (30 - len(str(b_prev_tid))),
                    _debug_stored_by,
                    data)
                )
            return

        if self._debug:
            print('store: %d %r %r %r' % (
                int_oid,
                b_prev_tid + ' ' * (30 - len(str(b_prev_tid))),
                _debug_stored_by,
                data)
            )

        return True

        result = client.set(
            bytes(int_oid),
            bytes(b_prev_tid) + bytes(data)
        )

        if self._validate:
            s_data, s_tid = self.load(int_oid)
            assert data == s_data
            assert s_tid == b_prev_tid

        return result


Registry.register(MemcachedCacheDriver)
