Time Entry
==========

Supported by Redmine starting from version 1.1

Create
------

Supported keyword arguments:

* **issue_id** or **project_id** (required). The issue id or project id to log time on.
* **spent_on** (optional). The date the time was spent (defaults to the current date if not set).
* **hours** (required). The number of spent hours.
* **activity_id** (optional). The id of the time activity. This parameter is required unless a
  default activity is defined in Redmine.
* **comments** (optional). Short description for the entry (255 characters max).

.. code-block:: python

    >>> time_entry = redmine.time_entry.create(issue_id=123, spent_on='2014-01-14', hours=3, activity_id=10, comments='hello')
    >>> time_entry
    <redmine.resources.TimeEntry #12345>

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> time_entry = redmine.time_entry.get(374)
    >>> time_entry
    <redmine.resources.TimeEntry #374>

All
+++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

.. code-block:: python

    >>> time_entries = redmine.time_entry.all(offset=10, limit=100)
    >>> time_entries
    <redmine.resultsets.ResourceSet object with TimeEntry resources>

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **spent_on**. Hours spent on what date. (this could not work in some redmine
  versions)
* **from_date**. Limit the TimeEntry from this date 
* **to_date** . Limit the TimeEntry until this date
* **project_id**. Get time entries from the project with the given id, where id
  is either project id or project identifier.
* **user_id**. Get time entries for the given user id
* **hours**. Get only time entries that are =, >=, <= hours.

.. code-block:: python

    >>> time_entries = redmine.time_entry.filter(offset=10, limit=100, project_id='vacation', hours='>=8')
    >>> time_entries
    <redmine.resultsets.ResourceSet object with TimeEntry resources>

.. hint::

    You can also get time entries from an issue resource object directly using
    ``time_entries`` relation:

    .. code-block:: python

        >>> issue = redmine.issue.get(34213)
        >>> issue.time_entries
        <redmine.resultsets.ResourceSet object with TimeEntry resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Supported keyword arguments: None

.. code-block:: python

    >>> redmine.time_entry.delete(1)
    >>> True
