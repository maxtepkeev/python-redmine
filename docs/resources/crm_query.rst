CRM Query
=========

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ 3.3.0 and higher is installed.

Manager
-------

All operations on the crm query resource are provided via it's manager. To get access to
it you have to call ``redmine.crm_query`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by CRM plugin

Read methods
------------

get
+++

Not supported by CRM plugin

all
+++

Not supported by CRM plugin

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns crm query resources that match the given lookup parameters.

    :param string resource:
      .. raw:: html

          (required). Get crm queries for the requested resource. Available resources are:

      - contact
      - deal

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> queries = redmine.crm_query.filter(resource='contact')
    >>> queries
    <redmine.resultsets.ResourceSet object with CrmQuery resources>

.. hint::

    CrmQuery resource object provides you with some relations. Relations are the other
    resource objects wrapped in a ResourceSet which are somehow related to a CrmQuery
    resource object. The relations provided by the CrmQuery resource object are:

    * deals

    .. code-block:: python

        >>> queries = redmine.crm_query.filter(resource='deal')
        >>> queries[0]
         <redmine.resources.CrmQuery #10 "Deals by category">
        >>> queries[0].deals
        <redmine.resultsets.ResourceSet object with Deal resources>

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin
