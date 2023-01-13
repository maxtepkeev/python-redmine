Group
=====

Supported by Redmine starting from version 2.1

Manager
-------

All operations on the Group resource are provided by its manager. To get access to it
you have to call ``redmine.group`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Group resource with given fields and saves it to the Redmine.

   :param string name: (required). Group name.
   :param list user_ids: (optional). Ids of users who will be members of a group.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> group = redmine.group.create(name='Developers', user_ids=[13, 15, 25])
   >>> group
   <redminelib.resources.Group #8 "Developers">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Group resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> group = redmine.group.new()
   >>> group.name = 'Developers'
   >>> group.user_ids = [13, 15, 25]
   >>> group.save()
   <redminelib.resources.Group #8 "Developers">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single group resource from Redmine by its id.

   :param int resource_id: (required). Id of the group.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - memberships
    - users

   :return: :ref:`Resource` object

.. code-block:: python

   >>> group = redmine.group.get(524, include=['memberships', 'users'])
   >>> group
   <redminelib.resources.Group #524 "DESIGN">

.. hint::

    Group resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Group
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get()`` method with
    ``include`` keyword argument. On demand includes provided by the Group resource object
    are the same as in the ``get()`` method above:

    .. code-block:: python

       >>> group = redmine.group.get(524)
       >>> group.users
       <redminelib.resultsets.ResourceSet object with User resources>

all
+++

.. py:method:: all()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Group resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> groups = redmine.group.all()
   >>> groups
   <redminelib.resultsets.ResourceSet object with Group resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Group resource and saves them to the Redmine.

   :param int resource_id: (required). Group id.
   :param string name: (optional). Group name.
   :param list user_ids: (optional). Ids of users who will be members of a group.
   :return: True

.. code-block:: python

   >>> redmine.group.update(1, name='Developers', user_ids=[13, 15, 25])
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Group
   :noindex:

   Saves current state of a Group resource to the Redmine. Attrs that can be
   changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> group = redmine.group.get(1)
   >>> group.name = 'Developers'
   >>> group.user_ids = [13, 15, 25]
   >>> group.save()
   <redminelib.resources.Group #1 "Developers">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> group = redmine.group.get(1).save(
   ...     name='Developers',
   ...     user_ids=[13, 15, 25]
   ... )
   >>> group
   <redminelib.resources.Group #1 "Developers">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Group resource from Redmine by its id.

   :param int resource_id: (required). Group id.
   :return: True

.. code-block:: python

   >>> redmine.group.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.Group
   :noindex:

   Deletes current Group resource object from Redmine.

   :return: True

.. code-block:: python

   >>> group = redmine.group.get(1)
   >>> group.delete()
   True

Export
------

Not supported by Redmine

Users
-----

Python-Redmine provides 2 methods to work with group users:

add
+++

.. py:method:: add(user_id)
   :module: redminelib.resources.Group.User
   :noindex:

   Adds a user to a group by its id.

   :param int user_id: (required). User id.
   :return: True

.. code-block:: python

   >>> group = redmine.group.get(1)
   >>> group.user.add(1)
   True

remove
++++++

.. py:method:: remove(user_id)
   :module: redminelib.resources.Group.User
   :noindex:

   Removes a user from a group by its id.

   :param int user_id: (required). User id.
   :return: True

.. code-block:: python

   >>> group = redmine.group.get(1)
   >>> group.user.remove(1)
   True
