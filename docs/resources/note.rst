Note
====

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the Note resource are provided by its manager. To get access to
it you have to call ``redmine.note`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

.. versionadded:: 2.4.0

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Note resource with given fields and saves it to the CRM plugin.

   :param project_id: (required). Id or identifier of note's project.
   :type project_id: int or string
   :param string source_type: (required). Resource type, note will belong to: Contact or Deal.
   :param int source_id: (required). Id of the resource, note will belong to, depending on the chosen source_type.
   :param string content: (optional). Note content.
   :param string subject: (optional). Note subject.
   :param int type_id:
    .. raw:: html

       (optional). Note type id (will default to Note if not set):

    - 0 - email
    - 1 - call
    - 2 - meeting

   :param created_on: (optional). Date when note was created.
   :type created_on: string or date object
   :param string note_time: (optional). Time when note was created.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> note = redmine.note.create(
   ...     project_id='vacation',
   ...     source_type='Contact',
   ...     source_id=12,
   ...     subject='note subject',
   ...     content='note content',
   ...     type_id=3,
   ...     created_on='2023-01-10',
   ...     note_time='11:11',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> note
   <redminelib.resources.Note #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Note resource but saves it to the CRM plugin only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> note = redmine.note.new()
   >>> note.project_id = 'vacation'
   >>> note.source_type = 'Contact'
   >>> note.source_id = 12
   >>> note.subject = 'note subject'
   >>> note.content = 'note content'
   >>> note.type_id = 3
   >>> note.created_on = '2023-01-10'
   >>> note.note_time = '11:11'
   >>> note.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> note.save()
   <redminelib.resources.Note #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Note resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the note.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> note = redmine.note.get(12345)
   >>> note
   <redminelib.resources.Note #12345>

all
+++

Not supported by CRM plugin

filter
++++++

Not supported by CRM plugin

Update methods
--------------

.. versionadded:: 2.4.0

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Note resource and saves them to the CRM plugin.

   :param int resource_id: (required). Note id.
   :param string content: (optional). Note content.
   :param string subject: (optional). Note subject.
   :param int type_id:
    .. raw:: html

       (optional). Note type id (will default to Note if not set):

    - 0 - email
    - 1 - call
    - 2 - meeting

   :param created_on: (optional). Date when note was created.
   :type created_on: string or date object
   :param string note_time: (optional). Time when note was created.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> redmine.note.update(
   ...     123,
   ...     subject='note subject',
   ...     content='note content',
   ...     type_id=3,
   ...     created_on='2023-01-10',
   ...     note_time='11:11',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Note
   :noindex:

   Saves the current state of a Note resource to the CRM plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> note = redmine.note.get(123)
   >>> note.subject = 'note subject'
   >>> note.content = 'note content'
   >>> note.type_id = 3
   >>> note.created_on = '2023-01-10'
   >>> note.note_time = '11:11'
   >>> note.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> note.save()
   <redminelib.resources.Note #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> note = redmine.note.get(123).save(
   ...     subject='note subject',
   ...     content='note content',
   ...     type_id=3,
   ...     created_on='2023-01-10',
   ...     note_time='11:11',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> note
   <redminelib.resources.Note #123>

Delete methods
--------------

.. versionadded:: 2.4.0

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Note resource from the CRM plugin by its id.

   :param int resource_id: (required). Note id.
   :return: True

.. code-block:: python

   >>> redmine.note.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Note
   :noindex:

   Deletes current Note resource object from the CRM plugin.

   :return: True

.. code-block:: python

   >>> note = redmine.note.get(1)
   >>> note.delete()
   True

Export
------

Not supported by CRM plugin
