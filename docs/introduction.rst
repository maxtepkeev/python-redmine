Introduction
============

Now when you have configured your Redmine object, you can start making requests to Redmine. This
document contains an introduction to the most important information about concepts and objects used
in Python-Redmine, so it is recommended to read it carefully to understand how everything works.

.. _ResourceManager:

Operations
----------

Redmine has a concept of resources, i.e. a resource is an entity to which one can apply CRUD
operations. Not all resources support every operation, if a resource doesn't support the requested
operation an exception will be thrown. All CRUD operations that you can execute on a resource are
provided by a :ref:`ResourceManager <ResourceManager>` object. This type of object is created automatically for each
resource when you request it, e.g:

.. code-block:: python

   >>> redmine.project
   <redminelib.managers.ResourceManager object for Project resource>
   >>> redmine.issue
   <redminelib.managers.ResourceManager object for Issue resource>
   >>> redmine.user
   <redminelib.managers.ResourceManager object for User resource>

.. tip::

   It is recommended to create a :ref:`ResourceManager <ResourceManager>` object every time on the fly:

   .. code-block:: python

      # this is good
      >>> p1 = redmine.project.get(1)
      >>> p2 = redmine.project.get(2)

      # this is not so good
      >>> project = redmine.project
      >>> p1 = project.get(1)
      >>> p2 = project.get(2)

create
++++++

There are 2 create operations available: ``create()`` and ``new()``.

create
******

Creates a new resource with given fields, saves it to the Redmine and returns a newly created
:ref:`Resource` object.

.. code-block:: python

   >>> project = redmine.project.create(
   ...     name='Vacation',
   ...     identifier='vacation',
   ...     description='foo',
   ...     homepage='http://foo.bar',
   ...     is_public=True,
   ...     parent_id=345,
   ...     inherit_members=True,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   ... )
   >>> project
   <redminelib.resources.Project #123 "Vacation">

new
***

Constructs an entirely new :ref:`Resource` object but doesn't save it to the Redmine until you call
``save()`` method manually:

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

There's a big difference between creating a resource via ``create()`` and ``new()`` methods of a
:ref:`ResourceManager <ResourceManager>`. A ``create()`` method is the most simple way to create a resource, it just creates
a resource with the provided fields, returns a newly created :ref:`Resource` object and that's it. A
``new()`` method doesn't create a resource immediately, it just constructs an empty :ref:`Resource` object
so you can use its attributes to set their values as needed, also when you call a ``save()`` method on
the resource, at first its ``pre_create()`` method will be executed to run pre create tasks if any, then
a request to Redmine will be made to actually save the resource and finally a ``post_create()`` method
will be executed to run post create tasks if any. You can use any method you like, though it is
recommended to use a ``new()`` method as the most advanced one.

.. hint::

   If there's no need to process response, one can use a ``redmine.session`` with either a ``return_response=False``
   which doesn't return any response in a form of Resource object, but still validates it in case there were any
   errors and raises an exception if needed or a ``ignore_response=True`` which totally ignores response even
   if there were any errors. These attributes can save quite some processing time and if a response isn't needed
   one is highly encouraged to use on of them:

   .. code-block:: python

      with redmine.session(return_response=False):
          redmine.issue.create(project_id=123, subject='Vacation')

      with redmine.session(return_response=False):
          issue = redmine.issue.new()
          issue.project_id = 123
          issue.subject = 'Vacation'
          issue.save()

read
++++

There are 3 read operations available: ``get()``, ``all()`` and ``filter()``. Each of these
methods support different keyword arguments depending on the resource used and method called.
You can read more about it in each resource's documentation.

get
***

Returns a single :ref:`Resource` object either by integer ``id`` or by string ``identifier``:

.. code-block:: python

   >>> project = redmine.project.get('vacation')
   >>> project
   <redminelib.resources.Project #123 "Vacation">

all
***

Returns a :ref:`ResourceSet` object that contains all the requested :ref:`Resource` objects:

