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

.. versionadded:: 2.3.0

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new News resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of News's project.
   :type project_id: int or string
   :param string title: (required). News title.
   :param string description: (required). News description.
   :param string summary: (optional). News summary.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> news = redmine.news.create(title='Foo', description='foobar')
   >>> news
   <redminelib.resources.News #8 "Foo">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty News resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> news = redmine.news.new()
   >>> news.title = 'Foo'
   >>> news.description = 'foobar'
   >>> news.save()
   <redminelib.resources.News #8 "Foo">

.. warning::

   Redmine's News API doesn't return a news object after create operation. Due to the fact that it goes
   against the behaviour of all other API endpoints, Python-Redmine has to do some tricks under the hood
   to return a resource object which involve an additional API request. If that isn't desired one should
   use the following technique:

   .. code-block:: python

      with redmine.session(return_response=False):
          news = redmine.news.new()
          news.title = 'Foo'
          news.description = 'foobar'
          news.save()

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

.. versionadded:: 2.3.0

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a News resource and saves them to the Redmine.

   :param int resource_id: (required). News id.
   :param string title: (optional). News title.
   :param string description: (optional). News description.
   :param string summary: (optional). News summary.
   :return: True

.. code-block:: python

   >>> redmine.news.update(1, title='Bar', description='barfoo', summary='bar')
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.News
   :noindex:

   Saves current state of a News resource to the Redmine. Attrs that can be
   changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> news = redmine.news.get(1)
   >>> news.title = 'Bar'
   >>> news.description = 'barfoo'
   >>> news.summary = 'bar'
   >>> news.save()
   <redminelib.resources.News #1 "Bar">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> news = redmine.news.get(1).save(
   ...     title='Bar',
   ...     description='barfoo',
   ...     summary='bar'
   ... )
   >>> news
   <redminelib.resources.News #1 "Bar">

Delete methods
--------------

.. versionadded:: 2.3.0

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single News resource from Redmine by it's id.

   :param int resource_id: (required). News id.
   :return: True

.. code-block:: python

   >>> redmine.news.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.News
   :noindex:

   Deletes current News resource object from Redmine.

   :return: True

.. code-block:: python

   >>> news = redmine.news.get(1)
   >>> news.delete()
   True

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
