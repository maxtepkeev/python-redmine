Checklist
=========

Requires Pro Edition and `Checklists plugin <https://www.redmineup.com/pages/plugins/checklists>`_ >= 3.0.0.

Manager
-------

All operations on the Checklist resource are provided by its manager. To get access to
it you have to call ``redmine.checklist`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Checklist resource item with given fields and saves it to the Checklists plugin.

   :param int issue_id: (required). Issue to which checklist item belongs to.
   :param string subject: (required). Subject of checklist item.
   :param bool is_done: (optional). Whether checklist item is done.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> checklist = redmine.checklist.create(issue_id=1, subject='FooBar', is_done=False)
   >>> checklist
   <redminelib.resources.Checklist #1>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Checklist resource item but saves it to the Checklists plugin only when ``save()`` is
   called, also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid
   attributes are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> checklist = redmine.checklist.new()
   >>> checklist.issue_id = 1
   >>> checklist.subject = 'FooBar'
   >>> checklist.is_done = False
   >>> checklist.save()
   <redminelib.resources.Checklist #1>

.. hint::

   Checklists can also be created/updated together with the Issue using checklists attribute:

   .. code-block:: python

      >>> issue = redmine.issue.create(
      ...     project_id=123,
      ...     subject='foo',
      ...     checklists=[{'subject': 'foo', 'is_done': True}, {'subject': 'bar', 'is_done': False}]
      ... )
      >>> issue
      <redminelib.resources.Issue #3>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Checklist resource item from the Checklists plugin by its id.

   :param int resource_id: (required). Id of the checklist item.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> checklist = redmine.checklist.get(123)
   >>> checklist
   <redminelib.resources.Checklist #123>

all
+++

Not supported by Checklists plugin

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Checklist resource items that match the given lookup parameters.

   :param int issue_id: (required). Issue to which these checklist items belong to.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> checklists = redmine.checklist.filter(issue_id=123)
   >>> checklists
   <redminelib.resultsets.ResourceSet object with Checklist resources>

.. hint::

   You can also get checklist items from an Issue resource objects directly using ``checklists`` relation:

   .. code-block:: python

      >>> issue = redmine.issue.get(1)
      >>> issue.checklists
      <redminelib.resultsets.ResourceSet object with Checklist resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Checklist resource item and saves them to the Checklists plugin.

   :param int resource_id: (required). Checklist item id.
   :param int issue_id: (optional). Checklist item issue id.
   :param string subject: (optional). Subject of the checklist item.
   :param bool is_done: (optional). Whether checklist item is done.
   :param int position: (optional). Checklist item position.
   :return: True

.. code-block:: python

   >>> redmine.checklist.update(1, issue_id=1, subject='FooBar', is_done=False, position=1)
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Checklist
   :noindex:

   Saves the current state of a Checklist item resource to the Checklists plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> checklist = redmine.checklist.get(123)
   >>> checklist.issue_id = 1
   >>> checklist.subject = 'FooBar'
   >>> checklist.is_done = False
   >>> checklist.position = 1
   >>> checklist.save()
   <redminelib.resources.Checklist #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> checklist = redmine.checklist.get(123).save(
   ...     issue_id=1,
   ...     subject='Foobar',
   ...     is_done=False,
   ...     position=1
   ... )
   >>> checklist
   <redminelib.resources.Checklist #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Checklist resource item from the Checklists plugin by its id.

   :param int resource_id: (required). Checklist item id.
   :return: True

.. code-block:: python

   >>> redmine.checklist.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Checklist
   :noindex:

   Deletes current Checklist resource item object from the Checklists plugin.

   :return: True

.. code-block:: python

   >>> checklist = redmine.checklist.get(1)
   >>> checklist.delete()
   True

Export
------

Not supported by Checklists plugin
