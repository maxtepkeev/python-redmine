News
====

Supported by Redmine starting from version 1.1

Manager
-------

All operations on the News resource are provided by it's manager. To get access to
it you have to call ``redmine.news`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

.. versionadded:: 2.1.0

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single News resource from Redmine by it's id.

   :param int resource_id: (required). News id.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> news = redmine.news.get(123)
   >>> news
   <redminelib.resources.News #123 "Vacation">

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all News resources from Redmine.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> news = redmine.news.all(offset=10, limit=100)
   >>> news
   <redminelib.resultsets.ResourceSet object with News resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns News resources that match the given lookup parameters.

   :param project_id: (required). Id or identifier of news project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> news = redmine.news.filter(project_id='vacation')
   >>> news
   <redminelib.resultsets.ResourceSet object with News resources>

.. hint::

   You can also get news from a Project resource object directly using ``news`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.news
      <redminelib.resultsets.ResourceSet object with News resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of News resources in one of the following formats: atom

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> news = redmine.news.all()
   >>> news.export('atom', savepath='/home/jsmith', filename='news.atom')
   '/home/jsmith/news.atom'
