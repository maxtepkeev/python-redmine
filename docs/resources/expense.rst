Expense
=======

.. versionadded:: 2.4.0

Requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_ >= 4.1.3.

Manager
-------

All operations on the Expense resource are provided by its manager. To get access to it
you have to call ``redmine.expense`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Expense resource with given fields and saves it to the Invoices plugin.

   :param project_id: (required). Id or identifier of expense's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (required). Expense status id:

    - 1 - draft
    - 2 - new
    - 3 - billed
    - 4 - paid

   :param expense_date: (required). Date when expense occurred.
   :type expense_date: string or date object
   :param string price: (optional). Expense amount.
   :param string currency: (optional). Expense currency.
   :param int contact_id: (optional). Expense contact id.
   :param int assigned_to_id: (optional). Expense will be assigned to this user id.
   :param bool is_billable: (optional). Whether expense is billable.
   :param int linked_issue_id: (optional). Issue id to be linked with this expense.
   :param string description: (optional). Expense description.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> expense = redmine.expense.create(
   ...     project_id='invoices',
   ...     status_id=2,
   ...     expense_date='2023-01-11',
   ...     price='13.56',
   ...     currency='USD',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     is_billable=True,
   ...     description='description',
   ...     linked_issue_id=557,
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> expense
   <redminelib.resources.Expense #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Expense resource, but saves it to the Invoices plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> expense = redmine.expense.new()
   >>> expense.project_id = 'invoices'
   >>> expense.status_id = 2
   >>> expense.expense_date = '2023-01-11'
   >>> expense.price = '13.56'
   >>> expense.currency = 'USD'
   >>> expense.contact_id = 3
   >>> expense.assigned_to_id = 12
   >>> expense.is_billable = True
   >>> expense.description = 'description'
   >>> expense.linked_issue_id = 557
   >>> expense.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> expense.save()
   <redminelib.resources.Expense #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Expense resource from the Invoices plugin by its id.

   :param int resource_id: (required). Id of the expense.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> expense = redmine.expense.get(123)
   >>> expense
   <redminelib.resources.Expense #123>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Expense resources from the Invoices plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> expenses = redmine.expense.all(limit=50)
   >>> expenses
   <redminelib.resultsets.ResourceSet object with Expense resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Expense resources that match the given lookup parameters.

   :param project_id: (optional). Id or identifier of expenses's project.
   :type project_id: int or string
   :param int assigned_to_id: (optional). Get expenses which are assigned to this user id.
   :param int status_id: (optional). Get expenses which have this status id.
   :param int contact_id: (optional). Get expenses for the given contact id.
   :param int author_id: (optional). Get expenses created by given author id.
   :param bool is_billable: (optional). Whether expense is billable.
   :param string currency: (optional). Get expenses which have the given currency.
   :param expense_date: (optional). Get expenses occurred on the given date.
   :type expense_date: string or date object
   :param string search: (optional). Get expenses with given search string.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> expenses = redmine.expense.filter(project_id='invoices', assigned_to_id=123, status_id=3, search='EXP', is_billable=True)
   >>> expenses
   <redminelib.resultsets.ResourceSet object with Expense resources>

.. hint::

   You can also get expenses from a Project, User and Contact resource objects directly using
   ``expenses`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('invoices')
      >>> project.expenses
      <redminelib.resultsets.ResourceSet object with Expense resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of an Expense resource and saves them to the Invoices plugin.

   :param int resource_id: (required). Expense id.
   :param project_id: (required). Id or identifier of expense's project.
   :type project_id: int or string
   :param int status_id:
    .. raw:: html

       (required). Expense status id:

    - 1 - draft
    - 2 - new
    - 3 - billed
    - 4 - paid

   :param expense_date: (required). Date when expense occurred.
   :type expense_date: string or date object
   :param string price: (optional). Expense amount.
   :param string currency: (optional). Expense currency.
   :param int contact_id: (optional). Expense contact id.
   :param int assigned_to_id: (optional). Expense will be assigned to this user id.
   :param bool is_billable: (optional). Whether expense is billable.
   :param int linked_issue_id: (optional). Issue id to be linked with this expense.
   :param string description: (optional). Expense description.
   :param list uploads:
    .. raw:: html

       (optional). Uploads as [{'': ''}, ...], accepted keys are:

    - path (required). Absolute file path or file-like object that should be uploaded.
    - filename (optional). Name of the file after upload.
    - description (optional). Description of the file.
    - content_type (optional). Content type of the file.

   :return: True

.. code-block:: python

   >>> redmine.expense.update(
   ...     project_id='invoices',
   ...     status_id=2,
   ...     expense_date='2023-01-11',
   ...     price='13.56',
   ...     currency='USD',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     is_billable=True,
   ...     description='description',
   ...     linked_issue_id=557,
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Expense
   :noindex:

   Saves the current state of an Expense resource to the Invoices plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> expense = redmine.expense.get(123)
   >>> expense.project_id = 'invoices'
   >>> expense.status_id = 2
   >>> expense.expense_date = '2023-01-11'
   >>> expense.price = '13.56'
   >>> expense.currency = 'USD'
   >>> expense.contact_id = 3
   >>> expense.assigned_to_id = 12
   >>> expense.is_billable = True
   >>> expense.description = 'description'
   >>> expense.linked_issue_id = 557
   >>> expense.uploads = [{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   >>> expense.save()
   <redminelib.resources.Expense #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> expense = redmine.expense.get(123).save(
   ...     project_id='invoices',
   ...     status_id=2,
   ...     expense_date='2023-01-11',
   ...     price='13.56',
   ...     currency='USD',
   ...     contact_id=3,
   ...     assigned_to_id=12,
   ...     is_billable=True,
   ...     description='description',
   ...     linked_issue_id=557,
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> expense
   <redminelib.resources.Expense #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Expense resource from the Invoices plugin by its id.

   :param int resource_id: (required). Expense id.
   :return: True

.. code-block:: python

   >>> redmine.expense.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Expense
   :noindex:

   Deletes current Expense resource object from the Invoices plugin.

   :return: True

.. code-block:: python

   >>> expense = redmine.expense.get(1)
   >>> expense.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Expense resources in one of the following formats: csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> expenses = redmine.expense.all()
   >>> expenses.export('csv', savepath='/home/jsmith', filename='expenses.csv')
   '/home/jsmith/expenses.csv'
