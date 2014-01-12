User
====

Supported by Redmine starting from version 1.1

Create
------

Supported keyword arguments:

* **login** (required). User login.
* **password** (optional). User password.
* **firstname** (required).
* **lastname** (required).
* **mail** (required).
* **auth_source_id** (optional). Authentication mode id.

.. code-block:: python

    >>> user = redmine.user.create(login='jsmith', password='qwerty', firstname='John', lastname='Smith', mail='john@smith.com', auth_source_id=1)
    >>> user
    <redmine.resources.User #32 "John Smith">

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **include**. Can be used to fetch associated data in one call. Accepted values (separated by comma):

  - memberships
  - groups

.. code-block:: python

    >>> user = redmine.user.get(17, include='memberships,groups')
    >>> user
    <redmine.resources.User #17 "John Smith">

All
+++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

.. code-block:: python

    >>> users = redmine.user.all(offset=10, limit=100)
    >>> users
    <redmine.resultsets.ResourceSet object with User resources>

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **status**. Get only users with the given status. Available statuses are:

  - 0 - anonymous
  - 1 - active (default)
  - 2 - registered
  - 3 - locked

* **name**. Filter users on their login, firstname, lastname and mail. If the
  pattern contains a space, it will also return users whose firstname match the
  first word or lastname match the second word.
* **group_id**. Get only users who are members of the given group.

.. code-block:: python

    >>> users = redmine.user.filter(offset=10, limit=100, status='3')
    >>> users
    <redmine.resultsets.ResourceSet object with User resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
