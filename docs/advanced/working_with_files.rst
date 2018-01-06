Working with Files
==================

It is possible to use Python-Redmine to upload/download files to/from Redmine. This document
describes low-level interfaces that Python-Redmine provides, in most cases they shouldn't be
used directly and high-level interfaces, e.g. ``uploads`` parameter in :doc:`../resources/issue`
resource or ``download()`` method in :doc:`../resources/attachment` resource should be used
instead. To get access to these low-level interfaces you have to call either ``redmine.upload()``
or ``redmine.download()`` where ``redmine`` is a configured redmine object. See the
:doc:`../configuration` about how to configure redmine object.

Upload
------

.. py:method:: upload(f, close=True)
   :module: redminelib.Redmine
   :noindex:

   Uploads file from filepath / filestream to Redmine and returns an assigned token.

   :param string f: (required). Path to the file / filestream that will be uploaded.
   :param bool close: (optional). Whether to close the file / filestream after it will be uploaded.
   :return: Token string

.. code-block:: python

   >>> token = redmine.upload('/usr/local/image.jpg')
   >>> token
   '7167.ed1ccdb093229ca1bd0b043618d88743'

Download
--------

.. py:method:: download(url, savepath=None, filename=None, params=None)
   :module: redminelib.Redmine
   :noindex:

   Downloads file from Redmine and saves it to savepath or returns a response directly
   for maximum control over file processing.

   :param string url: (required). URL of the file that will be downloaded.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :param dict params: (optional). Params to send in the query string.
   :return: string or `requests.Response <http://docs.python-requests.org/en/latest/api/#requests.Response>`_ object

If a ``savepath`` argument is provided, then a file will be saved into the provided path with
it's own name, if a ``filename`` argument is provided together with the ``savepath`` argument,
then a file will be saved into the provided path under the provided name and the resulting path
to the file will be returned.

.. code-block:: python

   >>> filepath = redmine.download('https://redmine.url/foobar.jpg', savepath='/usr/local', filename='image.jpg')
   >>> filepath
   '/usr/local/image.jpg'

If only a ``url`` argument is provided, then a `requests.Response <http://docs.python-requests.org/en/
latest/api/#requests.Response>`_ object will be returned which can be used for a maximum control over
file processing. For example, you can call a `iter_content() <http://docs.python-requests.org/en/latest/
api/#requests.Response.iter_content>`_ method with the needed arguments to have full control over the
content reading process:

.. code-block:: python

   >>> response = redmine.download('https://redmine.url/foobar.jpg')
   >>> for chunk in response.iter_content(chunk_size=1024):
           # do something with chunk
