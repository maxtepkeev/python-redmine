CRM Query
=========

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the CrmQuery resource are provided by its manager. To get access to
it you have to call ``redmine.crm_query`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by CRM plugin

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single CrmQuery resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the crm query.
   :param string resource:
    .. raw:: html

       (required). Get crm query for the resource. One of:

    - contact
    - deal
    - invoice (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)
    - expense (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)

   :return: :ref:`Resource` object

.. code-block:: python

   >>> query = redmine.crm_query.get(1, resource='contact')
   >>> query
   <redminelib.resources.CrmQuery #1 "By companies">

.. hint::

   CrmQuery resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to a CrmQuery
   resource object. The relations provided by the CrmQuery resource object are:

   * deals
   * contacts
   * invoices (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)
   * expenses (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)

   .. code-block:: python

      >>> queries = redmine.crm_query.filter(resource='deal')
      >>> queries[0]
      <redminelib.resources.CrmQuery #10 "Deals by category">
      >>> queries[0].deals
      <redminelib.resultsets.ResourceSet object with Deal resources>

all
+++

Not supported by CRM plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns crm query resources that match the given lookup parameters.

   :param string resource:
    .. raw:: html

       (required). Get crm queries for the resource. One of:

    - contact
    - deal
    - invoice (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)
    - expense (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3)

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> queries = redmine.crm_query.filter(resource='contact')
   >>> queries
   <redminelib.resultsets.ResourceSet object with CrmQuery resources>

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin

Export
------

Not supported by CRM plugin
