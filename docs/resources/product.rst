Product
=======

.. versionadded:: 2.5.0

Requires Pro Edition and `Products plugin <https://www.redmineup.com/pages/plugins/products>`_ >= 2.1.5.

Manager
-------

All operations on the Product resource are provided by its manager. To get access to it
you have to call ``redmine.product`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Product resource with given fields and saves it to the Products plugin.

   :param string name: (required). Product name.
   :param project_id: (required). Id or identifier of product's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (optional). Product status id:

    - 1 - active
    - 2 - inactive

   :param string code: (optional). Product code.
   :param string price: (optional). Product price.
   :param string currency: (optional). Product currency.
   :param int category_id: (optional). Product category id.
   :param string description: (optional). Product description.
   :param list tag_list: (optional). List of tags.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param dict image:
    .. raw:: html

       (optional). Image to be used for the product as dict, accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Required if a file-like object is provided.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> product = redmine.product.create(
   ...     project_id='products',
   ...     name='foobar',
   ...     status_id=2,
   ...     code='P-001',
   ...     price='9.99',
   ...     currency='USD',
   ...     category_id=8,
   ...     description='product description',
   ...     tag_list=['foo', 'bar'],
   ...     custom_fields=[{'id': 1, 'value': '11'}],
   ...     image={'path': '/absolute/path/to/file.jpg'},
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> product
   <redminelib.resources.Product #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Product resource, but saves it to the Products plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> product = redmine.product.new()
   >>> product.project_id = 'products'
   >>> product.name = 'foobar'
   >>> product.status_id = 2
   >>> product.code = 'P-001'
   >>> product.price = '9.99'
   >>> product.currency = 'USD'
   >>> product.category_id = 8
   >>> product.description = 'product description'
   >>> product.tag_list = ['foo', 'bar']
   >>> product.custom_fields = [{'id': 1, 'value': '11'}]
   >>> product.image = {'path': '/absolute/path/to/file.jpg'}
   >>> product.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> product.save()
   <redminelib.resources.Product #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Product resource from the Products plugin by its id.

   :param int resource_id: (required). Id of the product.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - attachments

   :return: :ref:`Resource` object

.. code-block:: python

   >>> product = redmine.product.get(123, include=['attachments'])
   >>> product
   <redminelib.resources.Product #123>

.. hint::

   Product resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Product
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Product resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> product = redmine.product.get(123)
      >>> product.attachments
      <redminelib.resultsets.ResourceSet object with Attachment resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Product resources from the Products plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> products = redmine.product.all(limit=50)
   >>> products
   <redminelib.resultsets.ResourceSet object with Product resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Product resources that match the given lookup parameters.

   :param project_id: (optional). Get products for the given project id.
   :type project_id: int or string
   :param int author_id: (optional). Get products created by given author id.
   :param int status_id:
    .. raw:: html

       (optional). Get products for the given status id:

    - 1 - active
    - 2 - inactive

   :param int category_id: (optional). Get products for the given category id.
   :param string code: (optional). Get products for the given code.
   :param string name: (optional). Get products for the given name.
   :param string price: (optional). Get products for the given price.
   :param string sort:
    .. raw:: html

       (optional). Column to sort, append :desc to invert the order:

    - code
    - name
    - created_at
    - updated_at

   :param string search: (optional). Get products for the given search string.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> products = redmine.product.filter(project_id='products', author_id=123, status_id=1, search='prod', sort='created_at:desc')
   >>> products
   <redminelib.resultsets.ResourceSet object with Product resources>

.. hint::

   You can also get products from a Project, User and CrmQuery resource objects directly using
   ``products`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('products')
      >>> project.products
      <redminelib.resultsets.ResourceSet object with Product resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Product resource and saves them to the Products plugin.

   :param int resource_id: (required). Product id.
   :param string name: (optional). Product name.
   :param project_id: (optional). Id or identifier of product's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (optional). Product status id:

    - 1 - active
    - 2 - inactive

   :param string code: (optional). Product code.
   :param string price: (optional). Product price.
   :param string currency: (optional). Product currency.
   :param int category_id: (optional). Product category id.
   :param string description: (optional). Product description.
   :param list tag_list: (optional). List of tags.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param dict image:
    .. raw:: html

       (optional). Image to be used for the product as dict, accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Required if a file-like object is provided.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> redmine.product.update(
   ...     123,
   ...     project_id='products',
   ...     name='foobar',
   ...     status_id=2,
   ...     code='P-001',
   ...     price='9.99',
   ...     currency='USD',
   ...     category_id=8,
   ...     description='product description',
   ...     tag_list=['foo', 'bar'],
   ...     custom_fields=[{'id': 1, 'value': '11'}],
   ...     image={'path': '/absolute/path/to/file.jpg'},
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Product
   :noindex:

   Saves the current state of a Product resource to the Products plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> product = redmine.product.get(123)
   >>> product.project_id = 'products'
   >>> product.name = 'foobar'
   >>> product.status_id = 2
   >>> product.code = 'P-001'
   >>> product.price = '9.99'
   >>> product.currency = 'USD'
   >>> product.category_id = 8
   >>> product.description = 'product description'
   >>> product.tag_list = ['foo', 'bar']
   >>> product.custom_fields = [{'id': 1, 'value': '11'}]
   >>> product.image = {'path': '/absolute/path/to/file.jpg'}
   >>> product.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> product.save()
   <redminelib.resources.Product #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> product = redmine.product.get(123).save(
   ...     project_id='products',
   ...     name='foobar',
   ...     status_id=2,
   ...     code='P-001',
   ...     price='9.99',
   ...     currency='USD',
   ...     category_id=8,
   ...     description='product description',
   ...     tag_list=['foo', 'bar'],
   ...     custom_fields=[{'id': 1, 'value': '11'}],
   ...     image={'path': '/absolute/path/to/file.jpg'},
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> product
   <redminelib.resources.Product #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Product resource from the Products plugin by its id.

   :param int resource_id: (required). Product id.
   :return: True

.. code-block:: python

   >>> redmine.product.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Product
   :noindex:

   Deletes current Product resource object from the Products plugin.

   :return: True

.. code-block:: python

   >>> product = redmine.product.get(1)
   >>> product.delete()
   True

Export
------

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Product resources in one of the following formats: csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> products = redmine.product.all()
   >>> products.export('csv', savepath='/home/jsmith', filename='products.csv')
   '/home/jsmith/products.csv'