.. code-block:: python

   >>> projects = redmine.project.all()
   >>> projects
   <redminelib.resultsets.ResourceSet object with Project resources>

filter
******

Returns a :ref:`ResourceSet` object that contains :ref:`Resource` objects filtered by some condition(s):

.. code-block:: python

   >>> issues = redmine.issue.filter(project_id='vacation')
   >>> issues
   <redminelib.resultsets.ResourceSet object with Issue resources>


update
++++++

Updates a resource with given fields and saves it to the Redmine.

.. code-block:: python

   >>> redmine.project.update(123, name='Work', description='Work tasks')
   True

delete
++++++

Deletes a resource from Redmine.

.. code-block:: python

   >>> redmine.project.delete(1)
   True

.. warning::

   Deleted resources can't be restored. Use this method carefully.

Search
------

.. versionadded:: 2.0.0

Starting from Redmine >= 3.3 it is now possible to search for resources using the new Search API. There
are two ways to search for resources in Python-Redmine, one is to use the ``search()`` method of a
:ref:`ResourceManager <ResourceManager>` object and another is to use the ``search()`` method of a configured redmine object.
The difference between two methods is that a method of a :ref:`ResourceManager <ResourceManager>` object searches only for a
specific resource type and a method of a redmine object searches for all supported resource types. For
example if we want to search for all issues which have the text "rom" either in title or somewhere in
text:

.. code-block:: python

   >>> issues = redmine.issue.search('rom')
   <redminelib.resultsets.ResourceSet object with Issue resources>

And if we want to do the same but for all resources:

.. code-block:: python

   >>> resources = redmine.search('rom')
   {'news': <redminelib.resultsets.ResourceSet object with News resources>,
    'issues': <redminelib.resultsets.ResourceSet object with Issue resources>}

There can also be a ``unknown`` key which contains unknown resource types, for example it is possible
to search for messages using this functionality, but because messages don't have any API endpoints
they are considered unknown resource types to Python-Redmine, can't be converted to a :ref:`ResourceSet`
object and thus will be available as dictionaries under ``unknown`` key.

Both methods also support some options that can be combined together:

* **titles_only**. ``True`` to search only in title/names and ignore everything else.
* **open_issues**. ``True`` to search open issues only.
* **attachments**. ``True`` to also search attachments, ``only`` to search attachments only.
* **scope**. Search scope condition. Accepted values:

  * ``all``. Search all projects.
  * ``my_projects``. Search only in user's projects.
  * ``subprojects``. Include subprojects when my_projects specified.

* **resources**. Only search for these types of resources, makes sense only when applied to ``search()``
  method on redmine object, available values are: issues, news, documents, changesets, wiki_pages,
  messages, projects and more if additional plugins that support this API are installed.

All of these options are limiting, i.e. by default we try to find everything, so they should be used
only if there is a need to somehow limit search results. To revert the effect of any option set it to
``None`` or remove entirely.

.. code-block:: python

   >>> list(redmine.issue.search('rom', titles_only=True, open_issues=True))
   [<redminelib.resources.Issue "#123 (New): Romul">,
    <redminelib.resources.Issue "#456 (In Progress): From Russia with Love">]

   >>> redmine.search('rom', resources=['issues', 'projects'])
   {'issues': <redminelib.resultsets.ResourceSet object with Issue resources>,
    'projects': <redminelib.resultsets.ResourceSet object with Project resources>}

.. _Resource:

Resource
--------

A :ref:`Resource` object is the most important part of Python-Redmine. Every such object represents
a single resource and can be accessed in several ways, for example you can retrieve a resource via
``get()`` method of a :ref:`ResourceManager <ResourceManager>` as discussed earlier:

.. code-block:: python

   >>> project = redmine.project.get('vacation')
   >>> project.id
   123
   >>> project.name
   'Vacation'

Or create a new resource via ``create()`` method of a :ref:`ResourceManager <ResourceManager>`:

