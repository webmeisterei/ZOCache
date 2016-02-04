===============================================================
Zope Object Cache - Client side redis/memcached cache
===============================================================

Idea and quite a lot of code taken from cipher.encryptingstorage.

The ``ZOCache`` package provides a ZODB storage wrapper
implementation that provides caching of database records.

.. contents::

Usage
=====

The primary storage is ``ZOCache.ZOCacheStorage``.
It is used as a wrapper around a lower-level storage.  From Python, it is
constructed by passing another storage, as in::

    import ZODB.FileStorage
    from ZOCache import ZOCacheStorage
    from ZOCache.tests import MockCacheDriver

    storage = ZOCacheStorage(
        ZODB.FileStorage.FileStorage('data.fs'),
        'mock://user:password@localhost:1313/db'
    )

.. -> src

The above code will give you a ``mock`` driver which would connect to localhost:1313 and the db ``db``
with the user ``user`` and password ``password``.

    >>> exec src
    >>> isinstance(storage.driver, MockCacheDriver)
    True

    >>> storage.driver.url.username
    'user'

    >>> storage.driver.url.password
    'password'

    >>> storage.driver.url.host
    'localhost'

    >>> storage.driver.url.port
    1313

    >>> storage.driver.url.database
    'db'

    >>> storage.close()