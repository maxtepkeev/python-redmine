Tracker
=======

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the tracker resource are provided via it's manager. To get access to
it you have to call ``redmine.tracker`` where ``redmine`` is a configured redmine object.
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

.. py:method:: all()
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all tracker resources from the Redmine.

    :return: ResourceSet object

.. code-block:: python

    >>> trackers = redmine.tracker.all()
    >>> trackers
    <redmine.resultsets.ResourceSet object with Tracker resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
