Operations
==========

Now when you have configured your Redmine object, you can start making operations on the Redmine.
Redmine has a conception of resources, i.e. resource is an entity which can be used in Redmine's
REST API. All operations on the resources are provided by the ResourceManager object which you
usually don't have to use directly. Not all resources support every operation, if resource doesn't
support the requested operation, an exception will be thrown.

Create
------

Not yet supported by Python Redmine

Read
----

Python Redmine provides 3 read operation methods: ``get``, ``all`` and ``filter``. Each
of this methods support different keyword arguments depending on the resource used and
method called. You can read more about it in each resource's documentation.

Get
+++

Returns requested Resource object either by integer ``id`` or by string ``identifier``:

.. code-block:: python

    >>> redmine = Redmine('http://demo.redmine.org')
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

All
+++

Returns a ResourceSet object that contains all the requested Resource objects:

.. code-block:: python

    >>> redmine = Redmine('http://demo.redmine.org')
    >>> projects = redmine.project.all()
    >>> projects
    <redmine.resultsets.ResourceSet object with Project resources>

Filter
++++++

Returns a ResourceSet object that contains Resource objects filtered by some condition(s):

.. code-block:: python

    >>> redmine = Redmine('http://demo.redmine.org')
    >>> issues = redmine.issue.filter(project_id='vacation')
    >>> issues
    <redmine.resultsets.ResourceSet object with Issue resources>

.. hint::

    ResourceSet object supports limit and offset, i.e. if you need to get only some portion
    of Resource objects, in the form of ``[offset:limit]`` or as keyword arguments:

    .. code-block:: python

        redmine.project.all()[:135]  # Returns only the first 135 resources
        redmine.project.all(limit=135)  # Returns only the first 135 resources
        redmine.issue.filter(project_id='vacation')[10:3]  # Returns only 3 issues starting from 10th
        redmine.issue.filter(project_id='vacation', offset=10, limit=3)  # Returns only 3 issues starting from 10th

.. hint::

    ResourceSet object provides 2 helper methods ``get`` and ``filter``:

    * **get**. Returns a single resource from the ResourceSet by integer id.

      .. code-block:: python

            redmine.project.all().get(30404)

    * **filter**. Returns a ResourceSet with requested resource ids.

      .. code-block:: python

            redmine.project.all().filter((30404, 30405, 30406, 30407))

.. note::

    ResourceSet object is lazy, i.e. it doesn't make any requests to Redmine when it is created
    and is evaluated only when some of these conditions are met:

    * **Iteration**. A ResourceSet is iterable and it is evaluated when you iterate over it.

      .. code-block:: python

            for project in redmine.project.all():
                print(project.name)

    * **len()**. A ResourceSet is evaluated when you call len() on it and returns the length of the list.

      .. code-block:: python

            length = len(redmine.project.all())

    * **list()**. Force evaluation of a ResourceSet by calling list() on it.

      .. code-block:: python

            projects = list(redmine.project.all())

    * **Index**. A ResourceSet is also evaluated when you request some of it's Resources by index.

      .. code-block:: python

            redmine.project.all()[0]  # Returns the first Resource in the ResourceSet

Update
------

Not yet supported by Python Redmine

Delete
------

Not yet supported by Python Redmine
