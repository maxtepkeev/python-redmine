Project Membership
==================

Supported by Redmine starting from version 1.4

Manager
-------

All operations on the ProjectMembership resource are provided by it's manager. To get access to
it you have to call ``redmine.project_membership`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new ProjectMembership resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of the project.
   :type project_id: int or string
   :param int user_id: (required). Id of the user to add to the project.
   :param list role_ids: (required). Role ids to add to the user in this project.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> membership = redmine.project_membership.create(project_id='vacation', user_id=1, role_ids=[1, 2])
   >>> membership
   <redminelib.resources.ProjectMembership #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty ProjectMembership resource but saves it to the Redmine only when ``save()`` is
   called, also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object.
   Valid attributes are the same as for ``create()`` method above.bove.

   :return: :ref:`Resource` object

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
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single ProjectMembership resource from Redmine by it's id.

   :param int resource_id: (required). Project membership id.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> membership = redmine.project_membership.get(521)
   >>> membership
   <redminelib.resources.ProjectMembership #521>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns ProjectMembership resources that match the given lookup parameters.

   :param project_id: (required). Id or identifier of the project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> memberships = redmine.project_membership.filter(project_id='vacation')
   >>> memberships
   <redminelib.resultsets.ResourceSet object with ProjectMembership resources>

.. hint::

   You can also get project memberships from a Project resource object directly using
   ``memberships`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.memberships
      <redminelib.resultsets.ResourceSet object with ProjectMembership resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a ProjectMembership resource and saves them to the Redmine.

   :param int resource_id: (required). Project membership id.
   :param list role_ids: (required). Role ids to add to the user in this project.
   :return: True

.. code-block:: python

   >>> redmine.project_membership.update(1, role_ids=[1, 2])
   True

save
++++

.. py:method:: save()
   :module: redminelib.resources.ProjectMembership
   :noindex:

   Saves the current state of a ProjectMembership resource to the Redmine. Fields that can
   be changed are the same as for ``update()`` method above.

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
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single ProjectMembership resource from Redmine by it's id.

   :param int resource_id: (required). Project membership id.
   :return: True

.. code-block:: python

   >>> redmine.project_membership.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.ProjectMembership
   :noindex:

   Deletes current ProjectMembership resource object from Redmine.

   :return: True

.. code-block:: python

   >>> membership = redmine.project_membership.get(1)
   >>> membership.delete()
   True

Export
------

Not supported by Redmine
