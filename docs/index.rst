Python Redmine
==============

Python Redmine is a library for communicating with a `Redmine <http://www.redmine.org>`_
project management application. Redmine exposes some of it's data via `REST API
<http://www.redmine.org/projects/redmine/wiki/Rest_api>`_ for which Python Redmine provides
a simple but powerful Pythonic API inspired by a well-known `Django ORM
<https://docs.djangoproject.com/en/dev/topics/db/queries/>`_:

.. code-block:: python

    >>> redmine = Redmine('http://demo.redmine.org')
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

Table of contents
=================

.. toctree::
    :maxdepth: 2

    installation
    configuration
    operations
    resources/index
    exceptions
    license
    changelog
