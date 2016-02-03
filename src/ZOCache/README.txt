=============================================================
ZODB storage wrapper for caching of database records
=============================================================

Idea and quite a lot of code taken from cipher.encryptingstorage.

The ``ZOCache`` package provides ZODB storage wrapper
implementations that provides caching of database records.

.. contents::

Usage
=====

The primary storage is ``cipher.encryptingstorage.EncryptingStorage``.
It is used as a wrapper around a lower-level storage.  From Python, it is
constructed by passing another storage, as in::

    import ZODB.FileStorage
    from ZOCache import ZOCacheStorage

    storage = cipher.encryptingstorage.EncryptingStorage(
        ZODB.FileStorage.FileStorage('data.fs'))

.. -> src

    >>> exec src
    >>> data = 'x' * 100
    >>> storage.transform_record_data(data).startswith('.e')
    True
    >>> storage.close()