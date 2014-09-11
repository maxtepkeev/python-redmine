Working with Files
==================

It is possible to use Python Redmine to upload/download files to/from Redmine. This document
describes low-level interfaces that Python Redmine provides, in most cases they shouldn't be
used directly and high-level interfaces, e.g. ``uploads`` parameter in :doc:`../resources/issue`
resource or ``download()`` method in :doc:`../resources/attachment` resource should be used
instead. To get access to these low-level interfaces you have to call either ``redmine.upload()``
or ``redmine.download()`` where ``redmine`` is a configured redmine object. See the
:doc:`../configuration` about how to configure redmine object.

Upload
------

.. versionadded:: 0.2.0

.. py:method:: upload(filepath)
    :module: redmine.Redmine
    :noindex:

    Uploads file from filepath to Redmine and returns an assigned token which can then be used
    to attach the uploaded file to some resource, e.g. Issue.

    :param string filepath: (optional). Local path to the file which should be uploaded.
    :return: Token string

.. code-block:: python

    >>> token = redmine.upload('/usr/local/image.jpg')
    >>> token
    '7167.ed1ccdb093229ca1bd0b043618d88743'

Download
--------

.. versionadded:: 0.9.0

.. py:method:: download(url, savepath=None, filename=None)
    :module: redmine.Redmine
    :noindex:

    Downloads file from Redmine and saves it to savepath or returns it as bytes.

    :param string url: (required). A URL of the file which should be downloaded.
    :param string savepath: (optional). Local path where file should be saved.
    :param string filename: (optional). Filename which will be used for a file.
    :return: String or Method

If a ``savepath`` argument is provided, then a file will be saved into the provided path with
it's own name, if a ``filename`` argument is provided together with the ``savepath`` argument,
then a file will be saved into the provided path under the provided name and the resulting path
to the file will be returned.

.. code-block:: python

    >>> filepath = redmine.download('https://redmine.url/foobar.jpg', savepath='/usr/local/', filename='image.jpg')
    >>> filepath
    '/usr/local/image.jpg'

If only a ``url`` argument is provided, then a `iter_content <http://docs.python-requests.org/
en/latest/api/#requests.Response.iter_content>`_ method will be returned which you can call with
the needed arguments to have full control over the iteration over the response data.

.. code-block:: python

    >>> iter_content = redmine.download('https://redmine.url/foobar.jpg')
    >>> for chunk in iter_content(chunk_size=1024):
            # do something with chunk
