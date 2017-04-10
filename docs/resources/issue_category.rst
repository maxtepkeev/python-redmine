Issue Category
==============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the IssueCategory resource are provided by it's manager. To get
access to it you have to call ``redmine.issue_category`` where ``redmine`` is a configured
redmine object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new IssueCategory resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of issue category's project.
   :type project_id: int or string
   :param string name: (required). Issue category name.
   :param int assigned_to_id: (optional). The id of the user assigned to the category
    (new issues with this category will be assigned by default to this user).
   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.issue_category.create(project_id='vacation', name='woohoo', assigned_to_id=13)
   >>> category
   <redminelib.resources.IssueCategory #810 "woohoo">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty IssueCategory resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.issue_category.new()
   >>> category.project_id = 'vacation'
   >>> category.name = 'woohoo'
   >>> category.assigned_to_id = 13
   >>> category.save()
   True

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single IssueCategory resource from Redmine by it's id.

   :param int resource_id: (required). Id of the issue category.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> category = redmine.issue_category.get(794)
   >>> category
   <redminelib.resources.IssueCategory #794 "Malibu">

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns IssueCategory resources that match the given lookup parameters.

   :param project_id: (required). Get issue categories from the project with the
    given id, where id is either project id or project identifier.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> categories = redmine.issue_category.filter(project_id='vacation')
   >>> categories
   <redminelib.resultsets.ResourceSet object with IssueCategory resources>

.. hint::

   You can also get issue categories from a Project resource object directly using
   ``issue_categories`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.issue_categories
      <redminelib.resultsets.ResourceSet object with IssueCategory resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an IssueCategory resource and saves them to the Redmine.

   :param int resource_id: (required). Issue category id.
   :param string name: (optional). Issue category name.
   :param int assigned_to_id: (optional). The id of the user assigned to the
    category (new issues with this category will be assigned by default to this user).
   :return: True

.. code-block:: python

   >>> redmine.issue_category.update(1, name='woohoo', assigned_to_id=13)
   True

save
++++

.. py:method:: save()
   :module: redminelib.resources.IssueCategory
   :noindex:

   Saves the current state of an IssueCategory resource to the Redmine. Fields that
   can be changed are the same as for ``update()`` method above.

   :return: True

.. code-block:: python

   >>> category = redmine.issue_category.get(1)
   >>> category.name = 'woohoo'
   >>> category.assigned_to_id = 13
   >>> category.save()
   True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single IssueCategory resource from Redmine by it's id.

   :param int resource_id: (required). Issue category id.
   :param int reassign_to_id: (optional). When there are issues assigned to the
    category you are deleting, this parameter lets you reassign these issues to the
    category with given id.
   :return: True

.. code-block:: python

   >>> redmine.issue_category.delete(1, reassign_to_id=2)
   True

.. py:method:: delete()
   :module: redminelib.resources.IssueCategory
   :noindex:

   Deletes current IssueCategory resource object from Redmine.

   :param int reassign_to_id: (optional). When there are issues assigned to the
    category you are deleting, this parameter lets you reassign these issues to the
    category with given id.
   :return: True

.. code-block:: python

   >>> category = redmine.issue_category.get(794)
   >>> category.delete(reassign_to_id=2)
   True

Export
------

Not supported by Redmine
