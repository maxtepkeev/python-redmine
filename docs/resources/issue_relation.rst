Issue Relation
==============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the IssueRelation resource are provided by it's manager. To get access
to it you have to call ``redmine.issue_relation`` where ``redmine`` is a configured redmine
object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new IssueRelation resource with given fields and saves it to the Redmine.

   :param int issue_id: (required). Creates a relation for the issue of given id.
   :param int issue_to_id: (required). Id of the related issue.
   :param string relation_type:
    .. raw:: html

       (required). Type of the relation, one of:

    - relates
    - duplicates
    - duplicated
    - blocks
    - blocked
    - precedes
    - follows
    - copied_to
    - copied_from

   :param int delay: (optional). Delay in days for a "precedes" or "follows" relation.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> relation = redmine.issue_relation.create(
   ...     issue_id=12345,
   ...     issue_to_id=54321,
   ...     relation_type='precedes',
   ...     delay=5
   ... )
   >>> relation
   <redminelib.resources.IssueRelation #667>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty IssueRelation resource but saves it to the Redmine only when ``save()`` is
   called, also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object.
   Valid attributes are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

    >>> relation = redmine.issue_relation.new()
    >>> relation.issue_id = 12345
    >>> relation.issue_to_id = 54321
    >>> relation.relation_type = 'precedes'
    >>> relation.delay = 5
    >>> relation.save()
   <redminelib.resources.IssueRelation #667>

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single IssueRelation resource from Redmine by it's id.

   :param int resource_id: (required). Id of the issue relation.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> relation = redmine.issue_relation.get(606)
   >>> relation
   <redminelib.resources.IssueRelation #606>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns IssueRelation resources that match the given lookup parameters.

   :param int issue_id: (required). Get relations from the issue with given id.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> relations = redmine.issue_relation.filter(issue_id=6543)
   >>> relations
   <redminelib.resultsets.ResourceSet object with IssueRelation resources>

.. hint::

   You can also get issue relations from an Issue resource object directly using
   ``relations`` relation:

   .. code-block:: python

      >>> issue = redmine.issue.get(6543)
      >>> issue.relations
      <redminelib.resultsets.ResourceSet object with IssueRelation resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redminelib.managers.ResourceManager
    :noindex:

    Deletes single IssueRelation resource from Redmine by it's id.

    :param int resource_id: (required). Issue relation id.
    :return: True

.. code-block:: python

    >>> redmine.issue_relation.delete(1)
    True

.. py:method:: delete()
   :module: redminelib.resources.IssueRelation
   :noindex:

   Deletes current IssueRelation resource object from Redmine.

   :return: True

.. code-block:: python

   >>> relation = redmine.issue_relation.get(1)
   >>> relation.delete()
   True

Export
------

Not supported by Redmine
