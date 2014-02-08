Issue Relation
==============

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the issue relation resource are provided via it's manager. To get
access to it you have to call ``redmine.issue_relation`` where ``redmine`` is a configured
redmine object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new issue relation resource with given fields and saves it to the Redmine.

    :param integer issue_id: (required). Creates a relation for the issue of given id.
    :param integer issue_to_id: (required). Id of the related issue.
    :param string relation_type:
      .. raw:: html

          (required). Type of the relation, available values are:

      - relates
      - duplicates
      - duplicated
      - blocks
      - blocked
      - precedes
      - follows

    :param integer delay: (optional). Delay in days for a "precedes" or "follows" relation.
    :return: IssueRelation resource object

.. code-block:: python

    >>> relation = redmine.issue_relation.create(issue_id=12345, issue_to_id=54321, relation_type='precedes', delay=5)
    >>> relation
    <redmine.resources.IssueRelation #667>

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty issue relation resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: IssueRelation resource object

.. code-block:: python

    >>> relation = redmine.issue_relation.new()
    >>> relation.issue_id = 12345
    >>> relation.issue_to_id = 54321
    >>> relation.relation_type = 'precedes'
    >>> relation.delay = 5
    >>> relation.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single issue relation resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the issue relation.
    :return: IssueRelation resource object

.. code-block:: python

    >>> relation = redmine.issue_relation.get(606)
    >>> relation
    <redmine.resources.IssueRelation #606>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns issue relation resources that match the given lookup parameters.

    :param integer issue_id: (required). Get relations from the issue with the given id.
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> relations = redmine.issue_relation.filter(issue_id=6543)
    >>> relations
    <redmine.resultsets.ResourceSet object with IssueRelation resources>

.. hint::

    You can also get issue relations from an issue resource object directly using
    ``relations`` relation:

    .. code-block:: python

        >>> issue = redmine.issue.get(6543)
        >>> issue.relations
        <redmine.resultsets.ResourceSet object with IssueRelation resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single issue relation resource from the Redmine by it's id.

    :param integer resource_id: (required). Issue relation id.
    :return: True

.. code-block:: python

    >>> redmine.issue_relation.delete(1)
    True
