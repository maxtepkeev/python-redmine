Wiki Page
=========

Supported by Redmine starting from version 2.2

Create
------

Not yet supported by Python Redmine

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **project_id**. Get wiki page from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.get('Photos', project_id='vacation')
    >>> wiki_page
    <redmine.resources.WikiPage "Photos">

All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments: None

Supported filters:

* **project_id**. Get wiki pages from the project with the given id, where id is either
  project id or project identifier.

.. code-block:: python

    >>> wiki_pages = redmine.wiki_page.filter(project_id='vacation')
    >>> wiki_pages
    <redmine.resultsets.ResourceSet object with WikiPage resources>

.. hint::

    You can also get wiki pages from a project resource object directly using
    ``wiki_pages`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.wiki_pages
        <redmine.resultsets.ResourceSet object with WikiPage resources>

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
