Contact Tag
===========

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ of version 3.3.1 and higher is installed.

Manager
-------

All operations on the contact tag resource are provided via it's manager. To get access to
it you have to call ``redmine.contact_tag`` where ``redmine`` is a configured redmine object.
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

    Returns all contact tag resources from the CRM plugin.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> tags = redmine.contact_tag.all()
    >>> tags
    <redmine.resultsets.ResourceSet object with ContactTag resources>

filter
++++++

Not supported by CRM plugin

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin
