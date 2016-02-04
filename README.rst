ZOCache
=======

The ``ZOCache - Zope Object Cache`` package provides an ZEO client side central redis/memcached cache for the ZODB.

This project is a WIP.


Authors
=======
- Rene´ Jochum <rene@webmeisterei.com>
- Idea from `@frisi <https://github.com/frisi>`_.
- Lots of code is from `cipher.encryptingstorage <https://github.com/zopefoundation/cipher.encryptingstorage>`_
  which got lots of code from `zc.zlibstorage <https://github.com/zopefoundation/zc.zlibstorage>`_.
- Some code is from `sqlalchemy <http://www.sqlalchemy.org/>`_.
- Caching logic is from `relstorage <https://github.com/zodb/relstorage>`_.


License
=======

ZOCache is distributed under the Zope Public License, an OSI-approved
open source license.  Please see the LICENSE.txt file for terms and
conditions.


Testing for Developers
======================

The ZOCache checkouts are `buildouts <http://www.python.org/pypi/zc.buildout>`_.::

    $ virtualenv -p /usr/bin/python2.7 --no-site-packages .
    $ ./bin/pip install -r requirements.txt

Symlink either ``zodb3.cfg`` or ``zodb4.cfg`` to ``buildout.cfg``::

    $ ln -s zodb4.cfg buildout.cfg

With IPython::

    $ ./bin/buildout -c ipzope.cfg

Or without::

    $ ./bin/buildout

Run the testsuite::

    $ ./bin/test -v1


Contribute
==========

- Issue Tracker: https://github.com/webmeisterei/ZOCache/issues
- Source Code: https://github.com/webmeisterei/ZOCache


Support
=======

If you are having issues, please let us know.
