News
====

Supported by Redmine starting from version 1.1

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

    >>> news = redmine.news.all(offset=10, limit=100)
    >>> news
    <redmine.resultsets.ResourceSet object with News resources>

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **project_id**. Get issues from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> news = redmine.news.filter(project_id='vacation')
    >>> news
    <redmine.resultsets.ResourceSet object with News resources>

.. hint::

    You can also get news from a project resource object directly using ``news`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.news
        <redmine.resultsets.ResourceSet object with News resources>

Update
------

Not supported by Redmine

Delete
------

Not supported by Redmine
