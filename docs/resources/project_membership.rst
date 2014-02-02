Project Membership
==================

Supported by Redmine starting from version 1.4

Manager
-------

All operations on the project membership resource are provided via it's manager. To get access to it
you have to call ``redmine.project_membership`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new project membership resource with given fields and saves it to the Redmine.

    :param project_id: (required). Id or identifier of the project.
    :type project_id: integer or string
    :param integer user_id: (required). Id of the user to add to the project.
    :param role_ids: (required). Role ids to add to the user in this project.
    :type role_ids: list or tuple
    :return: ProjectMembership resource object

.. code-block:: python

    >>> membership = redmine.project_membership.create(project_id='vacation', user_id=1, role_ids=[1, 2])
    >>> membership
    <redmine.resources.ProjectMembership #123>

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty project membershp resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: ProjectMembership resource object

.. code-block:: python

    >>> membership = redmine.project_membership.new()
    >>> membership.project_id = 'vacation'
    >>> membership.user_id = 1
    >>> membership.role_ids = [1, 2]
    >>> membership.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single project membership resource from the Redmine by it's id.

    :param integer resource_id: (required). Project membership id.
    :return: ProjectMembership resource object

.. code-block:: python

    >>> membership = redmine.project_membership.get(521)
    >>> membership
    <redmine.resources.ProjectMembership #521>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns project membership resources that match the given lookup parameters.

    :param project_id: (required). Id or identifier of the project.
    :type project_id: integer or string
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> memberships = redmine.project_membership.filter(project_id='vacation')
    >>> memberships
    <redmine.resultsets.ResourceSet object with ProjectMembership resources>

.. hint::

    You can also get project memberships from a project resource object directly using
    ``memberships`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.memberships
        <redmine.resultsets.ResourceSet object with ProjectMembership resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a project membership resource and saves them to the Redmine.

    :param integer resource_id: (required). Project membership id.
    :param role_ids: (required). Role ids to add to the user in this project.
    :type role_ids: list or tuple
    :return: True

.. code-block:: python

    >>> redmine.project_membership.update(1, role_ids=[1, 2])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.ProjectMembership
    :noindex:

    Saves the current state of a project membership resource to the Redmine. Fields that can
    be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> membership = redmine.project_membership.get(1)
    >>> membership.role_ids = [1, 2]
    >>> membership.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single project membership resource from the Redmine by it's id.

    :param integer resource_id: (required). Project membership id.
    :return: True

.. code-block:: python

    >>> redmine.project_membership.delete(1)
    True
