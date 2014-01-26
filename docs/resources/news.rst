News
====

Supported by Redmine starting from version 1.1

Manager
-------

All operations on the news resource are provided via it's manager. To get access to
it you have to call ``redmine.news`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

Not supported by Redmine

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all news resources from the Redmine.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> news = redmine.news.all(offset=10, limit=100)
    >>> news
    <redmine.resultsets.ResourceSet object with News resources>

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns news resources that match the given lookup parameters.

    :param project_id: (required). Id or identifier of news project.
    :type project_id: integer or string
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> news = redmine.news.filter(project_id='vacation')
    >>> news
    <redmine.resultsets.ResourceSet object with News resources>

.. hint::

    You can also get news from a project resource object directly using ``news`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.news
        <redmine.resultsets.ResourceSet object with News resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
