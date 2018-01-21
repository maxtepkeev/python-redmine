Deal
====

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the Deal resource are provided by it's manager. To get access to it
you have to call ``redmine.deal`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Deal resource with given fields and saves it to the CRM plugin.

   :param project_id: (required). Id or identifier of deal's project.
   :type project_id: int or string
   :param string name: (required). Deal name.
   :param int contact_id: (optional). Deal contact id.
   :param int price: (optional). Deal price.
   :param string currency: (optional). Deal currency.
   :param int probability: (optional). Deal probability.
   :param due_date: (optional). Deal should be won by this date.
   :type due_date: string or date object
   :param string background: (optional). Deal background.
   :param int status_id: (optional). Deal status id.
   :param int category_id: (optional). Deal category id.
   :param int assigned_to_id: (optional). Deal will be assigned to this user id.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :return: :ref:`Resource` object

.. code-block:: python

   >>> deal = redmine.deal.create(
   ...     project_id='vacation',
   ...     name='FooBar',
   ...     contact_id=1,
   ...     price=1000,
   ...     currency='EUR',
   ...     probability=80,
   ...     due_date=datetime.date(2014, 12, 12),
   ...     background='some deal background',
   ...     status_id=1,
   ...     category_id=1,
   ...     assigned_to_id=12,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   ... )
   >>> deal
   <redminelib.resources.Deal #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Deal resource but saves it to the CRM plugin only when ``save()`` is called, also
   calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> deal = redmine.deal.new()
   >>> deal.project_id = 'vacation'
   >>> deal.name = 'FooBar'
   >>> deal.contact_id = 1
   >>> deal.price = 1000
   >>> deal.currency = 'EUR'
   >>> deal.probability = 80
   >>> deal.due_date = datetime.date(2014, 12, 12)
   >>> deal.background = 'some deal background'
   >>> deal.status_id = 1
   >>> deal.category_id = 1
   >>> deal.assigned_to_id = 12
   >>> deal.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> deal.save()
   <redminelib.resources.Deal #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Deal resource from the CRM plugin by it's id.

   :param int resource_id: (required). Id of the deal.
   :param string include:
    .. raw:: html

       (optional). Can be used to fetch associated data in one call. Accepted values (separated by
       <code class="docutils literal"><span class="pre">,</span></code>):

    - notes

   :return: :ref:`Resource` object

.. code-block:: python

   >>> deal = redmine.deal.get(123, include='notes')
   >>> deal
   <redminelib.resources.Deal #123>

.. hint::

   Deal resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Deal
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Deal resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> deal = redmine.deal.get(123)
      >>> deal.notes
      <redminelib.resultsets.ResourceSet object with Note resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Deal resources from the CRM plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> deals = redmine.deal.all(limit=50)
   >>> deals
   <redminelib.resultsets.ResourceSet object with Deal resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Deal resources that match the given lookup parameters.

   :param project_id: (optional). Id or identifier of deal's project.
   :type project_id: int or string
   :param int assigned_to_id: (optional). Get deals which are assigned to this user id.
   :param int query_id: (optional). Get deals for the given query id.
   :param int status_id: (optional). Get deals which have this status id.
   :param string search: (optional). Get deals with given search string.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> deals = redmine.deal.filter(project_id='vacation', assigned_to_id=123, status_id=1, search='Smith')
   >>> deals
   <redminelib.resultsets.ResourceSet object with Deal resources>

.. hint::

   You can also get deals from a Project, User and DealStatus resource objects directly using
   ``deals`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.deals
      <redminelib.resultsets.ResourceSet object with Deal resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Deal resource and saves them to the CRM plugin.

   :param int resource_id: (required). Deal id.
   :param string name: (optional). Deal name.
   :param int contact_id: (optional). Deal contact id.
   :param int price: (optional). Deal price.
   :param string currency: (optional). Deal currency.
   :param int probability: (optional). Deal probability.
   :param due_date: (optional). Deal should be won by this date.
   :type due_date: string or date object
   :param string background: (optional). Deal background.
   :param int status_id: (optional). Deal status id.
   :param int category_id: (optional). Deal category id.
   :param int assigned_to_id: (optional). Deal will be assigned to this user id.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :return: True

.. code-block:: python

   >>> redmine.deal.update(
   ...     123,
   ...     name='FooBar',
   ...     contact_id=1,
   ...     price=1000,
   ...     currency='EUR',
   ...     probability=80,
   ...     due_date=datetime.date(2014, 12, 12),
   ...     background='some deal background',
   ...     status_id=1,
   ...     category_id=1,
   ...     assigned_to_id=12,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Deal
   :noindex:

   Saves the current state of a Deal resource to the CRM plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> deal = redmine.deal.get(123)
   >>> deal.name = 'FooBar'
   >>> deal.contact_id = 1
   >>> deal.price = 1000
   >>> deal.currency = 'EUR'
   >>> deal.probability = 80
   >>> deal.due_date = datetime.date(2014, 12, 12)
   >>> deal.background = 'some deal background'
   >>> deal.status_id = 1
   >>> deal.category_id = 1
   >>> deal.assigned_to_id = 12
   >>> deal.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> deal.save()
   <redminelib.resources.Deal #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> deal = redmine.deal.get(123).save(
   ...     contact_id=1,
   ...     price=1000,
   ...     currency='EUR',
   ...     probability=80,
   ...     due_date=datetime.date(2014, 12, 12),
   ...     background='some deal background',
   ...     status_id=1,
   ...     category_id=1,
   ...     assigned_to_id=12,
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   ... )
   >>> deal
   <redminelib.resources.Deal #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Deal resource from the CRM plugin by it's id.

   :param int resource_id: (required). Deal id.
   :return: True

.. code-block:: python

   >>> redmine.deal.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Deal
   :noindex:

   Deletes current Deal resource object from the CRM plugin.

   :return: True

.. code-block:: python

   >>> deal = redmine.deal.get(1)
   >>> deal.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Deal resources in one of the following formats: csv

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> deals = redmine.deal.all()
   >>> deals.export('csv', savepath='/home/jsmith', filename='deals.csv')
   '/home/jsmith/deals.csv'
