Attachment
==========

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the Attachment resource are provided by it's manager. To get access to it
you have to call ``redmine.attachment`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine. Some resources support adding attachments via it's create/update methods, e.g. Issue, WikiPage.

Read methods
------------

get
+++

.. py:method:: get(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Attachment resource from Redmine by it's id.

   :param int resource_id: (required). Id of the attachment.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> attachment = redmine.attachment.get(76905)
   >>> attachment
   <redminelib.resources.Attachment #76905 "1(a).png">

.. hint::

   Attachment can be easily downloaded via the provided ``download()`` method which is a proxy
   to the ``redmine.download()`` method which provides several options to control the saving
   process (see `docs <https://python-redmine.com/advanced/working_with_files.html#
   download>`_ for details):

   .. code-block:: python

      >>> attachment = redmine.attachment.get(76905)
      >>> filepath = attachment.download(savepath='/usr/local/', filename='image.jpg')
      >>> filepath
      '/usr/local/image.jpg'

all
+++

Not supported by Redmine

filter
++++++

Not supported by Redmine

Update methods
--------------

.. versionadded:: 2.1.0

Requires Redmine >= 3.4.0

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an Attachment resource and saves them to the Redmine.

   :param int resource_id: (required). Attachment id.
   :param string filename: (optional). File name.
   :param string description: (optional). File description.
   :param string content_type: (optional). File content-type.
   :return: True

.. code-block:: python

   >>> redmine.attachment.update(
   ...     1,
   ...     filename='foo.txt',
   ...     description='foobar',
   ...     content_type='text/plain'
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Attachment
   :noindex:

   Saves the current state of an Attachment resource to the Redmine. Attrs that can
   be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> attachment = redmine.attachment.get(1)
   >>> attachment.filename = 'foo.txt'
   >>> attachment.description = 'foobar'
   >>> attachment.content_type = 'text/plain'
   >>> attachment.save()
   <redminelib.resources.Attachment #1 "foo.txt">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> attachment = redmine.attachment.get(1).save(
   ...     filename='foo.txt',
   ...     description='foobar',
   ...     content_type='text/plain'
   ... )
   >>> attachment
   <redminelib.resources.Attachment #1 "foo.txt">

Delete methods
--------------

.. versionadded:: 2.0.0

Requires Redmine >= 3.3.0

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Attachment resource from Redmine by it's id.

   :param int resource_id: (required). Version id.
   :return: True

.. code-block:: python

   >>> redmine.attachment.delete(76905)
   True

.. py:method:: delete()
   :module: redminelib.resources.Attachment
   :noindex:

   Deletes current Attachment resource object from Redmine.

   :return: True

.. code-block:: python

   >>> attachment = redmine.attachment.get(76905)
   >>> attachment.delete()
   True

Export
------

Not supported by Redmine
