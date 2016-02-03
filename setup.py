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
"""ZOCache package."""

import os
from setuptools import setup
from setuptools import find_packages

VERSION = "0.0.1.dev0"

# The choices for the Trove Development Status line:
# Development Status :: 5 - Production/Stable
# Development Status :: 4 - Beta
# Development Status :: 3 - Alpha


doclines = __doc__.split("\n")


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

setup(
    name="ZOCache",
    version=VERSION,
    author="Zope Foundation and Contributors",
    maintainer="Rene´ Jochum",
    maintainer_email="rene@webmeisterei.com",
    url="http://github.com/webmeisterei/zeocache",
    license="ZPL 2.1",
    platforms=["any"],
    description=doclines[0],
    classifiers=[
        'Development Status :: 4 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Zope Public License',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: OS Independent'],
    long_description=(
        read("README.rst") + "\n\n" +
        "Changelog\n" +
        "==============\n\n" +
        read("CHANGES.rst")
    ),

    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'ZODB3 >=3.10.5',
        'setuptools',
    ],
    extras_require={
        'redis': [
            'redis'
        ],
        'memcached': [
            'pymemcache'
        ],
        'test': [
            'zope.testing',
            'zope.app.testing',
            'manuel'
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
