Version
=======

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the Version resource are provided by it's manager. To get access
to it you have to call ``redmine.version`` where ``redmine`` is a configured redmine
object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Version resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of version's project.
   :type project_id: int or string
   :param string name: (required). Version name.
   :param string status:
    .. raw:: html

       (optional). Status of the version, one of:

    - open (default)
    - locked
    - closed

   :param string sharing:
    .. raw:: html

       (optional). Version sharing, one of:

    - none (default)
    - descendants
    - hierarchy
    - tree
    - system

   :param due_date: (optional). Expiration date.
   :type due_date: string or date object
   :param string description: (optional). Version description.
   :param string wiki_page_title: (optional). Version wiki page title.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> version = redmine.version.create(
   ...     project_id='vacation',
   ...     name='Vacation',
   ...     status='open',
   ...     sharing='none',
   ...     due_date=datetime.date(2014, 1, 30),
   ...     description='my vacation',
   ...     wiki_page_title='Vacation'
   ... )
   >>> version
   <redminelib.resources.Version #235 "Vacation">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Version resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> version = redmine.version.new()
   >>> version.project_id = 'vacation'
   >>> version.name = 'Vacation'
   >>> version.status = 'open'
   >>> version.sharing = 'none'
   >>> version.due_date = datetime.date(2014, 1, 30)
   >>> version.description = 'my vacation'
   >>> version.wiki_page_title = 'Vacation'
   >>> version.save()
   True

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Version resource from Redmine by it's id.

   :param int resource_id: (required). Id of the version.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> version = redmine.version.get(1)
   >>> version
   <redminelib.resources.Version #1 "Release 1">

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Version resources that match the given lookup parameters.

   :param project_id: (required). Id or identifier of version's project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> versions = redmine.version.filter(project_id='vacation')
   >>> versions
   <redminelib.resultsets.ResourceSet object with Versions resources>

.. hint::

   You can also get versions from a Project resource object directly using ``versions`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.versions
      <redminelib.resultsets.ResourceSet object with Version resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Version resource and saves them to the Redmine.

   :param int resource_id: (required). Version id.
   :param string name: (optional). Version name.
   :param string status:
    .. raw:: html

       (optional). Status of the version, one of:

    - open (default)
    - locked
    - closed

   :param string sharing:
    .. raw:: html

       (optional). Version sharing, one of:

    - none (default)
    - descendants
    - hierarchy
    - tree
    - system

   :param due_date: (optional). Expiration date.
   :type due_date: string or date object
   :param string description: (optional). Version description.
   :param string wiki_page_title: (optional). Version wiki page title.
   :return: True

.. code-block:: python

   >>> redmine.version.update(
   ...     1,
   ...     name='Vacation',
   ...     status='open',
   ...     sharing='none',
   ...     due_date=datetime.date(2014, 1, 30),
   ...     description='my vacation',
   ...     wiki_page_title='Vacation'
   ... )
   True

save
++++

.. py:method:: save()
   :module: redminelib.resources.Version
   :noindex:

   Saves the current state of a Version resource to the Redmine. Fields that can
   be changed are the same as for ``update()`` method above.

   :return: True

.. code-block:: python

   >>> version = redmine.version.get(1)
   >>> version.name = 'Vacation'
   >>> version.status = 'open'
   >>> version.sharing = 'none'
   >>> version.due_date = datetime.date(2014, 1, 30)
   >>> version.description = 'my vacation'
   >>> version.wiki_page_title = 'Vacation'
   >>> version.save()
   True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Version resource from Redmine by it's id.

   :param int resource_id: (required). Version id.
   :return: True

.. code-block:: python

   >>> redmine.version.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.Version
   :noindex:

   Deletes current Version resource object from Redmine.

   :return: True

.. code-block:: python

   >>> version = redmine.version.get(1)
   >>> version.delete()
   True

Export
------

Not supported by Redmine
