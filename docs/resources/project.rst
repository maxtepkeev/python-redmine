Project
=======

Supported by Redmine starting from version 1.0

Manager
-------

All operations on the Project resource are provided by it's manager. To get access to
it you have to call ``redmine.project`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Project resource with given fields and saves it to the Redmine.

   :param string name: (required). Project name.
   :param string identifier: (required). Project identifier.
   :param string description: (optional). Project description.
   :param string homepage: (optional). Project homepage url.
   :param bool is_public: (optional). Whether project is public.
   :param int parent_id: (optional). Project's parent project id.
   :param bool inherit_members: (optional). Whether to inherit parent project's members.
   :param list tracker_ids: (optional). The ids of trackers for this project.
   :param list issue_custom_field_ids: (optional). The ids of issue custom fields for this project.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list enabled_module_names: (optional). The names of enabled modules for this project (Redmine >= 2.6.0 only).
   :return: :ref:`Resource` object

.. code-block:: python

   >>> project = redmine.project.create(
   ...     name='Vacation',
   ...     identifier='vacation',
   ...     description='foo',
   ...     homepage='http://foo.bar',
   ...     is_public=True,
   ...     parent_id=345,
   ...     inherit_members=True,
   ...     tracker_ids=[1, 2],
   ...     issue_custom_field_ids=[1, 2],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     enabled_module_names=['calendar', 'documents', 'files', 'gantt']
   ... )
   >>> project
   <redminelib.resources.Project #123 "Vacation">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Project resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> project = redmine.project.new()
   >>> project.name = 'Vacation'
   >>> project.identifier = 'vacation'
   >>> project.description = 'foo'
   >>> project.homepage = 'http://foo.bar'
   >>> project.is_public = True
   >>> project.parent_id = 345
   >>> project.inherit_members = True
   >>> project.tracker_ids = [1, 2]
   >>> project.issue_custom_field_ids = [1, 2]
   >>> project.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> project.enabled_module_names = ['calendar', 'documents', 'files', 'gantt']
   >>> project.save()
   <redminelib.resources.Project #123 "Vacation">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Project resource from Redmine by it's id or identifier.

   :param resource_id: (required). Project id or identifier.
   :type resource_id: int or string
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - trackers
    - issue_categories
    - enabled_modules (Redmine >= 2.6.0 only)
    - time_entry_activities (Redmine >= 3.4.0 only)

   :return: :ref:`Resource` object

.. code-block:: python

   >>> project = redmine.project.get('vacation', include=['trackers', 'issue_categories', 'enabled_modules', 'time_entry_activities'])
   >>> project
   <redminelib.resources.Project #123 "Vacation">

.. hint::

   Project resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Project
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Project resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.trackers
      <redminelib.resultsets.ResourceSet object with Tracker resources>

.. hint::

   Project resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to a Project
   resource object. The relations provided by the Project resource object are:

   * wiki_pages
   * memberships
   * issue_categories
   * versions
   * news
   * files
   * issues
   * time_entries
   * deals (requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_)
   * contacts (requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_)
   * deal_categories (requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_
     >= 3.3.0)

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.issues
      <redminelib.resultsets.ResourceSet object with Issue resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Project resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :param list include:
    .. raw:: html

       (optional). Redmine >= 2.6.0 only. Fetches associated data in one call. Accepted
       values:

    - trackers
    - issue_categories
    - enabled_modules
    - time_entry_activities

   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> projects = redmine.project.all(offset=10, limit=100, include=['trackers', 'issue_categories', 'enabled_modules', 'time_entry_activities'])
   >>> projects
   <redminelib.resultsets.ResourceSet object with Project resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Project resource and saves them to the Redmine.

   :param int resource_id: (required). Project id.
   :param string name: (optional). Project name.
   :param string description: (optional). Project description.
   :param string homepage: (optional). Project homepage url.
   :param bool is_public: (optional). Whether project is public.
   :param int parent_id: (optional). Project's parent project id.
   :param bool inherit_members: (optional). Whether to inherit parent project's members.
   :param list tracker_ids: (optional). The ids of trackers for this project.
   :param list issue_custom_field_ids: (optional). The ids of issue custom fields for this project.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list enabled_module_names: (optional). The names of enabled modules for this project (Redmine >= 2.6.0 only).
   :return: True

.. code-block:: python

   >>> redmine.project.update(
   ...     1,
   ...     name='Vacation',
   ...     description='foo',
   ...     homepage='http://foo.bar',
   ...     is_public=True,
   ...     parent_id=345,
   ...     inherit_members=True,
   ...     tracker_ids=[1, 2],
   ...     issue_custom_field_ids=[1, 2],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     enabled_module_names=['calendar', 'documents', 'files', 'gantt']
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Project
   :noindex:

   Saves the current state of a Project resource to the Redmine. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> project = redmine.project.get(1)
   >>> project.name = 'Vacation'
   >>> project.description = 'foo'
   >>> project.homepage = 'http://foo.bar'
   >>> project.is_public = True
   >>> project.parent_id = 345
   >>> project.inherit_members = True
   >>> project.tracker_ids = [1, 2]
   >>> project.issue_custom_field_ids = [1, 2]
   >>> project.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> project.enabled_module_names = ['calendar', 'documents', 'files', 'gantt']
   >>> project.save()
   <redminelib.resources.Project #1 "Vacation">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> project = redmine.project.get(1).save(
   ...     name='Vacation',
   ...     description='foo',
   ...     homepage='http://foo.bar',
   ...     is_public=True,
   ...     parent_id=345,
   ...     inherit_members=True,
   ...     tracker_ids=[1, 2],
   ...     issue_custom_field_ids=[1, 2],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     enabled_module_names=['calendar', 'documents', 'files', 'gantt']
   ... )
   >>> project
   <redminelib.resources.Project #1 "Vacation">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Project resource from Redmine by it's id or identifier.

   :param resource_id: (required). Project id or identifier.
   :type resource_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.project.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.Project
   :noindex:

   Deletes current Project resource object from Redmine.

   :return: True

.. code-block:: python

   >>> project = redmine.project.get(1)
   >>> project.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Project resources in one of the following formats: atom

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> projects = redmine.project.all()
   >>> projects.export('atom', savepath='/home/jsmith', filename='projects.atom')
   '/home/jsmith/projects.atom'
