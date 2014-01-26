Issue Category
==============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the issue category resource are provided via it's manager. To get
access to it you have to call ``redmine.issue_category`` where ``redmine`` is a configured
redmine object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new issue category resource with given fields and saves it to the Redmine.

    :param project_id: (required). Id or identifier of issue category's project.
    :type project_id: integer or string
    :param string name: (required). Issue category name.
    :param integer assigned_to_id: (optional). The id of the user assigned to the
      category (new issues with this category will be assigned by default to this user).
    :return: IssueCategory resource object

.. code-block:: python

    >>> category = redmine.issue_category.create(project_id='vacation', name='woohoo', assigned_to_id=13)
    >>> category
    <redmine.resources.IssueCategory #810 "woohoo">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty issue category resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: IssueCategory resource object

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
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single issue category resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the issue category.
    :return: IssueCategory resource object

.. code-block:: python

    >>> category = redmine.issue_category.get(794)
    >>> category
    <redmine.resources.IssueCategory #794 "Malibu">

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns issue category resources that match the given lookup parameters.

    :param project_id: (required). Get issue categories from the project with the
      given id, where id is either project id or project identifier.
    :type project_id: integer or string
    :return: ResourceSet object

.. code-block:: python

    >>> categories = redmine.issue_category.filter(project_id='vacation')
    >>> categories
    <redmine.resultsets.ResourceSet object with IssueCategory resources>

.. hint::

    You can also get issue categories from a project resource object directly using
    ``issue_categories`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.issue_categories
        <redmine.resultsets.ResourceSet object with IssueCategory resources>

Update methods
--------------

Not yet supported by Python Redmine

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single issue category resource from the Redmine by it's id.

    :param integer resource_id: (required). Issue category id.
    :param integer reassign_to_id: (optional). When there are issues assigned to the
      category you are deleting, this parameter lets you reassign these issues to the
      category with given id.
    :return: True

.. code-block:: python

    >>> redmine.issue_category.delete(1, reassign_to_id=2)
    True
