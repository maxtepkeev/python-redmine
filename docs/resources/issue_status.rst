Issue Status
============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the issue status resource are provided via it's manager. To get access to
it you have to call ``redmine.issue_status`` where ``redmine`` is a configured redmine object.
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

    Returns all issue status resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> statuses = redmine.issue_status.all()
    >>> statuses
    <redmine.resultsets.ResourceSet object with IssueStatus resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
