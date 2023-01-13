Issue Status
============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the IssueStatus resource are provided by its manager. To get access to
it you have to call ``redmine.issue_status`` where ``redmine`` is a configured redmine object.
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

   Returns single IssueStatus resource from Redmine by its id.

   :param int resource_id: (required). Id of the issue status.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> status = redmine.issue_status.get(1)
   >>> status
   <redminelib.resources.IssueStatus #1 "Rejected">

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all IssueStatus resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> statuses = redmine.issue_status.all()
   >>> statuses
   <redminelib.resultsets.ResourceSet object with IssueStatus resources>

.. hint::

   IssueStatus resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to an IssueStatus
   resource object. The relations provided by the IssueStatus resource object are:

   * issues

   .. code-block:: python

      >>> statuses = redmine.issue_status.all()
      >>> statuses[0]
      <redminelib.resources.IssueStatus #1 "New">
      >>> statuses[0].issues
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
