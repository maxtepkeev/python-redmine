Frequently Asked Questions
==========================

Create/Update/Delete resource operations doesn't work
-----------------------------------------------------

Your Redmine server is probably using ``https`` as the primary protocol and you're trying to connect to it
under ``http`` protocol. Please use the ``https`` protocol and it should work.

The problem described above happens because when you're trying to connect using the ``http`` protocol, your
server issues a redirect to the ``https`` which changes the request method, e.g. if your were trying to
create/update/delete a resource, then ``POST``/``PUT``/``DELETE`` is changing to ``GET`` which expectedly
causes the create/update/delete operations to fail.

The detailed explanation about why this happens is available `here <https://github.com/kennethreitz/requests/
issues/1704>`__.

Can I use python-redmine with ChiliProject fork
-----------------------------------------------

Yes, you can. But keep in mind that ChiliProject is not actively developed and some features in REST API are
missing, not all filters will work, etc. Several problems are described in issues `#37 <https://github.com/
maxtepkeev/python-redmine/issues/37>`_ and `#38 <https://github.com/maxtepkeev/python-redmine/issues/38>`_.
