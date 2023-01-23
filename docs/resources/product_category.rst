Product Category
================

.. versionadded:: 2.5.0

Requires Pro Edition and `Products plugin <https://www.redmineup.com/pages/plugins/products>`_ >= 2.1.5.

Manager
-------

All operations on the ProductCategory resource are provided by its manager. To get access to it
you have to call ``redmine.product_category`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new ProductCategory resource with given fields and saves it to the Products plugin.

   :param string name: (required). Category name.
   :param string code: (optional). Category code.
   :param int parent_id: (optional). Category parent id.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.product_category.create(
   ...     name='Software',
   ...     code='S-001',
   ...     parent_id=13
   ... )
   >>> category
   <redminelib.resources.ProductCategory #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty ProductCategory resource, but saves it to the Products plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.product_category.new()
   >>> category.name = 'Software'
   >>> category.code = 'S-001'
   >>> category.parent_id = 13
   >>> category.save()
   <redminelib.resources.ProductCategory #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single ProductCategory resource from the Products plugin by its id.

   :param int resource_id: (required). Id of the product category.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.product_category.get(123)
   >>> category
   <redminelib.resources.ProductCategory #123>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all ProductCategory resources from the Products plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> categories = redmine.product_category.all(limit=50)
   >>> categories
   <redminelib.resultsets.ResourceSet object with ProductCategory resources>

filter
++++++

Not supported by Products plugin

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a ProductCategory resource and saves them to the Products plugin.

   :param int resource_id: (required). Category id.
   :param string name: (optional). Category name.
   :param string code: (optional). Category code.
   :param int parent_id: (optional). Category parent id.
   :return: True

.. code-block:: python

   >>> redmine.product_category.update(
   ...     123,
   ...     name='Software',
   ...     code='S-001',
   ...     parent_id=13
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.ProductCategory
   :noindex:

   Saves the current state of a ProductCategory resource to the Products plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.product_category.get(123)
   >>> category.name = 'Software'
   >>> category.code = 'S-001'
   >>> category.parent_id = 13
   >>> category.save()
   <redminelib.resources.ProductCategory #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> category = redmine.product_category.get(123).save(
   ...     name='Software',
   ...     code='S-001',
   ...     parent_id=13
   ... )
   >>> category
   <redminelib.resources.ProductCategory #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single ProductCategory resource from the Products plugin by its id.

   :param int resource_id: (required). Category id.
   :return: True

.. code-block:: python

   >>> redmine.product_category.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.ProductCategory
   :noindex:

   Deletes current ProductCategory resource object from the Products plugin.

   :return: True

.. code-block:: python

   >>> category = redmine.product_category.get(1)
   >>> category.delete()
   True

Export
------

Not supported by Products plugin