.. code-block:: python

   >>> project = redmine.project.create(
   ...     name='Vacation',
   ...     identifier='vacation',
   ...     description='foo',
   ...     homepage='http://foo.bar',
   ...     is_public=True,
   ...     parent_id=345,
   ...     inherit_members=True,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   ... )
   >>> project
   <redminelib.resources.Project #123 "Vacation">

Or you can construct an entirely new :ref:`Resource` object using ``new()`` method of a :ref:`ResourceManager <ResourceManager>`:

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

Introspection
+++++++++++++

Different resources can have different attributes even when they are of the same type. Attributes are
constructed dynamically by Python-Redmine when it receives the resource's data from Redmine. That means
that we need to introspect a resource somehow to see what's inside before we can use it. Fortunately a
:ref:`Resource` object provides several ways to introspect itself:

* **dir()**. Returns all the attributes resource has as a list.

  .. code-block:: python

     >>> dir(redmine.project.get('vacation'))
     ['created_on',
      'description',
      'enabled_modules',
      'id',
      'identifier',
      'issue_categories',
      'issues',
      'memberships',
      'name',
      'news',
      'status',
      'time_entries',
      'trackers',
      'updated_on',
      'versions',
      'wiki_pages']

* **list()**. Returns all the attributes with their values, which resource has, as a list of tuples.

  .. code-block:: python

     >>> list(redmine.project.get('vacation'))
     [('created_on', '2015-11-23T08:18:39Z'),
      ('time_entries', None),
      ('trackers', None),
      ('wiki_pages', None),
      ('status', 1),
      ('description', 'foo'),
      ('news', None),
      ('versions', None),
      ('identifier', 'vacation'),
      ('name', 'Vacation'),
      ('enabled_modules', None),
      ('issues', None),
      ('issue_categories', None),
      ('memberships', None),
      ('id', 123),
      ('updated_on', '2015-11-23T08:20:31Z')]

* **repr()**. Returns string representation of a resource.

  .. code-block:: python

     >>> repr(redmine.project.get('vacation'))
     '<redminelib.resources.Project #123 "Vacation">'

.. hint::

   Python has a very handy ``getattr()`` function which you can use to access attributes that are not
   always available, for example Issue resource has ``is_private`` attribute which is set to True if
   issue is private, otherwise this attribute doesn't exist:

   .. code-block:: python

      >>> issue = redmine.issue.get(1)
      >>> getattr(issue, 'is_private', False)  # prints True if issue is private, False otherwise
      False

Export
++++++

.. versionadded:: 2.0.0

A :ref:`Resource` object can be exported in one of the formats supported by Redmine using the ``export()``
method. A format can be one of the atom, csv, txt, pdf, html etc. You can read more about the supported
formats of each resource in its documentation.

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> issue.export('pdf', savepath='/home/jsmith')
   '/home/jsmith/123.pdf'

You can also get access to export url if needed via ``export_url()`` method:

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> issue.export_url('pdf')
   'http://demo.redmine.org/issues/123.pdf'

Refresh
+++++++

In some cases Redmine's REST API doesn't provide us with full resource data, fortunately there is
a ``refresh()`` method for that:

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> list(issue.project)
   [('name', 'FooBar'),
    ('id', 456)]
   >>> issue.project.refresh()
   >>> list(issue.project)
   [('created_on', '2015-12-07T09:19:27Z'),
    ('status', 1),
    ('description', 'A superb project'),
    ('identifier', 'foobar'),
    ('name', 'FooBar'),
    ('homepage', ''),
    ('parent', {'id': 789, 'name': 'Yada'}),
    ('id', 456),
    ('updated_on', '2015-12-07T09:19:27Z')]

Url
+++

:ref:`Resource` object also provides a convenient ``url`` attribute which can be used if there is a need
to know its url:

.. code-block:: python

   >>> issue = redmine.issue.get(123)
   >>> issue.url
   'http://demo.redmine.org/issues/123'

.. _ResourceSet:

ResourceSet
-----------

