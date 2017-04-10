Enumeration
===========

Supported by Redmine starting from version 2.2

Manager
-------

All operations on the Enumeration resource are provided by it's manager. To get access to
it you have to call ``redmine.enumeration`` where ``redmine`` is a configured redmine object.
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

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Enumeration resources that match the given lookup parameters.

   :param string resource:
    .. raw:: html

       (required). Get enumerations for the resource. One of:

    - issue_priorities
    - time_entry_activities
    - document_categories

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> enumerations = redmine.enumeration.filter(resource='time_entry_activities')
   >>> enumerations
   <redminelib.resultsets.ResourceSet object with Enumeration resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine

Export
------

Not supported by Redmine
