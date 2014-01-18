Issue Relation
==============

Supported by Redmine starting from version 1.3

Create
------

Supported keyword arguments:

* **issue_id** (required). Creates a relation for the issue of given id.
* **issue_to_id** (required). Id of the related issue.
* **relation_type** (required): Type of the relation, available values are:

  - relates
  - duplicates
  - duplicated
  - blocks
  - blocked
  - precedes
  - follows

* **delay** (optional). Delay in days for a "precedes" or "follows" relation.

.. code-block:: python

    >>> relation = redmine.issue_relation.create(issue_id=12345, issue_to_id=54321, relation_type='precedes', delay=5)
    >>> relation
    <redmine.resources.IssueRelation #667>

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> relation = redmine.issue_relation.get(606)
    >>> relation
    <redmine.resources.IssueRelation #606>

All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **issue_id**. Get relations from the issue with the given issue id.

.. code-block:: python

    >>> relations = redmine.issue_relation.filter(issue_id=6543)
    >>> relations
    <redmine.resultsets.ResourceSet object with IssueRelation resources>

.. hint::

    You can also get issue relations from an issue resource object directly using
    ``relations`` relation:

    .. code-block:: python

        >>> issue = redmine.issue.get(6543)
        >>> issue.relations
        <redmine.resultsets.ResourceSet object with IssueRelation resources>

Update
------

Not supported by Redmine

Delete
------

Supported keyword arguments: None

.. code-block:: python

    >>> redmine.issue_relation.delete(1)
    >>> True
