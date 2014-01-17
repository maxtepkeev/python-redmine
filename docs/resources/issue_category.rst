Issue Category
==============

Supported by Redmine starting from version 1.3

Create
------

Supported keyword arguments:

* **project_id** (required). The id of the project, where id is either project id or project identifier.
* **name** (required). Name of issue category.
* **assigned_to_id** (optional). The id of the user assigned to the category (new issues with this category
  will be assigned by default to this user).

.. code-block:: python

    >>> category = redmine.issue_category.create(project_id='vacation', name='woohoo', assigned_to_id=13)
    >>> category
    <redmine.resources.IssueCategory #810 "woohoo">

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> category = redmine.issue_category.get(794)
    >>> category
    <redmine.resources.IssueCategory #794 "Malibu">


All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments: None

Supported filters:

* **project_id**. Get issue categories from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> categories = redmine.issue_category.filter(project_id='vacation')
    >>> categories
    <redmine.resultsets.ResourceSet object with IssueCategory resources>

.. hint::

    You can also get issue categories from a project resource object directly using
    ``issue_categories`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.issue_categories
        <redmine.resultsets.ResourceSet object with IssueCategory resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Supported keyword arguments:

* **reassign_to_id** (optional). When there are issues assigned to the category you are
  deleting, this parameter lets you reassign these issues to the category with given id

.. code-block:: python

    >>> redmine.issue_category.delete(1, reassign_to_id=2)
    >>> True
