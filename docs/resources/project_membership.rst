Project Membership
==================

Supported by Redmine starting from version 1.4

Create
------

Not yet supported by Python Redmine

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> membership = redmine.project_membership.get(521)
    >>> membership
    <redmine.resources.ProjectMembership #521>
    >>> dir(membership)
    ['id', 'project', 'roles', 'user']
    >>> membership.user.name
    'John Smith'

All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **project_id**. Get issues from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> memberships = redmine.project_membership.filter(project_id='vacation')
    >>> memberships
    <redmine.resultsets.ResourceSet object with ProjectMembership resources>

.. hint::

    You can also get project memberships from a project resource object directly using
    ``memberships`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.memberships
        <redmine.resultsets.ResourceSet object with ProjectMembership resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
