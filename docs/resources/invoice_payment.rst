Invoice Payment
===============

.. versionadded:: 2.4.0

Requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3.

Manager
-------

All operations on the InvoicePayment resource are provided by its manager. To get access to it
you have to call ``redmine.invoice_payment`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new InvoicePayment resource with given fields and saves it to the Invoices plugin.

   :param int invoice_id: (required). Invoice id.
   :param string amount: (required). Payment amount.
   :param payment_date: (required). Payment date.
   :type payment_date: string or date object
   :param string description: (optional). Payment description.

   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> payment = redmine.invoice_payment.create(
   ...     invoice_id=6,
   ...     amount='12.34',
   ...     payment_date='2023-01-11',
   ...     description='description',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> payment
   <redminelib.resources.InvoicePayment #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty InvoicePayment resource, but saves it to the Invoices plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> payment = redmine.invoice_payment.new()
   >>> payment.invoice_id = 6
   >>> payment.amount = '12.34'
   >>> payment.payment_date = '2023-01-11'
   >>> payment.description = 'description'
   >>> payment.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> payment.save()
   <redminelib.resources.InvoicePayment #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single InvoicePayment resource from the Invoices plugin by its id.

   :param int resource_id: (required). Id of the payment.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> payment = redmine.invoice_payment.get(123)
   >>> payment
   <redminelib.resources.InvoicePayment #123>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all InvoicePayment resources from the Invoices plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> payments = redmine.invoice_payment.all(limit=50)
   >>> payments
   <redminelib.resultsets.ResourceSet object with InvoicePayment resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns InvoicePayment resources that match the given lookup parameters.

   :param int invoice_id: (optional). Get payments for the given invoice id.
   :param int contact_id: (optional). Get payments for the given contact id.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> payments = redmine.invoice_payment.filter(invoice_id=1, contact_id=1)
   >>> payments
   <redminelib.resultsets.ResourceSet object with InvoicePayment resources>

.. hint::

   You can also get payments from an Invoice and Contact resource objects directly using
   ``payments`` relation:

   .. code-block:: python

      >>> invoice = redmine.invoice.get(123)
      >>> invoice.payments
      <redminelib.resultsets.ResourceSet object with InvoicePayment resources>

Update methods
--------------

Not supported by Invoices plugin

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single InvoicePayment resource from the Invoices plugin by its id.

   :param int resource_id: (required). Payment id.
   :param int invoice_id: (required). Invoice id which payment belongs to.
   :return: True

.. code-block:: python

   >>> redmine.invoice_payment.delete(123, invoice_id=1)
   True

.. py:method:: delete()
   :module: redminelib.resources.InvoicePayment
   :noindex:

   Deletes current InvoicePayment resource object from the Invoices plugin.

   :return: True

.. code-block:: python

   >>> payment = redmine.invoice_payment.get(123)
   >>> payment.delete()
   True

Export
------

Not supported by Invoices plugin
