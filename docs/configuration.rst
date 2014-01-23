Configuration
=============

Redmine
-------

To start making requests to Redmine you have to check the box Enable REST API in
Administration -> Settings -> Authentication and click the Save button.

.. hint::

    Sometimes it is a good idea to create a special user in Redmine which will
    be used only for the calls to Redmine's REST API.

Parameters
----------

Configuring Python Redmine is extremely easy, the first thing you have to do is to import
the Redmine object, which will represent the connection to Redmine server:

.. code-block:: python

    from redmine import Redmine

Location
++++++++

Now you need to configure the Redmine object and pass it a few parameters. The only required
parameter is the Redmine location (without the forward slash in the end):

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org')

Authentication
++++++++++++++

Most of the time, the API requires authentication. It can be done in 2 different ways:

* using user's regular login and password:

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org', username='foo', password='bar')

* using user's API key which is a handy way to avoid putting a password in a script:

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org', key='b244397884889a29137643be79c83f1d470c1e2fac')

The API key can be found on users account page when logged in, on the right-hand pane of
the default layout.

Impersonation
+++++++++++++

As of Redmine 2.2.0, you can impersonate user through the REST API. It must be set to a user login,
e.g. jsmith. This only works when using the API with an administrator account, this will be ignored
when using the API with a regular user account.

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org', impersonate='jsmith')

If the login specified does not exist or is not active, you will get an exception.

Version
+++++++

There are a lot of different Redmine versions out there and different versions support different
resources and features. To be sure that everything will work as expected you need to tell Python
Redmine what version of Redmine do you use:

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org', version='2.3.3')

DateTime Formats
++++++++++++++++

Python Redmine automatically converts Redmine's date/datetime strings to Python's date/datetime
objects:

.. code-block:: python

    '2013-12-31T13:27:47Z' -> datetime.datetime(2013, 12, 31, 13, 27, 47)

If the conversion doesn't work for you and you receive strings instead of objects, you have a
different datetime formatting than default. To make the conversion work you have to tell Redmine
object what datetime formatting do you use, e.g. if the string returned is ``31.12.2013T13:27:47Z``:

.. code-block:: python

    redmine = Redmine('http://demo.redmine.org', date_format='%d.%m.%Y', datetime_format='%d.%m.%YT%H:%M:%SZ')

Connection Options
++++++++++++++++++

Python Redmine uses Requests library for all the http(s) calls to Redmine server. Requests provides
sensible default connection options, but sometimes you may have a need to change them. For example
if your Redmine server uses SSL but the certificate is invalid you need to set a Requests's verify
option to False:

.. code-block:: python

    redmine = Redmine('https://redmine.url', requests={'verify': False})

.. hint::

    Storing settings right in the code is a bad habit. Instead store them in some configuration
    file and then import them, for example if you use Django, you can create settings for Python
    Redmine in project's settings.py file and then import them in the code, e.g.:

    .. code-block:: python

        # settings.py
        REDMINE_URL = 'http://demo.redmine.org'
        REDMINE_KEY = 'b244397884889a29137643be79c83f1d470c1e2fac'

        # somewhere in the code
        from django.conf import settings
        from redmine import Redmine

        redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)
