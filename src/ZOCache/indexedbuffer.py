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

import tempfile
import threading


class IndexedBuffer(object):
    """ A somewhat intelligent buffer
    it knows where data is stored and howto retreive that.

    This class is thread save.
    """

    def __init__(self, bufsize=10*1024*1024):
        self._bufsize = bufsize
        self._f = tempfile.TemporaryFile(bufsize=self._bufsize)
        self._index = []
        self._map = {}
        self._lock = threading.Lock()
        self._transaction = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        with self._lock:
            self._f.close()
            self._f = None
            self._index = []
            self._map = {}
            self._transaction = None
            self._tid = None

    def store(self, int_oid, data):
        with self._lock:
            self._index.append((int_oid, self._f.tell(), len(data),))
            self._map[int_oid] = len(self._index) - 1
            self._f.write(bytes(data))

    def load(self, int_oid):
        with self._lock:
            if int_oid not in self._map:
                return None

            pos = self._f.tell()
            _, start, length = self._index[self._map[int_oid]]
            self._f.seek(start)
            data = self._f.read(length)
            self._f.seek(pos)

            return str(data)

    def reset(self):
        self.close()
        with self._lock:
            self._f = tempfile.TemporaryFile(bufsize=self._bufsize)

    def dump_and_reset(self):
        """ Returns an iterator that yields "(int_oid, data,)"
        and resets the buffer after.
        """

        with self._lock:
            self._f.seek(0)

            for int_oid, _, length in self._index:
                data = self._f.read(length)
                if len(data) < length:
                    raise EOFError('Got not enough data from file.')
                yield int_oid, str(data)

        self.reset()

    @property
    def transaction(self):
        return self._transaction

    @transaction.setter
    def transaction(self, value):
        self._transaction = value
