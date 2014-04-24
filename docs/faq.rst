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
