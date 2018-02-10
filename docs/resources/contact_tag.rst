Contact Tag
===========

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.4.0.

Manager
-------

All operations on the ContactTag resource are provided by it's manager. To get access to
it you have to call ``redmine.contact_tag`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by CRM plugin

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single ContactTag resource from the CRM plugin by it's id.

   :param int resource_id: (required). Id of the contact tag.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> tag = redmine.contact_tag.get(1)
   >>> tag
   <redminelib.resources.ContactTag #1 "Online">

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all ContactTag resources from the CRM plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> tags = redmine.contact_tag.all()
   >>> tags
   <redminelib.resultsets.ResourceSet object with ContactTag resources>

filter
++++++

Not supported by CRM plugin

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin

Export
------

Not supported by CRM plugin
