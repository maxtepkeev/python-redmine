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
    :param user_ids: (optional). Ids of users to add to a group.
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

Not yet supported by Python Redmine

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
