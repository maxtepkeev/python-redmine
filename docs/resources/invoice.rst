Invoice
=======

.. versionadded:: 2.4.0

Requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3.

Manager
-------

All operations on the Invoice resource are provided by its manager. To get access to it
you have to call ``redmine.invoice`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Invoice resource with given fields and saves it to the Invoices plugin.

   :param string number: (required). Invoice number.
   :param project_id: (required). Id or identifier of invoice's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (required). Invoice status id:

    - 0 - estimate
    - 1 - draft
    - 2 - sent
    - 3 - paid
    - 4 - cancelled

   :param invoice_date: (required). Date when invoice is issued.
   :type invoice_date: string or date object
   :param string subject: (optional). Invoice subject.
   :param int contact_id: (optional). Invoice contact id.
   :param int assigned_to_id: (optional). Invoice will be assigned to this user id.
   :param string order_number: (optional). Invoice order number.
   :param bool is_recurring: (optional). Whether invoice is recurring.
   :param string recurring_period:
    .. raw:: html

       (optional). Invoice recurring period:

    - 1week - weekly
    - 2week - every 2 weeks
    - 1month - monthly
    - 2month - every 2 months
    - 3month - every 3 months
    - 6month - every 6 months
    - 1year - yearly

   :param int recurring_action:
    .. raw:: html

       (optional). Invoice recurring action:

    - 0 - create draft
    - 1 - send to client

   :param int recurring_occurrences: (optional). Invoice recurring occurrences.
   :param due_date: (optional). Invoice should be payed by this date.
   :type due_date: string or date object
   :param int discount: (optional). Invoice percentage discount.
   :param string currency: (optional). Invoice currency.
   :param int template_id: (optional). Invoice template id.
   :param string language: (optional). Invoice language.
   :param string description: (optional). Invoice description.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list lines_attributes:
    .. raw:: html

       (optional). Invoice lines as [{'': ''}, ...], accepted keys are:

    - description (required). Product description.
    - position (optional). Position of the line among other invoice lines.
    - quantity (optional). Product quantity.
    - product_id (optional). ID of the product.
    - tax (optional). Tax in percentage.
    - price (optional). Price of the product.
    - units (optional). Product amount.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> invoice = redmine.invoice.create(
   ...     number='INV-001',
   ...     project_id='invoices',
   ...     status_id=1,
   ...     invoice_date='2023-01-11',
   ...     subject='invoice subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     due_date='2023-01-13',
   ...     discount=20,
   ...     currency='USD',
   ...     template_id=7,
   ...     language='en',
   ...     description='invoice description',
   ...     order_number='ON-0001',
   ...     is_recurring=True,
   ...     recurring_period='6month',
   ...     recurring_action=1,
   ...     recurring_occurrences=3,
   ...     lines_attributes=[{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'units': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> invoice
   <redminelib.resources.Invoice #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Invoice resource, but saves it to the Invoices plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> invoice = redmine.invoice.new()
   >>> invoice.number = 'INV-001'
   >>> invoice.project_id = 'invoices'
   >>> invoice.status_id = 1
   >>> invoice.invoice_date = '2023-01-11'
   >>> invoice.subject = 'invoice subject'
   >>> invoice.contact_id = 3
   >>> invoice.assigned_to_id = 12
   >>> invoice.due_date = '2023-01-13'
   >>> invoice.discount = 20
   >>> invoice.currency = 'USD'
   >>> invoice.template_id = 7
   >>> invoice.language = 'en'
   >>> invoice.description = 'invoice description'
   >>> invoice.order_number = 'ON-0001'
   >>> invoice.is_recurring = True
   >>> invoice.recurring_period = '6month'
   >>> invoice.recurring_action = 1
   >>> invoice.recurring_occurrences = 3
   >>> invoice.lines_attributes = [{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'units': '2'}]
   >>> invoice.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> invoice.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> invoice.save()
   <redminelib.resources.Invoice #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Invoice resource from the Invoices plugin by its id.

   :param int resource_id: (required). Id of the invoice.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> invoice = redmine.invoice.get(123)
   >>> invoice
   <redminelib.resources.Invoice #123>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Invoice resources from the Invoices plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> invoices = redmine.invoice.all(limit=50)
   >>> invoices
   <redminelib.resultsets.ResourceSet object with Invoice resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Invoice resources that match the given lookup parameters.

   :param project_id: (optional). Id or identifier of invoice's project.
   :type project_id: int or string
   :param int assigned_to_id: (optional). Get invoices which are assigned to this user id.
   :param int query_id: (optional). Get invoices for the given query id.
   :param int status_id: (optional). Get invoices which have this status id.
   :param int contact_id: (optional). Get invoices for the given contact id.
   :param int author_id: (optional). Get invoices created by given author id.
   :param bool recurring: (optional). Whether invoice is recurring.
   :param due_date: (optional). Get invoices that should be payed by this date.
   :type due_date: string or date object
   :param invoice_date: (optional). Get invoices issued on the given date.
   :type invoice_date: string or date object
   :param string currency: (optional). Get invoices which have the given currency.
   :param string search: (optional). Get invoices with given search string.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> invoices = redmine.invoice.filter(project_id='invoices', assigned_to_id=123, status_id=1, search='INV', recurring=True)
   >>> invoices
   <redminelib.resultsets.ResourceSet object with Invoice resources>

.. hint::

   You can also get invoices from a Project, User, Contact and CrmQuery resource objects directly using
   ``invoices`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('invoices')
      >>> project.invoices
      <redminelib.resultsets.ResourceSet object with Invoice resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an Invoice resource and saves them to the Invoices plugin.

   :param int resource_id: (required). Invoice id.
   :param string number: (optional). Invoice number.
   :param project_id: (optional). Id or identifier of invoice's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (optional). Invoice status id:

    - 0 - estimate
    - 1 - draft
    - 2 - sent
    - 3 - paid
    - 4 - cancelled

   :param invoice_date: (optional). Date when invoice is issued.
   :type invoice_date: string or date object
   :param string subject: (optional). Invoice subject.
   :param int contact_id: (optional). Invoice contact id.
   :param int assigned_to_id: (optional). Invoice will be assigned to this user id.
   :param string order_number: (optional). Invoice order number.
   :param bool is_recurring: (optional). Whether invoice is recurring.
   :param string recurring_period:
    .. raw:: html

       (optional). Invoice recurring period:

    - 1week - weekly
    - 2week - every 2 weeks
    - 1month - monthly
    - 2month - every 2 months
    - 3month - every 3 months
    - 6month - every 6 months
    - 1year - yearly

   :param int recurring_action:
    .. raw:: html

       (optional). Invoice recurring action:

    - 0 - create draft
    - 1 - send to client

   :param int recurring_occurrences: (optional). Invoice recurring occurrences.
   :param due_date: (optional). Invoice should be payed by this date.
   :type due_date: string or date object
   :param int discount: (optional). Invoice percentage discount.
   :param string currency: (optional). Invoice currency.
   :param int template_id: (optional). Invoice template id.
   :param string language: (optional). Invoice language.
   :param string description: (optional). Invoice description.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param list lines_attributes:
    .. raw:: html

       (optional). Invoice lines as [{'': ''}, ...], accepted keys are:

    - description (required). Product description.
    - position (optional). Position of the line among other invoice lines.
    - quantity (optional). Product quantity.
    - product_id (optional). ID of the product.
    - tax (optional). Tax in percentage.
    - price (optional). Price of the product.
    - units (optional). Product amount.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> redmine.invoice.update(
   ...     123,
   ...     number='INV-001',
   ...     project_id='invoices',
   ...     status_id=1,
   ...     invoice_date='2023-01-11',
   ...     subject='invoice subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     due_date='2023-01-13',
   ...     discount=20,
   ...     currency='USD',
   ...     template_id=7,
   ...     language='en',
   ...     description='invoice description',
   ...     order_number='ON-0001',
   ...     is_recurring=True,
   ...     recurring_period='6month',
   ...     recurring_action=1,
   ...     recurring_occurrences=3,
   ...     lines_attributes=[{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'units': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Invoice
   :noindex:

   Saves the current state of an Invoice resource to the Invoices plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> invoice = redmine.invoice.get(123)
   >>> invoice.number = 'INV-001'
   >>> invoice.project_id = 'invoices'
   >>> invoice.status_id = 1
   >>> invoice.invoice_date = '2023-01-11'
   >>> invoice.subject = 'invoice subject'
   >>> invoice.contact_id = 3
   >>> invoice.assigned_to_id = 12
   >>> invoice.due_date = '2023-01-13'
   >>> invoice.discount = 20
   >>> invoice.currency = 'USD'
   >>> invoice.template_id = 7
   >>> invoice.language = 'en'
   >>> invoice.description = 'invoice description'
   >>> invoice.order_number = 'ON-0001'
   >>> invoice.is_recurring = True
   >>> invoice.recurring_period = '6month'
   >>> invoice.recurring_action = 1
   >>> invoice.recurring_occurrences = 3
   >>> invoice.lines_attributes = [{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'units': '2'}]
   >>> invoice.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> invoice.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> invoice.save()
   <redminelib.resources.Invoice #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> invoice = redmine.invoice.get(123).save(
   ...     number='INV-001',
   ...     project_id='invoices',
   ...     status_id=1,
   ...     invoice_date='2023-01-11',
   ...     subject='invoice subject',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     due_date='2023-01-13',
   ...     discount=20,
   ...     currency='USD',
   ...     template_id=7,
   ...     language='en',
   ...     description='invoice description',
   ...     order_number='ON-0001',
   ...     is_recurring=True,
   ...     recurring_period='6month',
   ...     recurring_action=1,
   ...     recurring_occurrences=3,
   ...     lines_attributes=[{'position': 1, 'quantity': '3', 'description': 'product description', 'product_id': 1, 'tax': '10', 'price': '5', 'units': '2'}],
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> invoice
   <redminelib.resources.Invoice #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Invoice resource from the Invoices plugin by its id.

   :param int resource_id: (required). Invoice id.
   :return: True

.. code-block:: python

   >>> redmine.invoice.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Invoice
   :noindex:

   Deletes current Invoice resource object from the Invoices plugin.

   :return: True

.. code-block:: python

   >>> invoice = redmine.invoice.get(1)
   >>> invoice.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resources.Invoice
   :noindex:

   Exports Invoice resource in one of the following formats: pdf

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> invoice = redmine.invoice.get(123)
   >>> invoice.export('pdf', savepath='/home/jsmith')
   '/home/jsmith/123.pdf'

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Invoice resources in one of the following formats: csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> invoices = redmine.invoice.all()
   >>> invoices.export('csv', savepath='/home/jsmith', filename='invoices.csv')
   '/home/jsmith/invoices.csv'
