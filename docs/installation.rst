Installation
============

Dependencies
------------

Python Redmine relies heavily on great `Requests <http://docs.python-requests.org>`_
library by Kenneth Reitz for all the http(s) calls.

PyPI
----

The recommended way to install is from Python Package Index (PyPI) with `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

    $ pip install python-redmine

or with `easy_install <https://pypi.python.org/pypi/setuptools>`_:

.. code-block:: bash

    $ easy_install python-redmine

If the PyPI is down, you can also install Python Redmine from one of it's mirrors, e.g. from
`Crate.IO <http://crate.io>`_:

.. code-block:: bash

    $ pip install -i http://simple.crate.io/ python-redmine

GitHub
------

Python Redmine is actively developed on `GitHub <https://github.com/maxtepkeev/python-redmine>`_.
If you want to get latest development sources you have to clone the repository:

.. code-block:: bash

    $ git clone git://github.com/maxtepkeev/python-redmine.git

Once you have the sources, you can install it into your site-packages:

.. code-block:: bash

    $ python setup.py install
