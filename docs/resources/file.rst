File
====

Supported by Redmine starting from version 3.4

Manager
-------

All operations on the File resource are provided by its manager. To get access to it
you have to call ``redmine.file`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.FileManager
   :noindex:

   Creates new File resource with given fields and saves it to the Redmine.

   :param project_id: (required). Id or identifier of file's project.
   :type project_id: int or string
   :param string path: (required). Absolute file path or file-like object that should be uploaded.
   :param string filename: (optional). Name of the file after upload.
   :param string description: (optional). Description of the file.
   :param string content_type: (optional). Content type of the file.
   :param int version_id: (optional). File's version id.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> f = redmine.file.create(
   ...     project_id='vacation',
   ...     path='/absolute/path/to/file',
   ...     filename='foo.txt',
   ...     description='foobar',
   ...     content_type='text/plain',
   ...     version_id=1
   ... )
   >>> f
   <redminelib.resources.File #1 "foo.txt">

new
+++

.. py:method:: new()
   :module: redminelib.managers.FileManager
   :noindex:

   Creates new empty File resource but saves it to the Redmine only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> f = redmine.file.new()
   >>> f.project_id = 'vacation'
   >>> f.path = '/absolute/path/to/file'
   >>> f.filename = 'foo.txt'
   >>> f.description = 'foobar'
   >>> f.content_type = 'text/plain'
   >>> f.version_id = 1
   >>> f.save()
   <redminelib.resources.File #1 "foo.txt">

.. warning::

   Redmine's File API doesn't return a file object after create operation. Due to the fact that it goes
   against the behaviour of all other API endpoints, Python-Redmine has to do some tricks under the hood
   to return a resource object with at least an ``id`` attribute. That doesn't involve any additional API
   requests. In most cases that should be enough, but if it's not and a complete resource object is needed,
   one has to use a ``refresh()`` method to make an additional query to the Redmine to retrieve a complete
   resource:

   .. code-block:: python

      >>> f = redmine.file.new()
      >>> f.project_id = 'vacation'
      >>> f.path = '/absolute/path/to/file'
      >>> f.filename = 'foo.txt'
      >>> f.description = 'foobar'
      >>> f.content_type = 'text/plain'
      >>> f.version_id = 1
      >>> f.save()
      <redminelib.resources.File #1>
      >>> f.refresh()
      >>> f
      <redminelib.resources.File #1 "foo.txt">

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.FileManager
   :noindex:

   Returns single File resource from Redmine by its id.

   :param int resource_id: (required). Id of the file.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> f = redmine.file.get(12345)
   >>> f
   <redminelib.resources.File #12345 "foo.txt">

.. hint::

   Files can be easily downloaded via the provided ``download()`` method which is a proxy
   to the ``redmine.download()`` method which provides several options to control the saving
   process (see `docs <https://python-redmine.com/advanced/working_with_files.html#
   download>`_ for details):

   .. code-block:: python

      >>> f = redmine.file.get(12345)
      >>> filepath = f.download(savepath='/usr/local/', filename='image.jpg')
      >>> filepath
      '/usr/local/image.jpg'

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.FileManager
   :noindex:

   Returns File resources that match the given lookup parameters.

   :param project_id: (optional). Get files from the project with given id.
   :type project_id: int or string
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> files = redmine.file.filter(project_id='vacation')
   >>> files
   <redminelib.resultsets.ResourceSet object with File resources>

.. hint::

   You can also get files from a Project resource object directly using ``files`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.files
      <redminelib.resultsets.ResourceSet object with File resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.FileManager
   :noindex:

   Updates values of given fields of a File resource and saves them to the Redmine.

   :param int resource_id: (required). File id.
   :param string filename: (optional). File name.
   :param string description: (optional). File description.
   :param string content_type: (optional). File content-type.
   :return: True

.. code-block:: python

   >>> redmine.file.update(
   ...     1,
   ...     filename='foo.txt',
   ...     description='foobar',
   ...     content_type='text/plain'
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.File
   :noindex:

   Saves the current state of a File resource to the Redmine. Attrs that can
   be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> f = redmine.file.get(1)
   >>> f.filename = 'foo.txt'
   >>> f.description = 'foobar'
   >>> f.content_type = 'text/plain'
   >>> f.save()
   <redminelib.resources.File #1 "foo.txt">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> f = redmine.file.get(1).save(
   ...     filename='foo.txt',
   ...     description='foobar',
   ...     content_type='text/plain'
   ... )
   >>> f
   <redminelib.resources.File #1 "foo.txt">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.FileManager
   :noindex:

   Deletes single File resource from Redmine by its id.

   :param int resource_id: (required). File id.
   :return: True

.. code-block:: python

   >>> redmine.file.delete(12345)
   True

.. py:method:: delete()
   :module: redminelib.resources.File
   :noindex:

   Deletes current File resource object from Redmine.

   :return: True

.. code-block:: python

   >>> f = redmine.file.get(12345)
   >>> f.delete()
   True

Export
------

Export functionality doesn't make sense for files as they can be downloaded
