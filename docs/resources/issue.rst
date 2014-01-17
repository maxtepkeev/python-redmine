Issue
=====

Supported by Redmine starting from version 1.0

Create
------

Supported keyword arguments:

* **project_id** (required). Project identifier where issue will be created.
* **subject** (required). Issue subject.
* **tracker_id** (optional). Issue tracker id.
* **description** (optional). Issue description.
* **status_id** (optional). Issue status id.
* **priority_id** (optional). Issue priority id.
* **category_id** (optional). Issue category id.
* **fixed_version_id** (optional). Issue version id.
* **is_private** (optional). Whether issue is private.
* **assigned_to_id** (optional). Issue will be assigned to this user id.
* **watcher_user_ids** (optional). User ids who will be watching this issue as a list or tuple.
* **parent_issue_id** (optional). Id of the parent issue.
* **start_date** (optional). Issue start date.
* **due_date** (optional). Issue end date.
* **estimated_hours** (optional). Issue estimated hours.
* **done_ratio** (optional). Issue done ratio.
* **custom_fields** (optional). Value of custom fields as a dictionary in the form of {id: value}.
* **uploads** (optional). List or tuple of dicts in the form of [{'': ''}, {'': ''}], accepted keys are:

  - path (required). Absolute path to the file that should be uploaded.
  - filename (optional). Name of the file after upload.
  - description (optional). Description of the file.
  - content_type (optional). Content type of the file.

.. code-block:: python

    >>> issue = redmine.issue.create(project_id='vacation', subject='Vacation', tracker_id=8, description='foo', status_id=3, priority_id=7, assigned_to_id=123, watcher_user_ids=[123], parent_issue_id=345, start_date='2014-01-01', due_date='2014-02-01', estimated_hours=4, done_ratio=40, uploads=[{'path': '/some/path/to/file'}, {'path': '/some/path/to/file2'}])
    >>> issue
    <redmine.resources.Issue #123 "Vacation">

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

Supported keyword arguments: None

.. code-block:: python

    >>> redmine.issue.delete(1)
    >>> True
