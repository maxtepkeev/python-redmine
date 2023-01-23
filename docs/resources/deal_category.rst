Deal Category
=============

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the DealCategory resource are provided by its manager. To get access to
it you have to call ``redmine.deal_category`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

.. versionadded:: 2.5.0

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new DealCategory resource with given fields and saves it to the CRM plugin.

   :param project_id: (required). Id or identifier of deal category's project.
   :type project_id: int or string
   :param string name: (required). Category name.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.deal_category.create(project_id='vacation', name='Integration')
   >>> category
   <redminelib.resources.DealCategory #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty DealCategory resource, but saves it to the CRM plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.deal_category.new()
   >>> category.project_id = 'vacation'
   >>> category.name = 'Integration'
   >>> category.save()
   <redminelib.resources.DealCategory #123>

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single DealCategory resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the deal category.
   :param project_id: (required). Id or identifier of deal category's project.
   :type project_id: int or string

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.deal_category.get(1, project_id='vacation')
   >>> category
   <redminelib.resources.DealCategory #1 "Design">

all
+++

Not supported by CRM plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns DealCategory resources that match the given lookup parameters.

   :param project_id: (required). Id or identifier of deal category's project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> categories = redmine.deal_category.filter(project_id='vacation')
   >>> categories
   <redminelib.resultsets.ResourceSet object with DealCategory resources>

.. hint::

   You can also get deal categories from a Project resource object directly using
   ``deal_categories`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.deal_categories
      <redminelib.resultsets.ResourceSet object with DealCategory resources>

Update methods
--------------

.. versionadded:: 2.5.0

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a DealCategory resource and saves them to the CRM plugin.

   :param int resource_id: (required). Category id.
   :param string name: (required). Category name.
   :return: True

.. code-block:: python

   >>> redmine.deal_category.update(123, name='Software')
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.DealCategory
   :noindex:

   Saves the current state of a DealCategory resource to the CRM plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.deal_category.get(123)
   >>> category.name = 'Software'
   >>> category.save()
   <redminelib.resources.DealCategory #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> category = redmine.deal_category.get(123).save(name='Software')
   >>> category
   <redminelib.resources.DealCategory #123>

Delete methods
--------------

.. versionadded:: 2.5.0

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single DealCategory resource from the CRM plugin by its id.

   :param int resource_id: (required). Category id.
   :return: True

.. code-block:: python

   >>> redmine.deal_category.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.DealCategory
   :noindex:

   Deletes current DealCategory resource object from the CRM plugin.

   :return: True

.. code-block:: python

   >>> category = redmine.deal_category.get(1)
   >>> category.delete()
   True

Export
------

Not supported by CRM plugin
