Project
=======

Supported by Redmine starting from version 1.0

Manager
-------

All operations on the project resource are provided via it's manager. To get access to it
you have to call ``redmine.project`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new project resource with given fields and saves it to the Redmine.

    :param string name: (required). Project name.
    :param string identifier: (required). Project identifier.
    :param string description: (optional). Project description.
    :param string homepage: (optional). Project homepage url.
    :param boolean is_public: (optional). Whether project is public.
    :param integer parent_id: (optional). Project's parent project id.
    :param boolean inherit_members: (optional). Whether project will inherit parent project's members.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :return: Project resource object

.. code-block:: python

    >>> project = redmine.project.create(name='Vacation', identifier='vacation', description='foo', homepage='http://foo.bar', is_public=True, parent_id=345, inherit_members=True, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    >>> project
    <redmine.resources.Project #123 "Vacation">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty project resource but doesn't save it to the Redmine. This is useful if
    you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: Project resource object

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

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single project resource from the Redmine by it's id or identifier.

    :param resource_id: (required). Project id or identifier.
    :type resource_id: integer or string
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - trackers
      - issue_categories

    :return: Project resource object

.. code-block:: python

    >>> project = redmine.project.get('vacation', include='trackers,issue_categories')
    >>> project
    <redmine.resources.Project #123 "Vacation">

.. hint::

    Project resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a Project
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the Project resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.trackers
        <redmine.resultsets.ResourceSet object with Tracker resources>

.. hint::

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

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all project resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> projects = redmine.project.all(offset=10, limit=100)
    >>> projects
    <redmine.resultsets.ResourceSet object with Project resources>

filter
++++++

Not supported by Redmine

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a project resource and saves them to the Redmine.

    :param integer resource_id: (required). Project id.
    :param string name: (optional). Project name.
    :param string description: (optional). Project description.
    :param string homepage: (optional). Project homepage url.
    :param boolean is_public: (optional). Whether project is public.
    :param integer parent_id: (optional). Project's parent project id.
    :param boolean inherit_members: (optional). Whether project will inherit parent project's members.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :return: True

.. code-block:: python

    >>> redmine.project.update(1, name='Vacation', description='foo', homepage='http://foo.bar', is_public=True, parent_id=345, inherit_members=True, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Project
    :noindex:

    Saves the current state of a project resource to the Redmine. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

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

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single project resource from the Redmine by it's id or identifier.

    :param resource_id: (required). Project id or identifier.
    :type resource_id: integer or string
    :return: True

.. code-block:: python

    >>> redmine.project.delete(1)
    True
