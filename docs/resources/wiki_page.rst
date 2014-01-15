Wiki Page
=========

Supported by Redmine starting from version 2.2

Create
------

Supported keyword arguments:

* **project_id** (required). Create wiki page in the given project id.
* **title** (required). Title of the wiki page.
* **text** (required): Text of the wiki page.
* **comments** (optional). Comments of the wiki page.

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.create(project_id='vacation', title='FooBar', text='foo', comments='bar')
    >>> wiki_page
    <redmine.resources.WikiPage "FooBar">

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **project_id**. Get wiki page from the project with the given id, where id is either
  project id or project identifier.
* **include**. Can be used to fetch associated data in one call. Accepted values (separated by comma):

  - attachments

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
