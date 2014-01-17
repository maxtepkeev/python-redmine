Version
=======

Supported by Redmine starting from version 1.3

Create
------

Supported keyword arguments:

* **project_id** (required). The id of the project, where id is either project id or project identifier.
* **name** (required). Version name.
* **status** (optional). Status of the version, available values are:

  - open (default)
  - locked
  - closed

* **sharing** (optional). Version sharing in, available values are:

  - none (default)
  - descendants
  - hierarchy
  - tree
  - system

* **due_date** (optional). Expiration date.
* **description** (optional). Version description.
* **wiki_page_title** (optional). Version wiki page title.

.. code-block:: python

    >>> version = redmine.version.create(project_id='vacation', name='Vacation', status='open', sharing='none', due_date='2014-01-30', description='my vacation', wiki_page_title='Vacation')
    >>> version
    <redmine.resources.Version #235 "Vacation">

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> version = redmine.version.get(1)
    >>> version
    <redmine.resources.Version #1 "Release 1">

All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

Supported filters:

* **project_id**. Get versions from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> versions = redmine.version.filter(project_id='vacation')
    >>> versions
    <redmine.resultsets.ResourceSet object with Versions resources>

.. hint::

    You can also get versions from a project resource object directly using
    ``versions`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.versions
        <redmine.resultsets.ResourceSet object with Version resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Supported keyword arguments: None

.. code-block:: python

    >>> redmine.version.delete(1)
    >>> True
