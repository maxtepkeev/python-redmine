Issue
=====

Supported by Redmine starting from version 1.0

Create
------

Not yet supported by Python Redmine

Read
----

Relations
~~~~~~~~~

Issue resource object provides you with some relations. Relations are the other
resource objects wrapped in a ResourceSet which are somehow related to an Issue
resource object. The relations provided by the Issue resource object are:

* relations
* time_entries

.. code-block:: python

    >>> issue = redmine.issue.get(34441)
    >>> issue.time_entries
    <redmine.resultsets.ResourceSet object with TimeEntry resources>

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **include**. Can be used to fetch associated data in one call. Accepted values (separated by comma):

  - children
  - attachments
  - relations
  - changesets
  - journals
  - watchers

.. code-block:: python

    >>> issue = redmine.issue.get(34441, include='children,journals,watchers')
    >>> issue.subject
    'Vacation'

All
+++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.
* **sort**. column to sort with. Append :desc to invert the order.

.. code-block:: python

    >>> issues = redmine.issue.all(offset=10, limit=100, sort='category:desc')
    >>> issues
    <redmine.resultsets.ResourceSet object with Issue resources>

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.
* **sort**. column to sort with. Append :desc to invert the order.

Supported filters:

* **project_id**. Get issues from the project with the given id, where id is either
  project id or project identifier.
* **subproject_id**. Get issues from the subproject with the given id. You can use
  project_id=XXX&subproject_id=!* to get only the issues of a given project and
  none of its subprojects.
* **tracker_id**. Get issues from the tracker with the given id.
* **query_id**. Get issues for the given query_id only.
* **status_id**. Get issues with the given status id only. Possible values are:

  - open - open issues
  - closed - closed issues
  - \* - all issues

* **assigned_to_id**. Get issues which are assigned to the given user id.
* **cf_x**. Get issues with the given value for custom field with an ID of x.

.. code-block:: python

    >>> issues = redmine.issue.filter(project_id='vacation', subproject_id='!*', created_on='><2012-03-01|2012-03-07', sort='category:desc')
    >>> issues
    <redmine.resultsets.ResourceSet object with Issue resources>

.. hint::

    You can also get issues from a project resource object directly using
    ``issues`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.issues
        <redmine.resultsets.ResourceSet object with Issue resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
