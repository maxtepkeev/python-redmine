Custom Field
============

Supported by Redmine starting from version 2.4

Manager
-------

All operations on the custom field resource are provided via it's manager. To get access to
it you have to call ``redmine.custom_field`` where ``redmine`` is a configured redmine object.
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

    Returns all custom field resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> fields = redmine.custom_field.all()
    >>> fields
    <redmine.resultsets.ResourceSet object with CustomField resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
