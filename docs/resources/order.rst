Order
=====

.. versionadded:: 2.5.0

Requires Pro Edition and `Products plugin <https://www.redmineup.com/pages/plugins/products>`_ >= 2.1.5.

Manager
-------

All operations on the Order resource are provided by its manager. To get access to it
you have to call ``redmine.order`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Order resource with given fields and saves it to the Products plugin.

   :param string number: (required). Order number.
   :param int project_id: (required). Order project id.
   :param int status_id: (required). Order status id.
   :param order_date: (required). Date and time of the order.
   :type order_date: string or datetime object
   :param string subject: (optional). Order subject.
   :param int contact_id: (optional). Order contact id.
   :param int assigned_to_id: (optional). Order will be assigned to this user id.
   :param string currency: (optional). Order currency.
   :param string description: (optional). Order description.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list lines_attributes:
    .. raw:: html

       (optional). Order lines as [{'': ''}, ...], accepted keys are:

    - position (optional). Position of the line among other order lines.
    - product_id (optional). ID of the product.
    - description (required). Product description.
    - quantity (optional). Product quantity.
    - price (optional). Price of the product.
    - tax (optional). Tax in percentage.
    - discount (optional). Discount in percentage.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> order = redmine.order.create(
   ...     number='O-001',
   ...     project_id=12,
   ...     status_id=1,
   ...     order_date='2023-01-11',
   ...     subject='order subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     currency='USD',
   ...     description='order description',
   ...     lines_attributes=[{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'discount': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> order
   <redminelib.resources.Order #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Order resource, but saves it to the Products plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> order = redmine.order.new()
   >>> order.number = 'O-001'
   >>> order.project_id = 12
   >>> order.status_id = 1
   >>> order.order_date = '2023-01-11'
   >>> order.subject = 'order subject'
   >>> order.contact_id = 3
   >>> order.assigned_to_id = 12
   >>> order.currency = 'USD'
   >>> order.description = 'order description'
   >>> order.lines_attributes = [{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'discount': '2'}]
   >>> order.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> order.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> order.save()
   <redminelib.resources.Order #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Order resource from the Products plugin by its id.

   :param int resource_id: (required). Id of the order.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - lines

   :return: :ref:`Resource` object

.. code-block:: python

   >>> order = redmine.order.get(123, include=['lines'])
   >>> order
   <redminelib.resources.Order #123>

.. hint::

   Order resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with an Order
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Order resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> order = redmine.order.get(123)
      >>> order.lines

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Order resources from the Products plugin.

   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - lines

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> orders = redmine.order.all(limit=50, include=['lines'])
   >>> orders
   <redminelib.resultsets.ResourceSet object with Order resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Order resources that match the given lookup parameters.

   :param int project_id: (optional). Get orders for the given project id.
   :param int assigned_to_id: (optional). Get orders which are assigned to this user id.
   :param int status_id: (optional). Get orders which have this status id.
   :param int contact_id: (optional). Get orders for the given contact id.
   :param int author_id: (optional). Get orders created by given author id.
   :param string number: (optional). Get orders for the given number.
   :param string amount: (optional). Get orders which have given amount.
   :param completed_date: (optional). Get orders that should be completed by this date.
   :type completed_date: string or date object
   :param order_date: (optional). Get orders created on the given date.
   :type order_date: string or date object
   :param string sort:
    .. raw:: html

       (optional). Column to sort, append :desc to invert the order:

    - order_date
    - status_id
    - created_at
    - updated_at

   :param string search: (optional). Get orders for the given search string.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> orders = redmine.order.filter(project_id=12, assigned_to_id=123, status_id=1, search='SO', sort='order_date:desc')
   >>> orders
   <redminelib.resultsets.ResourceSet object with Order resources>

.. hint::

   You can also get orders from a Project, User and Contact resource objects directly using
   ``orders`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('products')
      >>> project.orders
      <redminelib.resultsets.ResourceSet object with Order resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an Order resource and saves them to the Products plugin.

   :param int resource_id: (required). Order id.
   :param string number: (optional). Order number.
   :param int project_id: (optional). Order project id.
   :param int status_id: (optional). Order status id.
   :param order_date: (optional). Date and time of the order.
   :type order_date: string or datetime object
   :param string subject: (optional). Order subject.
   :param int contact_id: (optional). Order contact id.
   :param int assigned_to_id: (optional). Order will be assigned to this user id.
   :param string currency: (optional). Order currency.
   :param string description: (optional). Order description.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list lines_attributes:
    .. raw:: html

       (optional). Order lines as [{'': ''}, ...], accepted keys are:

    - id (optional). If not set, a new line will be created.
    - position (optional). Position of the line among other order lines.
    - product_id (optional). ID of the product.
    - description (optional). Product description.
    - quantity (optional). Product quantity.
    - price (optional). Price of the product.
    - tax (optional). Tax in percentage.
    - discount (optional). Discount in percentage.
    - _destroy (optional). Whether to delete line with a specified id.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> redmine.order.update(
   ...     123,
   ...     number='O-001',
   ...     project_id=12,
   ...     status_id=1,
   ...     order_date='2023-01-11',
   ...     subject='order subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     currency='USD',
   ...     description='order description',
   ...     lines_attributes=[{'id': 1, '_destroy': True}, {'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'discount': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Order
   :noindex:

   Saves the current state of an Order resource to the Products plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> order = redmine.order.get(123)
   >>> order.number = 'O-001'
   >>> order.project_id = 12
   >>> order.status_id = 1
   >>> order.order_date = '2023-01-11'
   >>> order.subject = 'order subject'
   >>> order.contact_id = 3
   >>> order.assigned_to_id = 12
   >>> order.currency = 'USD'
   >>> order.description = 'order description'
   >>> order.lines_attributes = [{'id': 1, '_destroy': True}, {'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'discount': '2'}]
   >>> order.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> order.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> order.save()
   <redminelib.resources.Order #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> order = redmine.order.get(123).save(
   ...     number='O-001',
   ...     project_id=12,
   ...     status_id=1,
   ...     order_date='2023-01-11',
   ...     subject='order subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     currency='USD',
   ...     description='order description',
   ...     lines_attributes=[{'id': 1, '_destroy': True}, {'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'discount': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> order
   <redminelib.resources.Order #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Order resource from the Products plugin by its id.

   :param int resource_id: (required). Order id.
   :return: True

.. code-block:: python

   >>> redmine.order.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Order
   :noindex:

   Deletes current Order resource object from the Products plugin.

   :return: True

.. code-block:: python

   >>> order = redmine.order.get(1)
   >>> order.delete()
   True

Export
------

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Order resources in one of the following formats: csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> orders = redmine.order.all()
   >>> orders.export('csv', savepath='/home/jsmith', filename='orders.csv')
   '/home/jsmith/orders.csv'