A :ref:`ResourceSet` object is another important object type that is used in Python-Redmine. This type of
object is constructed automatically by ``all()`` or ``filter()`` methods of a :ref:`ResourceManager <ResourceManager>` and is
just a collection of :ref:`Resource` objects with a few convenient features. :ref:`ResourceSet` object is lazy,
i.e. it doesn't make any requests to Redmine when it is created and is evaluated only when some of these
conditions are met:

* **Iteration**. A :ref:`ResourceSet` is iterable and is evaluated when you iterate over it.

  .. code-block:: python

     for project in redmine.project.all():
         print(project.name)

* **len()**. A :ref:`ResourceSet` is evaluated during the ``len()`` call and returns the length of itself.

  .. code-block:: python

     len(redmine.project.all())

* **list()**. Force evaluation of a :ref:`ResourceSet` by calling ``list()`` on it.

  .. code-block:: python

     list(redmine.project.all())

* **Index**. A :ref:`ResourceSet` is evaluated when some of its resources are requested by index.

  .. code-block:: python

     redmine.project.all()[0]  # Returns the first Resource in the ResourceSet

Limit/Offset
++++++++++++

:ref:`ResourceSet` object supports limit and offset, i.e. if you need to get only some portion of :ref:`Resource`
objects, as ``[offset:limit]`` or as keyword arguments:

.. code-block:: python

   redmine.project.all()[:135]  # Returns only first 135 projects
   redmine.project.all(limit=135)  # Returns only first 135 projects
   redmine.issue.filter(project_id='vacation')[10:3]  # Returns only 3 issues starting from 10th
   redmine.issue.filter(project_id='vacation', offset=10, limit=3)  # Returns only 3 issues starting from 10th

Please note, that keyword arguments have a higher priority, e.g.:

.. code-block:: python

   redmine.project.all(limit=10)[:20]  # Returns 10 projects and not 20

Export
++++++

.. versionadded:: 2.0.0

A :ref:`ResourceSet` object can be exported in one of the formats supported by Redmine using the ``export()``
method. A format can be one of the atom, csv, txt, pdf, html etc. You can read more about the supported
formats of each resource in its documentation.

.. code-block:: python

   >>> issues = redmine.issue.filter(project_id='vacation', status_id='*')
   >>> issues.export('csv', savepath='/home/jsmith', columns='all')
   '/home/jsmith/issues.csv'

Methods
+++++++

:ref:`ResourceSet` object provides several helper methods:

* **get()**

  Returns a single resource from the :ref:`ResourceSet` by resource id:

  .. code-block:: python

     redmine.project.all().get(30404, None)  # Returns None if a Resource is not found

* **filter()**

  .. versionchanged:: 2.1.0

  Returns a :ref:`ResourceSet` object filtered on a requested :ref:`Resource` object's attributes values:

  .. code-block:: python

     redmine.project.all().filter(is_public=True, status=1)

  It is also possible to follow resource relationships using a double underscore ``__``:

  .. code-block:: python

     redmine.issue.all().filter(author__id=1, status__name='New')

  Finally it is possible to apply ``lookups`` to an attribute using a double underscore ``__``:

  .. code-block:: python

     redmine.issue.all().filter(status__name__in=('New', 'Closed'))

  If a lookup isn't defined an ``exact`` lookup will be used. The following lookups are available:

  * exact (exact match)
  * in (in a given iterable)

  Due to the fact that Redmine may return resources with different attributes, for example some resources
  may and some may not have a ``version`` attribute defined, one should be very careful with correctly
  applying filters. For example in a case of typo in one of the attribute names an empty :ref:`ResourceSet`
  will be returned as there is no way for Python-Redmine to know whether it was a typo or there was just
  really no resources that could satisfy the filtering conditions.

  Also keep in mind that filtering a :ref:`ResourceSet` is implemented in Python-Redmine and not in the
  Redmine itself. It is advised to apply all possible filters on the Redmine side first, i.e. using a
  ``filter()`` method of a :ref:`ResourceManager <ResourceManager>` and then filter everything else
  using a ``filter()`` method of a :ref:`ResourceSet` object. This strategy will ensure that filtering
  is done in the fastest and most optimized way.

