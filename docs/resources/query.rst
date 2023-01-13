Query
=====

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the Query resource are provided by its manager. To get access to
it you have to call ``redmine.query`` where ``redmine`` is a configured redmine object.
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

   Returns single Query resource from Redmine by its id.

   :param int resource_id: (required). Id of the query.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> query = redmine.query.get(654)
   >>> query
   <redminelib.resources.Query #654 "Done">

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Query resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> queries = redmine.query.all(offset=10, limit=100)
   >>> queries
   <redminelib.resultsets.ResourceSet object with Query resources>

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
