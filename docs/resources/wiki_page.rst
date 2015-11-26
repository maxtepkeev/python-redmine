Wiki Page
=========

Supported by Redmine starting from version 2.2

Manager
-------

All operations on the wiki page resource are provided via it's manager. To get access to it
you have to call ``redmine.wiki_page`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new wiki page resource with given fields and saves it to the Redmine.

    :param project_id: (required). Id or identifier of wiki page's project.
    :type project_id: integer or string
    :param string title: (required). Title of the wiki page.
    :param string text: (required). Text of the wiki page.
    :param string parent_title: (optional). Title of parent wiki page.
    :param string comments: (optional). Comments of the wiki page.
    :param uploads:
      .. raw:: html

          (optional). Uploads in the form of [{'': ''}, ...], accepted keys are:

      - path (required). Absolute path to the file that should be uploaded.
      - filename (optional). Name of the file after upload.
      - description (optional). Description of the file.
      - content_type (optional). Content type of the file.

    :type uploads: list or tuple
    :return: WikiPage resource object

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.create(project_id='vacation', title='FooBar', text='foo', parent_title='Yada', comments='bar', uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}])
    >>> wiki_page
    <redmine.resources.WikiPage "FooBar">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty wiki page resource but doesn't save it to the Redmine. This is useful
    if you want to set some resource fields later based on some condition(s) and only after
    that save it to the Redmine. Valid attributes are the same as for ``create`` method above.

    :return: WikiPage resource object

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.new()
    >>> wiki_page.project_id = 'vacation'
    >>> wiki_page.title = 'FooBar'
    >>> wiki_page.text = 'foo'
    >>> wiki_page.parent_title = 'Yada'
    >>> wiki_page.comments = 'bar'
    >>> wiki_page.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
    >>> wiki_page.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single wiki page resource from the Redmine by it's title.

    :param string resource_id: (required). Title of the wiki page.
    :param project_id: (required). Id or identifier of wiki page's project.
    :type project_id: integer or string
    :param integer version: (optional). Version of the wiki page.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - attachments

    :return: WikiPage resource object

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.get('Photos', project_id='vacation', version=12, include='attachments')
    >>> wiki_page
    <redmine.resources.WikiPage "Photos">

.. hint::

    .. versionadded:: 0.4.0

    |

    WikiPage resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a WikiPage
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the WikiPage resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> wiki_page = redmine.wiki_page.get(524)
        >>> wiki_page.attachments
        <redmine.resultsets.ResourceSet object with Attachment resources>

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns wiki page resources that match the given lookup parameters.

    :param project_id: (required). Id or identifier of wiki page's project.
    :type project_id: integer or string
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> wiki_pages = redmine.wiki_page.filter(project_id='vacation')
    >>> wiki_pages
    <redmine.resultsets.ResourceSet object with WikiPage resources>

.. hint::

    You can also get wiki pages from a project resource object directly using
    ``wiki_pages`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.wiki_pages
        <redmine.resultsets.ResourceSet object with WikiPage resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a wiki page resource and saves them to the Redmine.

    :param string resource_id: (required). Title of the wiki page.
    :param project_id: (required). Id or identifier of wiki page's project.
    :type project_id: integer or string
    :param string title: (optional). Title of the wiki page.
    :param string text: (optional). Text of the wiki page.
    :param string parent_title: (optional). Title of parent wiki page.
    :param string comments: (optional). Comments of the wiki page.
    :param uploads:
      .. raw:: html

          (optional). Uploads in the form of [{'': ''}, ...], accepted keys are:

      - path (required). Absolute path to the file that should be uploaded.
      - filename (optional). Name of the file after upload.
      - description (optional). Description of the file.
      - content_type (optional). Content type of the file.

    :type uploads: list or tuple
    :return: True

.. code-block:: python

    >>> redmine.wiki_page.update('Foo', project_id='vacation', title='FooBar', text='foo', parent_title='Yada', comments='bar', uploads=[{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.WikiPage
    :noindex:

    Saves the current state of a wiki page resource to the Redmine. Fields that can
    be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> wiki_page = redmine.wiki_page.get('Foo', project_id='vacation')
    >>> wiki_page.title = 'Bar'
    >>> wiki_page.text = 'bar'
    >>> wiki_page.parent_title = 'Yada'
    >>> wiki_page.comments = 'changed foo to bar'
    >>> wiki_page.uploads = [{'path': '/absolute/path/to/file'}, {'path': '/absolute/path/to/file2'}]
    >>> wiki_page.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single wiki page resource from the Redmine by it's title.

    :param string resource_id: (required). Title of the wiki page.
    :param project_id: (required). Id or identifier of wiki page's project.
    :type project_id: integer or string
    :return: True

.. code-block:: python

    >>> redmine.wiki_page.delete('Foo', project_id=1)
    True
