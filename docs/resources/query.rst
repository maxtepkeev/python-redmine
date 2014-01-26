Query
=====

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the query resource are provided via it's manager. To get access to
it you have to call ``redmine.query`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

Not supported by Redmine

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all query resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> queries = redmine.query.all(offset=10, limit=100)
    >>> queries
    <redmine.resultsets.ResourceSet object with Query resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