* **update()**

  Updates fields of all resources in a resource set with given values and returns
  an updated :ref:`ResourceSet` object, e.g., the following assigns issues of a project *vacation* with
  ids of *30404* and *30405* to the user with id of *547*:

  .. code-block:: python

     redmine.project.get('vacation').issues.filter((30404, 30405)).update(assigned_to_id=547)

  .. note::

     This method will also call ``pre_update()`` and ``post_update()`` methods for each :ref:`Resource` object
     in a :ref:`ResourceSet`.

* **delete()**

  Deletes all resources in a :ref:`ResourceSet`, e.g. the following deletes all issues from
  the *vacation* project:

  .. code-block:: python

     redmine.project.get('vacation').issues.delete()

  .. note::

     This method will also call ``pre_delete()`` and ``post_delete()`` methods for each :ref:`Resource` object
     in a :ref:`ResourceSet`.

* **values()**

  Returns an iterable of dictionaries rather than resource-instance objects. Each of those
  dictionaries represents a resource with the keys corresponding to the attribute names of resource objects.
  This example compares the dictionaries of ``values()`` with the normal resource objects:

  .. code-block:: python

     >>> list(redmine.issue_status.all(limit=1))
     [<redminelib.resources.IssueStatus #1 "New">]
     >>> list(redmine.issue_status.all(limit=1).values())
     [{'id': 1, 'is_default': True, 'name': 'New'}]

  The ``values()`` method takes optional positional arguments, ``*fields``, which specify field names
  to which resource fields should be limited. If you specify fields, each dictionary will contain only
  the field keys/values for the fields you specify. If you don't specify the fields, each dictionary
  will contain a key and value for every field in the resource:

  .. code-block:: python

     >>> list(redmine.issue_status.all(limit=1).values())
     [{'id': 1, 'is_default': True, 'name': 'New'}]
     >>> list(redmine.issue_status.all(limit=1).values('id', 'name'))
     [{'id': 1, 'name': 'New'}]

* **values_list()**

  .. versionadded:: 2.0.0

  Returns an iterable of tuples rather than resource-instance objects. Each of those
  tuples represents a resource without keys but with ordered values. This example compares the tuples
  of ``values_list()`` with the normal resource objects:

  .. code-block:: python

     >>> list(redmine.issue_status.all(limit=2))
     [<redminelib.resources.IssueStatus #1 "New">, <redminelib.resources.IssueStatus #2 "In Progress">]
     >>> list(redmine.issue_status.all(limit=2).values_list())
     [('New', 2), ('In Progress', 3)]

  The ``values_list()`` method takes optional positional arguments, ``*fields``, which specify field names
  to which resource fields should be limited. If you specify fields, each tuple will contain only the field
  values for the fields you specify. If you don't specify the fields, each tuple will contain a value for
  every field in the resource:

  .. code-block:: python

     >>> list(redmine.issue_status.all(limit=2).values_list())
     [('New', 2), ('In Progress', 3)]
     >>> list(redmine.issue_status.all(limit=2).values_list('id'))
     [(2,), (3,)]

  You can also flatten the iterable in case you are interested only in one field:

  .. code-block:: python

     >>> list(redmine.issue_status.all(limit=2).values_list('id', flat=True))
     [2, 3]

Attributes
++++++++++

:ref:`ResourceSet` object also provides some attributes:

* **limit**. What limit value was used to retrieve this resource set:

  .. code-block:: python

     >>> projects = redmine.project.all()[100:255]
     >>> projects.limit
     255

* **offset**. What offset value was used to retrieve this resource set:

  .. code-block:: python

     >>> projects = redmine.project.all()[100:255]
     >>> projects.offset
     100

* **total_count**. How much resources of current resource type there are available in Redmine:

  .. code-block:: python

     >>> projects = redmine.project.all()[100:255]
     >>> projects.total_count
     968
