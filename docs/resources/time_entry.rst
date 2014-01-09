Time Entry
==========

Supported by Redmine starting from version 1.1

Create
------

Not yet supported by Python Redmine

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

* **spent_on**. Hours spent on what date.
* **project_id**. Get time entries from the project with the given id, where id
  is either project id or project identifier.
* **user_id**. Get time entries for the given user id
* **hours**. Get only time entries that are =, >=, <= hours.

.. code-block:: python

    >>> time_entries = redmine.user.filter(offset=10, limit=100, project_id='vacation', hours='>=8')
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

Not yet supported by Python Redmine
