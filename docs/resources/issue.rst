Issue
=====

Supported by Redmine starting from version 1.0

Manager
-------

All operations on the Issue resource are provided by its manager. To get access to
it you have to call ``redmine.issue`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Issue resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of issue's project.
   :type project_id: int or string
   :param string subject: (required). Issue subject.
   :param int tracker_id: (optional). Issue tracker id.
   :param string description: (optional). Issue description.
   :param int status_id: (optional). Issue status id.
   :param int priority_id: (optional). Issue priority id.
   :param int category_id: (optional). Issue category id.
   :param int fixed_version_id: (optional). Issue version id.
   :param bool is_private: (optional). Whether issue is private.
   :param int assigned_to_id: (optional). Issue will be assigned to this user id.
   :param list watcher_user_ids: (optional). User ids watching this issue.
   :param int parent_issue_id: (optional). Parent issue id.
   :param start_date: (optional). Issue start date.
   :type start_date: string or date object
   :param due_date: (optional). Issue end date.
   :type due_date: string or date object
   :param int estimated_hours: (optional). Issue estimated hours.
   :param int done_ratio: (optional). Issue done ratio.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> from io import BytesIO
   >>> issue = redmine.issue.create(
   ...     project_id='vacation',
   ...     subject='Vacation',
   ...     tracker_id=8,
   ...     description='foo',
   ...     status_id=3,
   ...     priority_id=7,
   ...     assigned_to_id=123,
   ...     watcher_user_ids=[123],
   ...     parent_issue_id=345,
   ...     start_date=datetime.date(2014, 1, 1),
   ...     due_date=datetime.date(2014, 2, 1),
   ...     estimated_hours=4,
   ...     done_ratio=40,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> issue
   <redminelib.resources.Issue #123 "Vacation">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Issue resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

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
   >>> issue.start_date = datetime.date(2014, 1, 1)
   >>> issue.due_date = datetime.date(2014, 2, 1)
   >>> issue.estimated_hours = 4
   >>> issue.done_ratio = 40
   >>> issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   >>> issue.save()
   <redminelib.resources.Issue #123 "Vacation">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Issue resource from Redmine by its id.

   :param int resource_id: (required). Id of the issue.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - children
    - attachments
    - relations
    - changesets
    - journals
    - watchers (requires Redmine >= 2.3.0)
    - allowed_statuses (requires Redmine >= 5.0.0)

   :return: :ref:`Resource` object

.. code-block:: python

   >>> issue = redmine.issue.get(34441, include=['children', 'journals', 'watchers'])
   >>> issue
   <redminelib.resources.Issue #34441 "Vacation">

.. hint::

   Issue resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with an Issue
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Issue resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> issue = redmine.issue.get(34441)
      >>> issue.journals
      <redminelib.resultsets.ResourceSet object with IssueJournal resources>

.. hint::

   Issue resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to an Issue
   resource object. The relations provided by the Issue resource object are:

   * relations
   * time_entries
   * checklists (requires Pro Edition and `Checklists plugin <https://www.redmineup.com/pages/plugins/checklists>`_)

   .. code-block:: python

      >>> issue = redmine.issue.get(34441)
      >>> issue.time_entries
      <redminelib.resultsets.ResourceSet object with TimeEntry resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Issue resources (both open and closed) from Redmine, to return issues with specific
   status from Redmine use ``filter()`` method below.

   :param string sort: (optional). Column to sort. Append :desc to invert the order.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - relations
    - attachments (requires Redmine >= 3.4.0)

   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> issues = redmine.issue.all(sort='category:desc', include=['relations', 'attachments'])
   >>> issues
   <redminelib.resultsets.ResourceSet object with Issue resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Issue resources that match the given lookup parameters.

   :param issue_id: (optional). Find issue or issues by id (separated by ``,``)
   :type issue_id: int or string
   :param int parent_id: (optional). Get issues whose parent issue is given id.
   :param project_id: (optional). Id or identifier of issue's project.
   :type project_id: int or string
   :param subproject_id: (optional). Get issues from the subproject with the
    given id. You can use ``project_id=X, subproject_id=!*`` to get only the issues of
    a given project and none of its subprojects.
   :type subproject_id: int or string
   :param int tracker_id: (optional). Get issues from the tracker with given id.
   :param int query_id: (optional). Get issues for the given query id if the project_id is given.
   :param status_id:
    .. raw:: html

       (optional). Get issues with given status id. One of:

    - open - open issues
    - closed - closed issues
    - \* - all issues
    - id - status id

   :type status_id: int or string
   :param int author_id: (optional). Get issues which are authored by the given user id.
   :param int assigned_to_id: (optional). Get issues which are assigned to the given user id.
    To get the issues assigned to the user whose credentials were used to access the API pass ``me``
    as a string.
   :param string cf_x: (optional). Get issues with given value for custom field with an ID of x.
    The ``~`` sign can be used before the value to find issues containing a string in a custom field.
   :param string sort: (optional). Column to sort. Append :desc to invert the order.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - relations
    - attachments (requires Redmine >= 3.4.0)

   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> issues = redmine.issue.filter(
   ...     project_id='vacation',
   ...     subproject_id='!*',
   ...     created_on='><2012-03-01|2012-03-07',
   ...     cf_22='~foo',
   ...     sort='category:desc'
   ... )
   >>> issues
   <redminelib.resultsets.ResourceSet object with Issue resources>
   
