Issue
=====

Supported by Redmine starting from version 1.0

Manager
-------

All operations on the issue resource are provided via it's manager. To get access to it
you have to call ``redmine.issue`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new issue resource with given fields and saves it to the Redmine.

    :param project_id: (required). Id or identifier of issue's project.
    :type project_id: integer or string
    :param string subject: (required). Issue subject.
    :param integer tracker_id: (optional). Issue tracker id.
    :param string description: (optional). Issue description.
    :param integer status_id: (optional). Issue status id.
    :param integer priority_id: (optional). Issue priority id.
    :param integer category_id: (optional). Issue category id.
    :param integer fixed_version_id: (optional). Issue version id.
    :param boolean is_private: (optional). Whether issue is private.
    :param integer assigned_to_id: (optional). Issue will be assigned to this user id.
    :param watcher_user_ids: (optional). User ids who will be watching this issue.
    :type watcher_user_ids: list or tuple
    :param integer parent_issue_id: (optional). Parent issue id.
    :param start_date: (optional). Issue start date.
    :type start_date: string or date object
    :param due_date: (optional). Issue end date.
    :type due_date: string or date object
    :param integer estimated_hours: (optional). Issue estimated hours.
    :param integer done_ratio: (optional). Issue done ratio.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :param uploads:
      .. raw:: html

          (optional). Uploads in the form of [{'': ''}, ...], accepted keys are:

      - path (required). Absolute path to the file that should be uploaded.
      - filename (optional). Name of the file after upload.
      - description (optional). Description of the file.
      - content_type (optional). Content type of the file.

    :type uploads: list or tuple
    :return: Issue resource object

.. code-block:: python

    >>> issue = redmine.issue.create(project_id='vacation', subject='Vacation', tracker_id=8, description='foo', status_id=3, priority_id=7, assigned_to_id=123, watcher_user_ids=[123], parent_issue_id=345, start_date='2014-01-01', due_date='2014-02-01', estimated_hours=4, done_ratio=40, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}], uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}])
    >>> issue
    <redmine.resources.Issue #123 "Vacation">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty issue resource but doesn't save it to the Redmine. This is useful if
    you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: Issue resource object

.. code-block:: python

    >>> issue = redmine.issue.new()
    >>> issue.project_id = 'vacation'
    >>> issue.subject = 'Vacation'
    >>> issue.tracker_id = 8
    >>> issue.description = 'foo'
    >>> issue.status_id = 3
    >>> issue.priority_id = 7
    >>> issue.assigned_to_id = 123
    >>> issue.watcher_user_ids = [123]
    >>> issue.parent_issue_id = 345
    >>> issue.start_date = date(2014, 1, 1)
    >>> issue.due_date = date(2014, 2, 1)
    >>> issue.estimated_hours = 4
    >>> issue.done_ratio = 40
    >>> issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
    >>> issue.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single issue resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the issue.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - children
      - attachments
      - relations
      - changesets
      - journals
      - watchers

    :return: Issue resource object

.. code-block:: python

    >>> issue = redmine.issue.get(34441, include='children,journals,watchers')
    >>> issue
    <redmine.resources.Issue #34441 "Vacation">

.. hint::

    .. versionadded:: 0.4.0

    |

    Issue resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with an Issue
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the Issue resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> issue = redmine.issue.get(34441)
        >>> issue.journals
        <redmine.resultsets.ResourceSet object with IssueJournal resources>

.. hint::

    Issue resource object provides you with some relations. Relations are the other
    resource objects wrapped in a ResourceSet which are somehow related to an Issue
    resource object. The relations provided by the Issue resource object are:

    * relations
    * time_entries

    .. code-block:: python

        >>> issue = redmine.issue.get(34441)
        >>> issue.time_entries
        <redmine.resultsets.ResourceSet object with TimeEntry resources>

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all issue resources from the Redmine.

    :param string sort: (optional). Column to sort with. Append :desc to invert the order.
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> issues = redmine.issue.all(sort='category:desc')
    >>> issues
    <redmine.resultsets.ResourceSet object with Issue resources>

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns issue resources that match the given lookup parameters.

    :param project_id: (optional). Id or identifier of issue's project.
    :type project_id: integer or string
    :param subproject_id: (optional). Get issues from the subproject with the
      given id. You can use project_id=X, subproject_id=!* to get only the issues of
      a given project and none of its subprojects.
    :type subproject_id: integer or string
    :param integer tracker_id: (optional). Get issues from the tracker with the given id.
    :param integer query_id: (optional). Get issues for the given query id.
    :param status_id:
      .. raw:: html

          (optional). Get issues with the given status id. Possible values are:

      - open - open issues
      - closed - closed issues
      - \* - all issues
      - id - status id

    :type status_id: integer or string
    :param integer assigned_to_id: (optional). Get issues which are assigned to the given user id.
      To get the issues assigned to the user whose credentials were used to access the API pass ``me``
      as a string.
    :param string cf_x: (optional). Get issues with the given value for custom field with an ID of x.
    :param string sort: (optional). Column to sort with. Append :desc to invert the order.
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

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

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of an issue resource and saves them to the Redmine.

    :param integer resource_id: (required). Issue id.
    :param integer project_id: (optional). Issue project id.
    :param string subject: (optional). Issue subject.
    :param integer tracker_id: (optional). Issue tracker id.
    :param string description: (optional). Issue description.
    :param string notes: (optional). Issue journal note.
    :param integer status_id: (optional). Issue status id.
    :param integer priority_id: (optional). Issue priority id.
    :param integer category_id: (optional). Issue category id.
    :param integer fixed_version_id: (optional). Issue version id.
    :param boolean is_private: (optional). Whether issue is private.
    :param integer assigned_to_id: (optional). Issue will be assigned to this user id.
    :param integer parent_issue_id: (optional). Parent issue id.
    :param start_date: (optional). Issue start date.
    :type start_date: string or date object
    :param due_date: (optional). Issue end date.
    :type due_date: string or date object
    :param integer estimated_hours: (optional). Issue estimated hours.
    :param integer done_ratio: (optional). Issue done ratio.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :param uploads:
      .. raw:: html

          (optional). Uploads in the form of [{'': ''}, ...], accepted keys are:

      - path (required). Absolute path to the file that should be uploaded.
      - filename (optional). Name of the file after upload.
      - description (optional). Description of the file.
      - content_type (optional). Content type of the file.

    :type uploads: list or tuple
    :return: True

.. code-block:: python

    >>> redmine.issue.update(1, project_id=1, subject='Vacation', tracker_id=8, description='foo', notes='A journal note', status_id=3, priority_id=7, assigned_to_id=123, parent_issue_id=345, start_date='2014-01-01', due_date='2014-02-01', estimated_hours=4, done_ratio=40, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}], uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Issue
    :noindex:

    Saves the current state of an issue resource to the Redmine. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> issue = redmine.issue.get(1)
    >>> issue.project_id = 1
    >>> issue.subject = 'Vacation'
    >>> issue.tracker_id = 8
    >>> issue.description = 'foo'
    >>> issue.notes = 'A journal note'
    >>> issue.status_id = 3
    >>> issue.priority_id = 7
    >>> issue.assigned_to_id = 123
    >>> issue.parent_issue_id = 345
    >>> issue.start_date = date(2014, 1, 1)
    >>> issue.due_date = date(2014, 2, 1)
    >>> issue.estimated_hours = 4
    >>> issue.done_ratio = 40
    >>> issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
    >>> issue.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single issue resource from the Redmine by it's id.

    :param integer resource_id: (required). Issue id.
    :return: True

.. code-block:: python

    >>> redmine.issue.delete(1)
    True

Watchers
--------

.. versionadded:: 0.5.0

Python Redmine provides 2 methods to work with issue watchers: ``add`` and ``remove``.

add
+++

.. py:method:: add(user_id)
    :module: redmine.resources.Issue.Watcher
    :noindex:

    Adds a user to issue watchers list by it's id.

    :param integer user_id: (required). User id.
    :return: True

.. code-block:: python

    >>> issue = redmine.issue.get(1)
    >>> issue.watcher.add(1)
    True

remove
++++++

.. py:method:: remove(user_id)
    :module: redmine.resources.Issue.Watcher
    :noindex:

    Removes a user from issue watchers list by it's id.

    :param integer user_id: (required). User id.
    :return: True

.. code-block:: python

    >>> issue = redmine.issue.get(1)
    >>> issue.watcher.remove(1)
    True
