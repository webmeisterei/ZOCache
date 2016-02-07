#!/usr/bin/python
from __future__ import print_function
import io
import timeit
import tempfile

from ZOCache.util import text_type
from ZOCache.autotemp import AutoTemporaryFile


class Error(Exception):
    pass


def bench_temporaryfile():
    with tempfile.TemporaryFile(bufsize=10*1024*1024) as out:
        for i in range(0, 100):
            out.write(b"Value = ")
            out.write(bytes(i))
            out.write(b" ")
        # Get string.
        out.seek(0)
        contents = out.read()
        out.close()
        # Test first letter.
        if contents[0:5] != b"Value":
            raise Error


def bench_spooledtemporaryfile():
    with tempfile.SpooledTemporaryFile(max_size=10*1024*1024) as out:
        for i in range(0, 100):
            out.write(b"Value = ")
            out.write(bytes(i))
            out.write(b" ")
        # Get string.
        out.seek(0)
        contents = out.read()
        out.close()
        # Test first letter.
        if contents[0:5] != b"Value":
            raise Error


def bench_autotempfile():
    with AutoTemporaryFile() as out:
        for i in range(0, 100):
            out.write(u"Value = ")
            out.write(text_type(i))
            out.write(u" ")
        # Get string.
        out.seek(0)
        contents = out.read()
        out.close()
        # Test first letter.
        if contents[0] != 'V':
            raise Error


def bench_BufferedRandom():
    # 1. BufferedRandom
    with io.open('out.bin', mode='w+b') as fp:
        with io.BufferedRandom(fp, buffer_size=10*1024*1024) as out:
            for i in range(0, 100):
                out.write(b"Value = ")
                out.write(bytes(i))
                out.write(b" ")
            # Get string.
            out.seek(0)
            contents = out.read()
            # Test first letter.
            if contents[0:5] != b'Value':
                raise Error


def bench_stringIO():
    # 1. Use StringIO.
    out = io.StringIO()
    for i in range(0, 100):
        out.write(u"Value = ")
        out.write(text_type(i))
        out.write(u" ")
    # Get string.
    contents = out.getvalue()
    out.close()
    # Test first letter.
    if contents[0] != 'V':
        raise Error


def bench_concat():
    # 2. Use string appends.
    data = ""
    for i in range(0, 100):
        data += u"Value = "
        data += text_type(i)
        data += u" "
    # Test first letter.
    if data[0] != u'V':
        raise Error


if __name__ == '__main__':
    print(str(timeit.timeit('bench_temporaryfile', setup="from __main__ import bench_temporaryfile", number=1000)) + " TemporaryFile")
    print(str(timeit.timeit('bench_spooledtemporaryfile()', setup="from __main__ import bench_spooledtemporaryfile", number=1000)) + " SpooledTemporaryFile")
    print(str(timeit.timeit('bench_autotempfile()', setup="from __main__ import bench_autotempfile", number=1000)) + " AutoTemporaryFile")
    print(str(timeit.timeit('bench_BufferedRandom()', setup="from __main__ import bench_BufferedRandom", number=1000)) + " BufferedRandom")
    print(str(timeit.timeit("bench_stringIO()", setup="from __main__ import bench_stringIO", number=1000)) + " io.StringIO")
    print(str(timeit.timeit("bench_concat()", setup="from __main__ import bench_concat", number=1000)) + " concat")

# 1454659765.0
# 1454659765.99
# 1454659767.38