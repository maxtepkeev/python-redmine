Python Redmine
==============

.. image:: https://badge.fury.io/py/python-redmine.svg
    :target: https://badge.fury.io/py/python-redmine

.. image:: https://pypip.in/download/python-redmine/badge.svg
    :target: https://pypi.python.org/pypi/python-redmine/

.. image:: https://travis-ci.org/maxtepkeev/python-redmine.svg?branch=master
    :target: https://travis-ci.org/maxtepkeev/python-redmine

.. image:: https://img.shields.io/coveralls/maxtepkeev/python-redmine/master.svg
    :target: https://coveralls.io/r/maxtepkeev/python-redmine?branch=master

|

Python Redmine is a library for communicating with a `Redmine <http://www.redmine.org>`_
project management application. Redmine exposes some of it's data via `REST API
<http://www.redmine.org/projects/redmine/wiki/Rest_api>`_ for which Python Redmine provides
a simple but powerful Pythonic API inspired by a well-known `Django ORM
<https://docs.djangoproject.com/en/dev/topics/db/queries/>`_:

.. code-block:: python

    >>> from redmine import Redmine

    >>> redmine = Redmine('http://demo.redmine.org', username='foo', password='bar')
    >>> project = redmine.project.get('vacation')

    >>> project.id
    30404

    >>> project.identifier
    'vacation'

    >>> project.created_on
    datetime.datetime(2013, 12, 31, 13, 27, 47)

    >>> project.issues
    <redmine.resultsets.ResourceSet object with Issue resources>

    >>> project.issues[0]
    <redmine.resources.Issue #34441 "Vacation">

    >>> dir(project.issues[0])
    ['assigned_to', 'author', 'created_on', 'description', 'done_ratio',
    'due_date', 'estimated_hours', 'id', 'priority', 'project', 'relations',
    'start_date', 'status', 'subject', 'time_entries', 'tracker', 'updated_on']

    >>> project.issues[0].subject
    'Vacation'

    >>> project.issues[0].time_entries
    <redmine.resultsets.ResourceSet object with TimeEntry resources>

Features
--------

* Supports 100% of Redmine API features
* Supports Python 2.6 - 3.4
* Extensively documented
* Provides ORM-style Pythonic API

Contacts and Support
--------------------

I will be glad to get your feedback, `pull requests <https://github.com/maxtepkeev/python-redmine/pulls>`_,
`issues <https://github.com/maxtepkeev/python-redmine/issues>`_, whatever. Feel free to contact me for any
questions.

Donations and Sponsorship
-------------------------

If you like this project and want to support it you have 3 options:

#. Just give this project a star at the top of the `GitHub <https://github.com/maxtepkeev/python-redmine>`_
   repository. That doesn't cost you anything but makes the `author <https://github.com/maxtepkeev>`_ happier.
#. You can express your gratitude via `Gratipay <https://gratipay.com/maxtepkeev/>`_.
#. Become a sponsor. Contact me via ``tepkeev at gmail dot com`` if you are interested in becoming a sponsor
   and we will discuss the terms and conditions.

Copyright and License
---------------------

Python Redmine is licensed under Apache 2.0 license. Check the :doc:`license` for details.

Table of contents
-----------------

.. toctree::
    :maxdepth: 2

    installation
    configuration
    operations
    resources/index
    advanced/index
    FAQ <faq>
    exceptions
    license
    changelog
