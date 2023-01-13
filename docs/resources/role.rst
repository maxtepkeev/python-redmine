Role
====

Supported by Redmine starting from version 1.4

Manager
-------

All operations on the Role resource are provided by its manager. To get access to
it you have to call ``redmine.role`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Role resource from Redmine by its id.

   :param int resource_id: (required). Id of the role.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> role = redmine.role.get(4)
   >>> role
   <redminelib.resources.Role #4 "Waiter">

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Role resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> roles = redmine.role.all()
   >>> roles
   <redminelib.resultsets.ResourceSet object with Role resources>

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
