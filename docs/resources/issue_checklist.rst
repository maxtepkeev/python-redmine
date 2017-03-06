Issue Checklist
==============

Supported by Redmine starting from version 2.3

Manager
-------

All operations on the issue checklist resource are provided via it's manager. To get
access to it you have to call ``redmine.issue_checklist`` where ``redmine`` is a configured
redmine object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new issue checklist resource with given fields and saves it to the Redmine.

    :param integer issue_id: (required). Creates a checklist for the issue of given id.
    :param bool is_done: Set checklist as done.
    :param string subject: Text of the checklist .
    :param integer position: Position of the checklist .
    :return: IssueChecklist resource object.

.. code-block:: python

    >>> checklist = redmine.issue_checklist.create(issue_id=12345, is_done=False, subject='New todo item')
    >>> checklist
    <redmine.resources.IssueChecklist #6936>

new
+++

Not supported by Redmine

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single issue checklist resource from the Redmine by its id.

    :param integer resource_id: (required). Id of the issue checklist.
    :return: IssueChecklist resource object.

.. code-block:: python

    >>> checklist = redmine.issue_checklist.get(6936)
    >>> checklist
    <redmine.resources.IssueChecklist #6936>

all
+++

Not supported by Redmine

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

    Updates values of given fields of a checklist resource and saves them to the Redmine.

    :param integer checklist_id: (required). Checklist id.
    :param bool is_done: Set checklist as done.
    :param string subject: Text of the checklist .
    :param integer position: Position of the checklist.
    :return: True

.. code-block:: python
    >>> redmine.issue_checklist.update(6936, is_done=True)
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single issue checklist resource from Redmine by its id.

    :param integer resource_id: (required). Issue checklist id.
    :return: True

.. code-block:: python

    >>> redmine.issue_checklist.delete(6936)
    True
