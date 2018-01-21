Time Entry
==========

Supported by Redmine starting from version 1.1

Manager
-------

All operations on the TimeEntry resource are provided by it's manager. To get access
to it you have to call ``redmine.time_entry`` where ``redmine`` is a configured redmine
object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new TimeEntry resource with given fields and saves it to the Redmine.

   :param int issue_id or project_id: (required). The issue id or project id to log time on.
   :param hours: (required). The number of spent hours.
   :type hours: int or float
   :param spent_on: (optional). The date the time was spent (current date if not set).
   :type spent_on: string or date object
   :param int activity_id: (optional). The id of the time activity. This parameter is required unless
    a default activity is defined in Redmine. Available activity ids can be retrieved per project
    using ``include='time_entry_activities'``, requires Redmine >= 3.4.0.
   :param string comments: (optional). Short description for the entry (255 characters max).
   :return: :ref:`Resource` object

.. code-block:: python

   >>> time_entry = redmine.time_entry.create(
   ...     issue_id=123,
   ...     spent_on=datetime.date(2014, 1, 14),
   ...     hours=3,
   ...     activity_id=10,
   ...     comments='hello'
   ... )
   >>> time_entry
   <redminelib.resources.TimeEntry #12345>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty TimeEntry resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.bove.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> time_entry = redmine.time_entry.new()
   >>> time_entry.issue_id = 123
   >>> time_entry.spent_on = datetime.date(2014, 1, 14)
   >>> time_entry.hours = 3
   >>> time_entry.activity_id = 10
   >>> time_entry.comments = 'hello'
   >>> time_entry.save()
   <redminelib.resources.TimeEntry #12345>

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single TimeEntry resource from Redmine by it's id.

   :param int resource_id: (required). Id of the time entry.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> time_entry = redmine.time_entry.get(374)
   >>> time_entry
   <redminelib.resources.TimeEntry #374>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all TimeEntry resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> time_entries = redmine.time_entry.all(offset=10, limit=100)
   >>> time_entries
   <redminelib.resultsets.ResourceSet object with TimeEntry resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns TimeEntry resources that match the given lookup parameters.

   :param project_id: (optional). Get time entries from the project with given id.
   :type project_id: int or string
   :param int issue_id: (optional). Get time entries from the issue with given id.
   :param int user_id: (optional). Get time entries for the user with given id.
   :param spent_on: (optional). Redmine >= 2.3.0 only. Date when time was spent.
   :type spent_on: string or date object
   :param from_date: (optional). Limit time entries from this date.
   :type from_date: string or date object
   :param to_date: (optional). Limit time entries until this date.
   :type to_date: string or date object
   :param string hours: (optional). Get only time entries that are =, >=, <= hours.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: ResourceSet object

.. code-block:: python

   >>> time_entries = redmine.time_entry.filter(offset=10, limit=100, project_id='vacation', hours='>=8')
   >>> time_entries
   <redminelib.resultsets.ResourceSet object with TimeEntry resources>

.. hint::

   You can also get time entries from an Issue, Project and User resource objects directly
   using ``time_entries`` relation:

   .. code-block:: python

      >>> issue = redmine.issue.get(34213)
      >>> issue.time_entries
      <redminelib.resultsets.ResourceSet object with TimeEntry resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a TimeEntry resource and saves them to the Redmine.

   :param int resource_id: (required). Time entry id.
   :param int issue_id or project_id: (optional). The issue id or project id to log time on.
   :param int hours: (optional). The number of spent hours.
   :param spent_on: (optional). The date the time was spent.
   :type spent_on: string or date object
   :param int activity_id: (optional). The id of the time activity. Available activity ids can
    be retrieved per project using ``include='time_entry_activities'``, requires Redmine >= 3.4.0.
   :param string comments: (optional). Short description for the entry (255 characters max).
   :return: True

.. code-block:: python

   >>> redmine.time_entry.update(
   ...     1,
   ...     issue_id=123,
   ...     spent_on=datetime.date(2014, 1, 14),
   ...     hours=3,
   ...     activity_id=10,
   ...     comments='hello'
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.TimeEntry
   :noindex:

   Saves the current state of a TimeEntry resource to the Redmine. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> time_entry = redmine.time_entry.get(1)
   >>> time_entry.issue_id = 123
   >>> time_entry.spent_on = datetime.date(2014, 1, 14)
   >>> time_entry.hours = 3
   >>> time_entry.activity_id = 10
   >>> time_entry.comments = 'hello'
   >>> time_entry.save()
   <redminelib.resources.TimeEntry #1>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> time_entry = redmine.time_entry.get(1).save(
   ...     issue_id=123,
   ...     spent_on=datetime.date(2014, 1, 14),
   ...     hours=3,
   ...     activity_id=10,
   ...     comments='hello'
   ... )
   >>> time_entry
   <redminelib.resources.TimeEntry #1>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single TimeEntry resource from Redmine by it's id.

   :param int resource_id: (required). Time entry id.
   :return: True

.. code-block:: python

   >>> redmine.time_entry.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.TimeEntry
   :noindex:

   Deletes current TimeEntry resource object from Redmine.

   :return: True

.. code-block:: python

   >>> entry = redmine.time_entry.get(1)
   >>> entry.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of TimeEntry resources in one of the following formats: atom, csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> entries = redmine.time_entry.all()
   >>> entries.export('csv', savepath='/home/jsmith', filename='entries.csv')
   '/home/jsmith/entries.csv'
