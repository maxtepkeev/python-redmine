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

Not supported by Redmine

Delete methods
--------------

.. versionadded:: 2.0.0

Requires Redmine >= 3.3.0

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
