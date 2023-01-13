Custom Field
============

Supported by Redmine starting from version 2.4

Manager
-------

All operations on the CustomField resource are provided by its manager. To get access to
it you have to call ``redmine.custom_field`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single CustomField resource from Redmine by its id.

   :param int resource_id: (required). Id of the custom field.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> field = redmine.custom_field.get(1)
   >>> field
   <redminelib.resources.CustomField #1 "Vendor">

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all CustomField resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> fields = redmine.custom_field.all()
   >>> fields
   <redminelib.resultsets.ResourceSet object with CustomField resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine

Export
------

Not supported by Redmine
