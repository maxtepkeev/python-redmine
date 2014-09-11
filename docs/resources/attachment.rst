Attachment
==========

Supported by Redmine starting from version 1.3

Manager
-------

All operations on the attachment resource are provided via it's manager. To get access to it
you have to call ``redmine.attachment`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine. Some resources support adding attachments via it's create/update methods, e.g. issue.

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single attachment resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the attachment.
    :return: Attachment resource object

.. code-block:: python

    >>> attachment = redmine.attachment.get(76905)
    >>> attachment
    <redmine.resources.Attachment #76905 "1(a).png">

.. hint::

    Attachment can be easily downloaded via the provided ``download()`` method which is a proxy
    to the ``redmine.download()`` method which provides several options to control the saving
    process (see `docs <http://python-redmine.readthedocs.org/advanced/working_with_files.html#
    download>`__ for details):

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

Not supported by Redmine
