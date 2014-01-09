Issue Category
==============

Supported by Redmine starting from version 1.3

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

Not yet supported by Python Redmine
