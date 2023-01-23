Order Status
============

.. versionadded:: 2.5.0

Requires Pro Edition and `Products plugin <https://www.redmineup.com/pages/plugins/products>`_ >= 2.1.5.

Manager
-------

All operations on the OrderStatus resource are provided by its manager. To get access to
it you have to call ``redmine.order_status`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Products plugin

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single OrderStatus resource from the Products plugin by its id.

   :param int resource_id: (required). Id of the order status.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> status = redmine.order_status.get(1)
   >>> status
   <redminelib.resources.OrderStatus #1 "Paid">

.. hint::

   OrderStatus resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to an OrderStatus
   resource object. The relations provided by the OrderStatus resource object are:

   * orders

   .. code-block:: python

      >>> statuses = redmine.order_status.all()
      >>> statuses[0]
      <redminelib.resources.OrderStatus #1 "Paid">
      >>> statuses[0].orders
      <redminelib.resultsets.ResourceSet object with Order resources>

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all OrderStatus resources from the Products plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> statuses = redmine.order_status.all()
   >>> statuses
   <redminelib.resultsets.ResourceSet object with OrderStatus resources>

filter
++++++

Not supported by Products plugin

Update methods
--------------

Not supported by Products plugin

Delete methods
--------------

Not supported by Products plugin

Export
------

Not supported by Products plugin
