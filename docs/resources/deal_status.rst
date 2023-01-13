Deal Status
===========

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the DealStatus resource are provided by its manager. To get access to
it you have to call ``redmine.deal_status`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by CRM plugin

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single DealStatus resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the deal status.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> status = redmine.deal_status.get(1)
   >>> status
   <redminelib.resources.DealStatus #1 "Lost">

.. hint::

   DealStatus resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to a DealStatus
   resource object. The relations provided by the DealStatus resource object are:

   * deals

   .. code-block:: python

      >>> statuses = redmine.deal_status.all()
      >>> statuses[0]
      <redminelib.resources.DealStatus #1 "New">
      >>> statuses[0].deals
      <redminelib.resultsets.ResourceSet object with Deal resources>

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all DealStatus resources from the CRM plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> statuses = redmine.deal_status.all()
   >>> statuses
   <redminelib.resultsets.ResourceSet object with DealStatus resources>

filter
++++++

Not supported by CRM plugin

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin

Export
------

Not supported by CRM plugin
