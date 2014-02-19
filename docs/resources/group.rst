Group
=====

Supported by Redmine starting from version 2.1

Manager
-------

All operations on the group resource are provided via it's manager. To get access to it
you have to call ``redmine.group`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new group resource with given fields and saves it to the Redmine.

    :param string name: (required). Group name.
    :param user_ids: (optional). Ids of users who will be members of a group.
    :type user_ids: list or tuple
    :return: Group resource object

.. code-block:: python

    >>> group = redmine.group.create(name='Developers', user_ids=[13, 15, 25])
    >>> group
    <redmine.resources.Group #8 "Developers">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty group resource but doesn't save it to the Redmine. This is useful if
    you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: Group resource object

.. code-block:: python

    >>> group = redmine.group.new()
    >>> group.name = 'Developers'
    >>> group.user_ids = [13, 15, 25]
    >>> group.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single group resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the group.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - memberships
      - users

    :return: Group resource object

.. code-block:: python

    >>> group = redmine.group.get(524, include='memberships,users')
    >>> group
    <redmine.resources.Group #524 "DESIGN">

.. hint::

    .. versionadded:: 0.4.0

    Group resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a Group
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the Group resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> group = redmine.group.get(524)
        >>> group.users
        <redmine.resultsets.ResourceSet object with User resources>

all
+++

.. py:method:: all()
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all group resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> groups = redmine.group.all()
    >>> groups
    <redmine.resultsets.ResourceSet object with Group resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a group resource and saves them to the Redmine.

    :param integer resource_id: (required). Group id.
    :param string name: (optional). Group name.
    :param user_ids: (optional). Ids of users who will be members of a group.
    :type user_ids: list or tuple
    :return: True

.. code-block:: python

    >>> redmine.group.update(1, name='Developers', user_ids=[13, 15, 25])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Group
    :noindex:

    Saves the current state of a group resource to the Redmine. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> group = redmine.group.get(1)
    >>> group.name = 'Developers'
    >>> group.user_ids = [13, 15, 25]
    >>> group.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single group resource from the Redmine by it's id.

    :param integer resource_id: (required). Group id.
    :return: True

.. code-block:: python

    >>> redmine.group.delete(1)
    True

Users
-----

.. versionadded:: 0.5.0

Python Redmine provides 2 methods to work with group users: ``add`` and ``remove``.

add
+++

.. py:method:: add(user_id)
    :module: redmine.resources.Group.User
    :noindex:

    Adds a user to a group by it's id.

    :param integer user_id: (required). User id.
    :return: True

.. code-block:: python

    >>> group = redmine.group.get(1)
    >>> group.user.add(1)
    True

remove
++++++

.. py:method:: remove(user_id)
    :module: redmine.resources.Group.User
    :noindex:

    Removes a user from a group by it's id.

    :param integer user_id: (required). User id.
    :return: True

.. code-block:: python

    >>> group = redmine.group.get(1)
    >>> group.user.remove(1)
    True
