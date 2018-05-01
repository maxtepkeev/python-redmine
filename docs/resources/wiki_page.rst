Wiki Page
=========

Supported by Redmine starting from version 2.2

Manager
-------

All operations on the WikiPage resource are provided by it's manager. To get access to it
you have to call ``redmine.wiki_page`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Creates new WikiPage resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of wiki page's project.
   :type project_id: int or string
   :param string text: (required). Text of the wiki page.
   :param string title: (required). Title of the wiki page.
   :param string parent_title: (optional). Title of parent wiki page.
   :param string comments: (optional). Comments of the wiki page.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> from io import StringIO
   >>> wiki_page = redmine.wiki_page.create(
   ...     project_id='vacation',
   ...     title='FooBar',
   ...     text='foo',
   ...     parent_title='Yada',
   ...     comments='bar',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': StringIO('I am content of file 2')}]
   ... )
   >>> wiki_page
   <redminelib.resources.WikiPage "FooBar">

new
+++

.. py:method:: new()
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Creates new empty WikiPage resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> wiki_page = redmine.wiki_page.new()
   >>> wiki_page.project_id = 'vacation'
   >>> wiki_page.title = 'FooBar'
   >>> wiki_page.text = 'foo'
   >>> wiki_page.parent_title = 'Yada'
   >>> wiki_page.comments = 'bar'
   >>> wiki_page.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   >>> wiki_page.save()
   <redminelib.resources.WikiPage "FooBar">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Returns single WikiPage resource from Redmine by it's title.

   :param string resource_id: (required). Title of the wiki page.
   :param project_id: (required). Id or identifier of wiki page's project.
   :type project_id: int or string
   :param int version: (optional). Version of the wiki page.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - attachments

   :return: :ref:`Resource` object

.. code-block:: python

   >>> wiki_page = redmine.wiki_page.get('Photos', project_id='vacation', version=12, include=['attachments'])
   >>> wiki_page
   <redminelib.resources.WikiPage "Photos">

.. hint::

   WikiPage resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a WikiPage
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the WikiPage resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> wiki_page = redmine.wiki_page.get(524)
      >>> wiki_page.attachments
      <redminelib.resultsets.ResourceSet object with Attachment resources>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Returns WikiPage resources that match the given lookup parameters.

   :param project_id: (required). Id or identifier of wiki page's project.
   :type project_id: int or string
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> wiki_pages = redmine.wiki_page.filter(project_id='vacation')
   >>> wiki_pages
   <redminelib.resultsets.ResourceSet object with WikiPage resources>

.. hint::

   You can also get wiki pages from a Project resource object directly using ``wiki_pages`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.wiki_pages
      <redminelib.resultsets.ResourceSet object with WikiPage resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Updates values of given fields of a WikiPage resource and saves them to the Redmine.

   :param string resource_id: (required). Title of the wiki page.
   :param project_id: (required). Id or identifier of wiki page's project.
   :type project_id: int or string
   :param string text: (required). Text of the wiki page.
   :param string title: (optional). Title of the wiki page.
   :param string parent_title: (optional). Title of parent wiki page.
   :param string comments: (optional). Comments of the wiki page.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> from io import StringIO
   >>> redmine.wiki_page.update(
   ...     'Foo',
   ...     project_id='vacation',
   ...     title='FooBar',
   ...     text='foo',
   ...     parent_title='Yada',
   ...     comments='bar',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': StringIO('I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.WikiPage
   :noindex:

   Saves the current state of a WikiPage resource to the Redmine. Attrs that can
   be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> wiki_page = redmine.wiki_page.get('Foo', project_id='vacation')
   >>> wiki_page.title = 'Bar'
   >>> wiki_page.text = 'bar'
   >>> wiki_page.parent_title = 'Yada'
   >>> wiki_page.comments = 'changed foo to bar'
   >>> wiki_page.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   >>> wiki_page.save()
   <redminelib.resources.WikiPage "Bar">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> wiki_page = redmine.wiki_page.get('Foo', project_id='vacation').save(
   ...     title='Bar',
   ...     text='bar',
   ...     parent_title='Yada',
   ...     comments='changed foo to bar',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
   ... )
   >>> wiki_page
   <redminelib.resources.WikiPage "Bar">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
   :module: redminelib.managers.WikiPageManager
   :noindex:

   Deletes single WikiPage resource from Redmine by it's title.

   :param string resource_id: (required). Title of the wiki page.
   :param project_id: (required). Id or identifier of wiki page's project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> redmine.wiki_page.delete('Foo', project_id=1)
   True

.. py:method:: delete()
   :module: redminelib.resources.WikiPage
   :noindex:

   Deletes current WikiPage resource object from Redmine.

   :return: True

.. code-block:: python

   >>> wiki = redmine.wiki_page.get('Foo', project_id=1)
   >>> wiki.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resources.WikiPage
   :noindex:

   Exports WikiPage resource in one of the following formats: pdf, html, txt

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> wiki = redmine.wiki_page.get('Foo', project_id=1)
   >>> wiki.export('pdf', savepath='/home/jsmith')
   '/home/jsmith/123.pdf'

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of WikiPage resources in one of the following formats: atom, pdf, html

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> wiki_pages = redmine.wiki_page.filter(project_id='vacation')
   >>> wiki_pages.export('pdf', savepath='/home/jsmith', filename='wiki_pages.pdf')
   '/home/jsmith/wiki_pages.pdf'
