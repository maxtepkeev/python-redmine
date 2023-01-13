Tracker
=======

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the Tracker resource are provided by its manager. To get access to
it you have to call ``redmine.tracker`` where ``redmine`` is a configured redmine object.
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

   Returns single Tracker resource from Redmine by its id.

   :param int resource_id: (required). Id of the tracker.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> tracker = redmine.tracker.get(1)
   >>> tracker
   <redminelib.resources.Tracker #1 "Task">

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Tracker resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> trackers = redmine.tracker.all()
   >>> trackers
   <redminelib.resultsets.ResourceSet object with Tracker resources>

.. hint::

   Tracker resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to a Tracker
   resource object. The relations provided by the Tracker resource object are:

   * issues

   .. code-block:: python

      >>> trackers = redmine.tracker.all()
      >>> trackers[0]
      <redminelib.resources.Tracker #1 "FooBar">
      >>> trackers[0].issues
      <redminelib.resultsets.ResourceSet object with Issue resources>

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
