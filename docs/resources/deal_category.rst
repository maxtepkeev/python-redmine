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

Not supported by CRM plugin

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

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin

Export
------

Not supported by CRM plugin
