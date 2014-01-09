Query
=====

Supported by Redmine starting from version 1.3

Create
------

Not supported by Redmine

Read
----

Methods
~~~~~~~

Get
+++

Not supported by Redmine

All
+++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

.. code-block:: python

    >>> queries = redmine.query.all(offset=10, limit=100)
    >>> queries
    <redmine.resultsets.ResourceSet object with Query resources>

Filter
++++++

Not supported by Redmine

Update
------

Not supported by Redmine

Delete
------

Not supported by Redmine