.. code-block:: python

   >>> issues = redmine.issue.filter(
   ...     project_id='vacation',
   ...     query_id=326
   ... )
   >>> issues
   <redminelib.resultsets.ResourceSet object with Issue resources>

.. hint::

   You can also get issues from a Project, Tracker, IssueStatus or User resource objects directly
   using ``issues`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.issues
      <redminelib.resultsets.ResourceSet object with Issue resources>

   .. versionadded:: 2.5.0

   Apart from ``issues`` relation a User resource object provides ``issues_assigned`` which is an alias
   to ``issues`` relation and ``issues_authored`` relation which returns Issue objects authored by a user:

   .. code-block:: python

      >>> user = redmine.user.get(9)
      >>> user.issues
      <redminelib.resultsets.ResourceSet object with Issue resources>
      >>> user.issues_assigned
      <redminelib.resultsets.ResourceSet object with Issue resources>
      >>> user.issues_authored
      <redminelib.resultsets.ResourceSet object with Issue resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an Issue resource and saves them to the Redmine.

   :param int resource_id: (required). Issue id.
   :param int project_id: (optional). Issue project id.
   :param string subject: (optional). Issue subject.
   :param int tracker_id: (optional). Issue tracker id.
   :param string description: (optional). Issue description.
   :param string notes: (optional). Issue journal note.
   :param bool private_notes: (optional). Whether notes are private.
   :param int status_id: (optional). Issue status id.
   :param int priority_id: (optional). Issue priority id.
   :param int category_id: (optional). Issue category id.
   :param int fixed_version_id: (optional). Issue version id.
   :param bool is_private: (optional). Whether issue is private.
   :param int assigned_to_id: (optional). Issue will be assigned to this user id.
   :param int parent_issue_id: (optional). Parent issue id.
   :param start_date: (optional). Issue start date.
   :type start_date: string or date object
   :param due_date: (optional). Issue end date.
   :type due_date: string or date object
   :param int estimated_hours: (optional). Issue estimated hours.
   :param int done_ratio: (optional). Issue done ratio.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> from io import BytesIO
   >>> redmine.issue.update(
   ...     1,
   ...     project_id=1,
   ...     subject='Vacation',
   ...     tracker_id=8,
   ...     description='foo',
   ...     notes='A journal note',
   ...     private_notes=True,
   ...     status_id=3,
   ...     priority_id=7,
   ...     assigned_to_id=123,
   ...     parent_issue_id=345,
   ...     start_date=datetime.date(2014, 1, 1),
   ...     due_date=datetime.date(2014, 2, 1),
   ...     estimated_hours=4,
   ...     done_ratio=40,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Issue
   :noindex:

   Saves the current state of an Issue resource to the Redmine. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> issue = redmine.issue.get(1)
   >>> issue.project_id = 1
   >>> issue.subject = 'Vacation'
   >>> issue.tracker_id = 8
   >>> issue.description = 'foo'
   >>> issue.notes = 'A journal note'
   >>> issue.private_notes = True
   >>> issue.status_id = 3
   >>> issue.priority_id = 7
   >>> issue.assigned_to_id = 123
   >>> issue.parent_issue_id = 345
   >>> issue.start_date = datetime.date(2014, 1, 1)
   >>> issue.due_date = datetime.date(2014, 2, 1)
   >>> issue.estimated_hours = 4
   >>> issue.done_ratio = 40
   >>> issue.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> issue.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   >>> issue.save()
   <redminelib.resources.Issue #1 "Vacation">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> issue = redmine.issue.get(1).save(
   ...     project_id=1,
   ...     subject='Vacation',
   ...     tracker_id=8,
   ...     description='foo',
   ...     notes='A journal note',
   ...     private_notes=True,
   ...     status_id=3,
   ...     priority_id=7,
   ...     assigned_to_id=123,
   ...     parent_issue_id=345,
   ...     start_date=datetime.date(2014, 1, 1),
   ...     due_date=datetime.date(2014, 2, 1),
   ...     estimated_hours=4,
   ...     done_ratio=40,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   ... )
   >>> issue
   <redminelib.resources.Issue #1 "Vacation">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Issue resource from Redmine by its id.

   :param int resource_id: (required). Issue id.
   :return: True

.. code-block:: python

   >>> redmine.issue.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.Issue
   :noindex:

   Deletes current Issue resource object from Redmine.

   :return: True

.. code-block:: python

   >>> issue = redmine.issue.get(1)
   >>> issue.delete()
   True

Copying
-------

.. versionadded:: 2.5.0

.. py:method:: copy(resource_id, project_id=None, link_original=True, include=('subtasks', 'attachments'), **fields)
   :module: redminelib.managers.IssueManager
   :noindex:

   Copies single Issue resource by its id using the same API as Redmine's GUI copying which means copying
   is done the most efficient way possible. By default links original to a copy via relations and copies
   both subtasks and attachments.

   :param int resource_id: (required). Issue id.
   :param project_id: (required). Id or identifier of issue's project.
   :type project_id: int or string
   :param bool link_original: (optional). Whether to link the original issue to a copy via relations.
   :param list include:
    .. raw:: html

       (optional). Additional data to copy or <code>None</code>. Accepted values:

    - subtasks
    - attachments

   :param dict fields: (optional). Accepts the same fields as Issue's ``create()`` method to add or modify original values.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> copy = redmine.issue.copy(1, project_id='vacation', link_original=False, include=['attachments'])
   >>> copy
   <redminelib.resources.Issue #124 "Vacation">

.. py:method:: copy(link_original=True, include=('subtasks', 'attachments'), **fields)
   :module: redminelib.resources.Issue
   :noindex:

   Copies current Issue resource object.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> copy = issue.copy(subject='this is a copy')
   >>> copy
   <redminelib.resources.Issue #124 "this is a copy">

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resources.Issue
   :noindex:

   Exports Issue resource in one of the following formats: atom, pdf

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> issue.export('pdf', savepath='/home/jsmith')
   '/home/jsmith/123.pdf'

.. py:method:: export(fmt, savepath=None, filename=None, columns=None, encoding='UTF-8')
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Issue resources in one of the following formats: atom, pdf, csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :param columns: (optional). Iterable of column names or "all" string for all available columns
    or "all_gui" string for GUI like behaviour or iterable of elements with "all_gui" string and
    additional columns to export.
   :type columns: iterable or string
   :param encoding: (optional). Encoding that will be used for the result file.
   :return: String or Object

.. code-block:: python

   >>> issues = redmine.issue.all()
   >>> issues.export('csv', savepath='/home/jsmith', filename='issues.csv', columns='all')
   '/home/jsmith/issues.csv'

Journals
--------

The history of an issue is represented as a :ref:`ResourceSet` of ``IssueJournal`` resources.
Currently the following operations are possible:

create
++++++

To create a new record in issue history, i.e. new journal:

.. code-block:: python

   redmine.issue.update(1, notes='new note')
   True

read
++++

Recommended way to access issue journals is through associated data includes:

.. code-block:: python

   >>> issue = redmine.issue.get(1, include=['journals'])
   >>> issue.journals
   <redminelib.resultsets.ResourceSet object with IssueJournal resources>

But they can also be accessed through on demand includes:

.. code-block:: python

   >>> issue = redmine.issue.get(1)
   >>> issue.journals
   <redminelib.resultsets.ResourceSet object with IssueJournal resources>

After that they can be used as usual:

.. code-block:: python

   >>> for journal in issue.journals:
   ...     print(journal.id, journal.notes)
   ...
   1 foobar
   2 lalala
   3 hohoho

update
++++++

.. versionadded:: 2.4.0

To update `notes` attribute (the only attribute that can be updated) of a journal:

.. code-block:: python

   >>> issue = redmine.issue.get(1, include=['journals'])
   >>> for journal in issue.journals:
   ...     journal.save(notes='setting notes to a new value')
   ...

Or if you know the `id` beforehand:

.. code-block:: python

   >>> redmine.issue_journal.update(1, notes='setting notes to a new value')
   True

delete
++++++

.. versionadded:: 2.4.0

To delete a journal set its `notes` attribute to empty string:

.. code-block:: python

   >>> issue = redmine.issue.get(1, include=['journals'])
   >>> for journal in issue.journals:
   ...     journal.save(notes='')
   ...

Or if you know the `id` beforehand:

.. code-block:: python

   >>> redmine.issue_journal.update(1, notes='')
   True

.. note::

   You can only delete a journal that doesn't have the associated `details` attribute.

Watchers
--------

Python-Redmine provides 2 methods to work with issue watchers:

add
+++

.. py:method:: add(user_id)
   :module: redminelib.resources.Issue.Watcher
   :noindex:

   Adds a user to issue watchers list by its id.

   :param int user_id: (required). User id.
   :return: True

.. code-block:: python

   >>> issue = redmine.issue.get(1)
   >>> issue.watcher.add(1)
   True

remove
++++++

.. py:method:: remove(user_id)
   :module: redminelib.resources.Issue.Watcher
   :noindex:

   Removes a user from issue watchers list by its id.

   :param int user_id: (required). User id.
   :return: True

.. code-block:: python

   >>> issue = redmine.issue.get(1)
   >>> issue.watcher.remove(1)
   True
