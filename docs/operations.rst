Operations
==========

Now when you have configured your Redmine object, you can start making operations on the Redmine.
Redmine has a conception of resources, i.e. resource is an entity which can be used in Redmine's
REST API. All operations on the resources are provided by the ResourceManager object which you
usually don't have to use directly. Not all resources support every operation, if resource doesn't
support the requested operation, an exception will be thrown.

Create
------

Python Redmine provides 2 create operation methods: ``create`` and ``new``. Unfortunately Redmine
doesn't support the creation of some resources via REST API. You can read more about it in each
resource's documentation.

create
++++++

Creates new resource with given fields and saves it to the Redmine.

.. code-block:: python

    >>> project = redmine.project.create(name='Vacation', identifier='vacation', description='foo', homepage='http://foo.bar', is_public=True, parent_id=345, inherit_members=True, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    >>> project
    <redmine.resources.Project #123 "Vacation">

new
+++

Creates new empty resource but doesn't save it to the Redmine. This is useful if you want to
set some resource fields later based on some condition(s) and only after that save it to the
Redmine.

.. code-block:: python

    >>> project = redmine.project.new()
    >>> project.name = 'Vacation'
    >>> project.identifier = 'vacation'
    >>> project.description = 'foo'
    >>> project.homepage = 'http://foo.bar'
    >>> project.is_public = True
    >>> project.parent_id = 345
    >>> project.inherit_members = True
    >>> project.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> project.save()
    True

Read
----

Python Redmine provides 3 read operation methods: ``get``, ``all`` and ``filter``. Each
of this methods support different keyword arguments depending on the resource used and
method called. You can read more about it in each resource's documentation.

get
+++

Returns requested Resource object either by integer ``id`` or by string ``identifier``:

.. code-block:: python

    >>> project = redmine.project.get('vacation')
    >>> project.name
    'Vacation'
    >>> project['name']  # You can access Resource attributes this way too
    'Vacation'
    >>> project = redmine.project.get(30404)
    >>> project.name
    'Vacation'

.. note::

    Resource object provides 2 ways to introspect itself:

    * **dir()**. Returns all the attributes Resource has as a list.

      .. code-block:: python

            dir(redmine.project.get('vacation'))

    * **list()**. Returns all the attributes with it's values Resource has as a list of tuples.

      .. code-block:: python

            list(redmine.project.get('vacation'))

.. hint::

    Under some circumstances Redmine doesn't return all the data about Resource, fortunately
    Resource object provides a convenient refresh() method which will get all the available data:

    .. code-block:: python

        redmine.project.get('vacation').refresh()

all
+++

Returns a ResourceSet object that contains all the requested Resource objects:

.. code-block:: python

    >>> projects = redmine.project.all()
    >>> projects
    <redmine.resultsets.ResourceSet object with Project resources>

filter
++++++

Returns a ResourceSet object that contains Resource objects filtered by some condition(s):

.. code-block:: python

    >>> issues = redmine.issue.filter(project_id='vacation')
    >>> issues
    <redmine.resultsets.ResourceSet object with Issue resources>

.. hint::

    ResourceSet object supports limit and offset, i.e. if you need to get only some portion
    of Resource objects, in the form of ``[offset:limit]`` or as keyword arguments:

    .. code-block:: python

        redmine.project.all()[:135]  # Returns only the first 135 projects
        redmine.project.all(limit=135)  # Returns only the first 135 projects
        redmine.issue.filter(project_id='vacation')[10:3]  # Returns only 3 issues starting from 10th
        redmine.issue.filter(project_id='vacation', offset=10, limit=3)  # Returns only 3 issues starting from 10th

    Please note, that keyword arguments have a higher priority, e.g.:

    .. code-block:: python

        redmine.project.all(limit=10)[:20]  # Returns 10 projects and not 20

.. hint::

    ResourceSet object provides 2 helper methods ``get()`` and ``filter()``:

    * **get**. Returns a single resource from the ResourceSet by integer id.

      .. code-block:: python

            redmine.project.all().get(30404)

    * **filter**. Returns a ResourceSet with requested resource ids.

      .. code-block:: python

            redmine.project.all().filter((30404, 30405, 30406, 30407))

    ResourceSet object also provides some attributes:

    * **limit**. What limit value was used to retrieve this ResourceSet.

      .. code-block:: python

            redmine.project.all().limit

    * **offset**. What offset value was used to retrieve this ResourceSet.

      .. code-block:: python

            redmine.project.all().offset

    * **total_count**. How much resources of current resource type there are available in
      Redmine.

      .. code-block:: python

            redmine.project.all().total_count

.. note::

    ResourceSet object is lazy, i.e. it doesn't make any requests to Redmine when it is created
    and is evaluated only when some of these conditions are met:

    * **Iteration**. A ResourceSet is iterable and it is evaluated when you iterate over it.

      .. code-block:: python

            for project in redmine.project.all():
                print(project.name)

    * **len()**. A ResourceSet is evaluated when you call len() on it and returns the length of the list.

      .. code-block:: python

            len(redmine.project.all())

    * **list()**. Force evaluation of a ResourceSet by calling list() on it.

      .. code-block:: python

            list(redmine.project.all())

    * **Index**. A ResourceSet is also evaluated when you request some of it's Resources by index.

      .. code-block:: python

            redmine.project.all()[0]  # Returns the first Resource in the ResourceSet

Update
------

Python Redmine provides 2 update operation methods: ``update`` and ``save``. Unfortunately Redmine
doesn't support updates on some resources via REST API. You can read more about it in each
resource's documentation.

update
++++++

Updates a resource with given fields and saves it to the Redmine.

.. code-block:: python

    >>> redmine.project.update(1, name='Vacation', description='foo', homepage='http://foo.bar', is_public=True, parent_id=345, inherit_members=True, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    True

save
++++

Saves the current state of a resource to the Redmine.

.. code-block:: python

    >>> project = redmine.project.get(1)
    >>> project.name = 'Vacation'
    >>> project.description = 'foo'
    >>> project.homepage = 'http://foo.bar'
    >>> project.is_public = True
    >>> project.parent_id = 345
    >>> project.inherit_members = True
    >>> project.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> project.save()
    True

Delete
------

Resources can be deleted via ``delete`` method. Unfortunately Redmine doesn't support the deletion
of some resources via REST API. You can read more about it in each resource's documentation.

.. code-block:: python

    >>> redmine.project.delete(1)
    True

.. warning::

    Deleted resources can't be restored. Use this method carefully.
