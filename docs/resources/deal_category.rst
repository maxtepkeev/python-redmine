Deal Category
=============

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ of version 3.3.0 and higher is installed.

Manager
-------

All operations on the deal category resource are provided via it's manager. To get access to
it you have to call ``redmine.deal_category`` where ``redmine`` is a configured redmine object.
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

    Returns deal category resources that match the given lookup parameters.

    :param project_id: (required). Id or identifier of deal category's project.
    :type project_id: integer or string
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> categories = redmine.deal_category.filter(project_id='vacation')
    >>> categories
    <redmine.resultsets.ResourceSet object with DealCategory resources>

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin
