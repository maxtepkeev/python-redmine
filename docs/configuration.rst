Configuration
=============

Redmine
-------

To start making requests to Redmine you have to check the box Enable REST API in
Administration -> Settings -> Authentication and click the Save button.

.. hint::

   Some operations in Redmine require a user to have the needed permissions to
   perform them, that is why sometimes it is a good idea to create a special user
   with admin rights in Redmine which will be used only for the calls to Redmine
   REST API.

Parameters
----------

Configuring Python-Redmine is extremely easy, the first thing you need to do is to import
the Redmine object, which will represent the connection to the Redmine server:

.. code-block:: python

   from redminelib import Redmine

Location
++++++++

Now you need to configure the Redmine object and pass it a few parameters. The only required
parameter is the Redmine location (without the forward slash in the end):

.. code-block:: python

   redmine = Redmine('https://redmine.url')

Version
+++++++

There are a lot of different Redmine versions out there and different versions support different
resources and features. To be sure that everything will work as expected you need to tell
Python-Redmine what version of Redmine you're using. You can find the Redmine version by visiting
the following address ``https://redmine.url/admin/info`` and taking the first 3 numbers, i.e. if you
have a version of 5.0.4.stable.21982, Python-Redmine needs only the 5.0.4:

.. code-block:: python

   redmine = Redmine('https://redmine.url', version='5.0.4')

Authentication
++++++++++++++

Most of the time the API requires authentication. It can be done in 2 different ways:

* using user's regular login and password:

.. code-block:: python

   redmine = Redmine('https://redmine.url', username='foo', password='bar')

* using user's API key which is a handy way to avoid putting a password in a script:

.. code-block:: python

   redmine = Redmine('https://redmine.url', key='b244397884889a29137643be79c83f1d470c1e2fac')

The API key can be found on users account page when logged in, on the right-hand pane of
the default layout.

Impersonation
+++++++++++++

As of Redmine 2.2.0, you can impersonate user through the REST API. It must be set to a user login,
e.g. jsmith. This only works when using the API with an administrator account, this will be ignored
when using the API with a regular user account.

.. code-block:: python

   redmine = Redmine('https://redmine.url', impersonate='jsmith')

If the login specified does not exist or is not active, you will get an exception.

DateTime Formats
++++++++++++++++

Python-Redmine automatically converts Redmine's date/datetime strings to Python's date/datetime
objects:

.. code-block:: python

   '2013-12-31'           -> datetime.date(2013, 12, 31)
   '2013-12-31T13:27:47Z' -> datetime.datetime(2013, 12, 31, 13, 27, 47)

The conversion also works backwards, i.e. you can use Python's date/datetime objects when setting
resource attributes or in ``ResourceManager`` methods, e.g. ``filter()``:

.. code-block:: python

   datetime.date(2013, 12, 31)                 -> '2013-12-31'
   datetime.datetime(2013, 12, 31, 13, 27, 47) -> '2013-12-31T13:27:47Z'

If the conversion doesn't work for you and you receive strings instead of objects, you have a
different datetime formatting than default. To make the conversion work you have to tell Redmine
object what datetime formatting you're using, e.g. if the string returned is ``31.12.2013T13:27:47Z``:

.. code-block:: python

   redmine = Redmine('https://redmine.url', date_format='%d.%m.%Y', datetime_format='%d.%m.%YT%H:%M:%SZ')

Timezone
++++++++

.. versionadded:: 2.4.0

Redmine REST API expects and returns all datetime attributes in UTC. As described in the previous section,
by default Python-Redmine tries to convert datetime text representation to Python's naive datetime object
during attribute access and vice versa from Python's datetime object to the text representation ignoring
timezone information even if one exists. Since 2.4.0 a support for timezone aware datetime objects has
been added via a `timezone` argument which accepts either a string in a form of ±HHMM which is a time
offset from UTC in hours and minutes:

.. code-block:: python

   redmine = Redmine('https://redmine.url', timezone='-0930')

or any Python object which is a subclass of `datetime.tzinfo`:

.. code-block:: python

   from datetime import timezone

   redmine = Redmine('https://redmine.url', timezone=timezone.utc)

Main difference between the two is that ±HHMM string doesn't take DST into account, but requires no
extra packages to work, while a proper Python object which is a subclass of `datetime.tzinfo` does, but
may require you to install additional packages. If you're on Python 3.9+, there is a built-in `zoneinfo`
module which is a recommended way of specifying a timezone:

.. code-block:: python

   from zoneinfo import ZoneInfo

   redmine = Redmine('https://redmine.url', timezone=ZoneInfo('America/Los_Angeles'))

If you're on Python <3.9, there are several 3rd party packages that provide you with timezone databases
and classes that can be used as a value for Python-Redmine's `timezone` argument.

After setting a `timezone` attribute to the desired timezone, Python-Redmine will automatically convert
Redmine's datetime strings to Python's aware datetime objects:

.. code-block:: python

   '2013-12-31T13:27:47Z' -> datetime.datetime(2013, 12, 31, 5, 27, 47, tzinfo=zoneinfo.ZoneInfo(key='America/Los_Angeles'))

The conversion will also work backwards, i.e. you can use Python's aware datetime objects when setting
resource attributes or in ``ResourceManager`` methods, e.g. ``filter()``:

.. code-block:: python

   datetime.datetime(2013, 12, 31, 5, 27, 47, tzinfo=zoneinfo.ZoneInfo(key='America/Los_Angeles')) -> '2013-12-31T13:27:47Z'

Exception Control
+++++++++++++++++

If a requested attribute on a resource object doesn't exist, Python-Redmine will raise an
exception by default. Sometimes this may not be the desired behaviour. Python-Redmine provides
a way to control this type of exception.

You can completely turn it OFF for all resources:

.. code-block:: python

   redmine = Redmine('https://redmine.url', raise_attr_exception=False)

Or you can turn it ON only for some resources via a list or tuple of resource class names:

.. code-block:: python

   redmine = Redmine('https://redmine.url', raise_attr_exception=('Project', 'Issue', 'WikiPage'))

Connection Options
++++++++++++++++++

Python-Redmine uses Requests library for all the http(s) calls to Redmine server. Requests provides
sensible default connection options, but sometimes you may have a need to change them. For example
if your Redmine server uses SSL but the certificate is invalid you need to set a Requests's verify
option to False:

.. code-block:: python

   redmine = Redmine('https://redmine.url', requests={'verify': False})

Full list of available connection options can be found in the Requests
`documentation <http://docs.python-requests.org/en/latest/api/#requests.request>`_.

.. hint::

   Storing settings right in the code is a bad habit. Instead store them in some configuration
   file and then import them, for example if you use Django, you can create settings for
   Python-Redmine in project's settings.py file and then import them in the code, e.g.:

   .. code-block:: python

      # settings.py
      REDMINE_URL = 'https://redmine.url'
      REDMINE_KEY = 'b244397884889a29137643be79c83f1d470c1e2fac'

      # somewhere in the code
      from django.conf import settings
      from redminelib import Redmine

      redmine = Redmine(settings.REDMINE_URL, key=settings.REDMINE_KEY)

Request Engines
+++++++++++++++

See :doc:`advanced/request_engines` for details.

Custom Resources
++++++++++++++++

See :doc:`advanced/custom_resources` for details.
