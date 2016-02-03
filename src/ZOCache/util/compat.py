# util/compat.py
# Copyright (C) 2005-2015 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

"""Handle Python version/platform incompatibilities."""

import sys

try:
    import threading
except ImportError:
    import dummy_threading as threading

py36 = sys.version_info >= (3, 6)
py33 = sys.version_info >= (3, 3)
py32 = sys.version_info >= (3, 2)
py3k = sys.version_info >= (3, 0)
py2k = sys.version_info < (3, 0)
py265 = sys.version_info >= (2, 6, 5)
jython = sys.platform.startswith('java')
pypy = hasattr(sys, 'pypy_version_info')
win32 = sys.platform.startswith('win')
cpython = not pypy and not jython  # TODO: something better for this ?


if py3k:
    from urllib.parse import (parse_qsl, unquote)

    string_types = str,
    binary_type = bytes
    text_type = str
    int_types = int,
    iterbytes = iter

else:
    from urllib import unquote
    from urlparse import parse_qsl

    string_types = basestring,
    binary_type = str
    text_type = unicode
    int_types = int, long
