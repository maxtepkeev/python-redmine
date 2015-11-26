Installation
============

Dependencies
------------

Python Redmine relies heavily on great `Requests <http://docs.python-requests.org>`_ library by Kenneth Reitz
for all the http(s) calls. To provide better user experience, Python-Redmine vendors Requests (i.e. embeds it
inside itself) and uses a so-called "smart imports" strategy to identify whether it should use the vendored
version or the global one. It works like this, at the first import time Python-Redmine checks if there is a
global Requests installed and if it's version is greater than the vendored Requests, Python-Redmine will use
global Requests and if not, the vendored one. This strategy provides you with the following benefits:

* no external dependencies are installed together with Python-Redmine
* no more conflicts with other libraries that depend on other version of Requests
* always the latest version of Requests available at the release time of Python-Redmine
* use newer versions of Requests in case of the immediate upgrade need absolutely automatically

Conflicts
---------

Python Redmine can't be used together with `PyRedmine <https://pypi.python.org/pypi/pyredmine>`_
because they both use same module name, i.e. ``redmine`` which causes unexpected behaviour for
both packages. That means that you have to uninstall PyRedmine before installing Python Redmine.

PyPI
----

The recommended way to install is from Python Package Index (PyPI) with `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

    $ pip install python-redmine

or with `easy_install <https://pypi.python.org/pypi/setuptools>`_:

.. code-block:: bash

    $ easy_install python-redmine

GitHub
------

Python Redmine is actively developed on `GitHub <https://github.com/maxtepkeev/python-redmine>`_.
If you want to get latest development sources you have to clone the repository:

.. code-block:: bash

    $ git clone git://github.com/maxtepkeev/python-redmine.git

Once you have the sources, you can install it into your site-packages:

.. code-block:: bash

    $ python setup.py install

You can also install latest stable development version via `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

    $ pip install git+https://github.com/maxtepkeev/python-redmine.git@master
