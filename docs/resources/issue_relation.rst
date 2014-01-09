Issue Relation
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

Not yet supported by Python Redmine
