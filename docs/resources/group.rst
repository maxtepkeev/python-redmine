Group
=====

Supported by Redmine starting from version 2.1

Create
------

Supported keyword arguments:

* **name** (required). Group name.
* **user_ids** (optional). Ids of users to add to a group as a list or tuple.

.. code-block:: python

    >>> group = redmine.group.create(name='Developers', user_ids=[13, 15, 25])
    >>> group
    <redmine.resources.Group #8 "Developers">

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **include**. Can be used to fetch associated data in one call. Accepted values (separated by comma):

  - memberships
  - users

.. code-block:: python

    >>> group = redmine.group.get(524, include='memberships,users')
    >>> group
    <redmine.resources.Group #524 "DESIGN">

All
+++

Supported keyword arguments: None

.. code-block:: python

    >>> groups = redmine.group.all()
    >>> groups
    <redmine.resultsets.ResourceSet object with Group resources>

Filter
++++++

Not supported by Redmine

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
