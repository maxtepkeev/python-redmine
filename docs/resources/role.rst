Role
====

Supported by Redmine starting from version 1.4

Manager
-------

All operations on the role resource are provided via it's manager. To get access to
it you have to call ``redmine.role`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single role resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the role.
    :return: Role resource object

.. code-block:: python

    >>> role = redmine.role.get(4)
    >>> role
    <redmine.resources.Role #4 "Waiter">

all
+++

.. py:method:: all()
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all role resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> roles = redmine.role.all()
    >>> roles
    <redmine.resultsets.ResourceSet object with Role resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
