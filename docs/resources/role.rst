Role
====

Supported by Redmine starting from version 1.4

Create
------

Not supported by Redmine

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> role = redmine.role.get(4)
    >>> role
    <redmine.resources.Role #4 "Waiter">

All
+++

Supported keyword arguments: None

.. code-block:: python

    >>> roles = redmine.role.all()
    >>> roles
    <redmine.resultsets.ResourceSet object with Role resources>

Filter
++++++

Not supported by Redmine

Update
------

Not supported by Redmine

Delete
------

Not supported by Redmine
