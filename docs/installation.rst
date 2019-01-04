Installation
============

Dependencies
------------

Python-Redmine relies heavily on great `Requests <http://docs.python-requests.org>`_ library by Kenneth Reitz
for all the http(s) calls. To provide better user experience, Python-Redmine vendors Requests (i.e. embeds it
inside itself) and uses a so-called "smart imports" strategy to identify whether it should use the vendored
version or the global one. It works like this, at the first import time Python-Redmine checks if there is a
global Requests installed and if it's version is greater than the vendored Requests, Python-Redmine will use
global Requests and if not, the vendored one. This strategy provides you with the following benefits:

* no external dependencies are installed together with Python-Redmine
* no more conflicts with other libraries that depend on other version of Requests
* always the latest version of Requests available at the release time of Python-Redmine
* use newer versions of Requests in case of the immediate upgrade need absolutely automatically

.. versionadded:: 2.0.0

If for some reason there is a need to use a global Requests library even if it's version is lower than the
bundled one, one can set a REDMINE_USE_EXTERNAL_REQUESTS environmental variable to force this behaviour.

Standard Edition
----------------

PyPI
++++

The recommended way to install is from Python Package Index (PyPI) with `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

   $ pip install python-redmine

GitHub
++++++

Python-Redmine is actively developed on `GitHub <https://github.com/maxtepkeev/python-redmine>`_.
If you want to get latest development sources you have to clone the repository:

.. code-block:: bash

   $ git clone git://github.com/maxtepkeev/python-redmine.git

Once you have the sources, you can install it into your site-packages:

.. code-block:: bash

   $ python setup.py install

You can also install latest stable development version via `pip <http://www.pip-installer.org>`_:

.. code-block:: bash

   $ pip install git+https://github.com/maxtepkeev/python-redmine.git@master

Pro Edition
-----------

License for a Pro Edition can be bought
`here <https://secure.2checkout.com/order/checkout.php?PRODS=4708754&QTY=1&CART=1&CARD=1&DISABLE_SHORT_FORM_MOBILE=1>`_.
You will receive an email with all the details regarding Pro Edition installation process. In case of any
problems support is provided via support@python-redmine.com. Please be sure to write from email that was
specified during the purchase procedure.
