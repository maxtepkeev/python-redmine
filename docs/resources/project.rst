Project
=======

Supported by Redmine starting from version 1.0

Create
------

Supported keyword arguments:

* **name** (required). Project name.
* **identifier** (required). Project identifier.
* **description** (optional). Project description.
* **homepage** (optional). Project homepage url.
* **is_public** (optional). Whether project is public.
* **parent_id** (optional). Project's parent project id.
* **inherit_members** (optional). Whether project will inherit parent project's members.
* **custom_field_values** (optional). Value of custom fields as a dictionary in the form of {id: value}.

.. code-block:: python

    >>> project = redmine.project.create(name='Vacation', identifier='vacation', description='foo', homepage='http://foo.bar', is_public=True, parent_id=345, inherit_members=True, custom_field_values={2: 'foobar'})
    >>> project
    <redmine.resources.Project #123 "Vacation">

Read
----

Relations
~~~~~~~~~

Project resource object provides you with some relations. Relations are the other
resource objects wrapped in a ResourceSet which are somehow related to a Project
resource object. The relations provided by the Project resource object are:

* wiki_pages
* memberships
* issue_categories
* versions
* news
* issues

.. code-block:: python

    >>> project = redmine.project.get('vacation')
    >>> project.issues
    <redmine.resultsets.ResourceSet object with Issue resources>

Methods
~~~~~~~

Get
+++

Supported keyword arguments:

* **include**. Can be used to fetch associated data in one call. Accepted values (separated by comma):

  - trackers
  - issue_categories

.. code-block:: python

    >>> project = redmine.project.get('vacation', include='trackers,issue_categories')
    >>> project.name
    'Vacation'

All
+++

Supported keyword arguments:

* **limit**. How much Resource objects to return.
* **offset**. Starting from what object to return the other objects.

.. code-block:: python

    >>> projects = redmine.project.all(offset=10, limit=100)
    >>> projects
    <redmine.resultsets.ResourceSet object with Project resources>

Filter
++++++

Not supported by Redmine

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
