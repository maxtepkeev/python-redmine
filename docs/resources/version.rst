Version
=======

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the version resource are provided via it's manager. To get access
to it you have to call ``redmine.version`` where ``redmine`` is a configured redmine
object. See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new version resource with given fields and saves it to the Redmine.

    :param project_id: (required). Id or identifier of version's project.
    :type project_id: integer or string
    :param string name: (required). Version name.
    :param string status:
      .. raw:: html

          (optional). Status of the version, available values are:

      - open (default)
      - locked
      - closed

    :param string sharing:
      .. raw:: html

          (optional). Version sharing, available values are:

      - none (default)
      - descendants
      - hierarchy
      - tree
      - system

    :param string due_date: (optional). Expiration date.
    :param string description: (optional). Version description.
    :param string wiki_page_title: (optional). Version wiki page title.
    :return: Version resource object

.. code-block:: python

    >>> version = redmine.version.create(project_id='vacation', name='Vacation', status='open', sharing='none', due_date='2014-01-30', description='my vacation', wiki_page_title='Vacation')
    >>> version
    <redmine.resources.Version #235 "Vacation">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty version resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: Version resource object

.. code-block:: python

    >>> version = redmine.version.new()
    >>> version.project_id = 'vacation'
    >>> version.name = 'Vacation'
    >>> version.status = 'open'
    >>> version.sharing = 'none'
    >>> version.due_date='2014-01-30'
    >>> version.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single version resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the version.
    :return: Version resource object

.. code-block:: python

    >>> version = redmine.version.get(1)
    >>> version
    <redmine.resources.Version #1 "Release 1">

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns version resources that match the given lookup parameters.

    :param project_id: (required). Id or identifier of version's project.
    :type project_id: integer or string
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> versions = redmine.version.filter(project_id='vacation')
    >>> versions
    <redmine.resultsets.ResourceSet object with Versions resources>

.. hint::

    You can also get versions from a project resource object directly using
    ``versions`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.versions
        <redmine.resultsets.ResourceSet object with Version resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a version resource and saves them to the Redmine.

    :param integer resource_id: (required). Version id.
    :param string name: (optional). Version name.
    :param string status:
      .. raw:: html

          (optional). Status of the version, available values are:

      - open (default)
      - locked
      - closed

    :param string sharing:
      .. raw:: html

          (optional). Version sharing, available values are:

      - none (default)
      - descendants
      - hierarchy
      - tree
      - system

    :param string due_date: (optional). Expiration date.
    :param string description: (optional). Version description.
    :param string wiki_page_title: (optional). Version wiki page title.
    :return: True

.. code-block:: python

    >>> redmine.version.update(1, name='Vacation', status='open', sharing='none', due_date='2014-01-30', description='my vacation', wiki_page_title='Vacation')
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Version
    :noindex:

    Saves the current state of a version resource to the Redmine. Fields that can
    be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> version = redmine.version.get(1)
    >>> version.name = 'Vacation'
    >>> version.status = 'open'
    >>> version.sharing = 'none'
    >>> version.due_date = '2014-01-30'
    >>> version.description = 'my vacation'
    >>> version.wiki_page_title = 'Vacation'
    >>> version.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single version resource from the Redmine by it's id.

    :param integer resource_id: (required). Version id.
    :return: True

.. code-block:: python

    >>> redmine.version.delete(1)
    True
