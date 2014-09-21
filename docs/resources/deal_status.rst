Deal Status
===========

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ 3.3.0 and higher is installed.

Manager
-------

All operations on the deal status resource are provided via it's manager. To get access to
it you have to call ``redmine.deal_status`` where ``redmine`` is a configured redmine object.
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

.. py:method:: all()
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all deal status resources from the CRM plugin.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> statuses = redmine.deal_status.all()
    >>> statuses
    <redmine.resultsets.ResourceSet object with DealStatus resources>

.. hint::

    DealStatus resource object provides you with some relations. Relations are the other
    resource objects wrapped in a ResourceSet which are somehow related to a DealStatus
    resource object. The relations provided by the DealStatus resource object are:

    * deals

    .. code-block:: python

        >>> statuses = redmine.deal_status.all()
        >>> statuses[0]
        <redmine.resources.DealStatus #1 "New">
        >>> statuses[0].deals
        <redmine.resultsets.ResourceSet object with Deal resources>

filter
++++++

Not supported by CRM plugin

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin
