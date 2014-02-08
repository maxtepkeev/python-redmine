User
====

Supported by Redmine starting from version 1.1

Manager
-------

All operations on the user resource are provided via it's manager. To get access
to it you have to call ``redmine.user`` where ``redmine`` is a configured redmine
object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new user resource with given fields and saves it to the Redmine.

    :param string login: (required). User login.
    :param string password: (optional). User password.
    :param string firstname: (required). User name.
    :param string lastname: (required). User surname.
    :param string mail: (required). User email.
    :param integer auth_source_id: (optional). Authentication mode id.
    :return: User resource object

.. code-block:: python

    >>> user = redmine.user.create(login='jsmith', password='qwerty', firstname='John', lastname='Smith', mail='john@smith.com', auth_source_id=1)
    >>> user
    <redmine.resources.User #32 "John Smith">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty user resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: User resource object

.. code-block:: python

    >>> user = redmine.user.new()
    >>> user.login = 'jsmith'
    >>> user.password = 'qwerty'
    >>> user.firstname = 'John
    >>> user.lastname = 'Smith'
    >>> user.mail = 'john@smith.com'
    >>> user.auth_source_id = 1
    >>> user.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single user resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the user.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - memberships
      - groups

    :return: User resource object

.. code-block:: python

    >>> user = redmine.user.get(17, include='memberships,groups')
    >>> user
    <redmine.resources.User #17 "John Smith">

.. hint::

    User resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a User
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the User resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> user = redmine.user.get(17)
        >>> user.groups
        <redmine.resultsets.ResourceSet object with Group resources>

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all user resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> users = redmine.user.all(offset=10, limit=100)
    >>> users
    <redmine.resultsets.ResourceSet object with User resources>

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns user resources that match the given lookup parameters.

    :param integer status:
      .. raw:: html

          (optional). Get only users with the given status. Available statuses are:

      - 0 - anonymous
      - 1 - active (default)
      - 2 - registered
      - 3 - locked

    :param string name: (optional). Filter users on their login, firstname, lastname and mail. If the
      pattern contains a space, it will also return users whose firstname match the
      first word or lastname match the second word.
    :param integer group_id: (optional). Get only users who are members of the given group.
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> users = redmine.user.filter(offset=10, limit=100, status=3)
    >>> users
    <redmine.resultsets.ResourceSet object with User resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a user resource and saves them to the Redmine.

    :param integer resource_id: (required). User id.
    :param string login: (optional). User login.
    :param string password: (optional). User password.
    :param string firstname: (optional). User name.
    :param string lastname: (optional). User surname.
    :param string mail: (optional). User email.
    :param integer auth_source_id: (optional). Authentication mode id.
    :return: True

.. code-block:: python

    >>> redmine.user.update(1, login='jsmith', password='qwerty', firstname='John', lastname='Smith', mail='john@smith.com', auth_source_id=1)
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.User
    :noindex:

    Saves the current state of a user resource to the Redmine. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> user = redmine.user.get(1)
    >>> user.login = 'jsmith'
    >>> user.password = 'qwerty'
    >>> user.firstname = 'John'
    >>> user.lastname = 'Smith'
    >>> user.mail = 'john@smith.com'
    >>> user.auth_source_id = 1
    >>> user.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single user resource from the Redmine by it's id.

    :param integer resource_id: (required). User id.
    :return: True

.. code-block:: python

    >>> redmine.user.delete(1)
    True
