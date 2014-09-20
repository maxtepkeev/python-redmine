Deal
====

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ is installed.

.. hint::

    It is highly recommended to use CRM plugin of version 3.3.0 and higher because some bugs
    and inconsistencies in REST API exists in older versions.

Manager
-------

All operations on the deal resource are provided via it's manager. To get access to it
you have to call ``redmine.deal`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new deal resource with given fields and saves it to the CRM plugin.

    :param project_id: (required). Id or identifier of deal's project.
    :type project_id: integer or string
    :param string name: (required). Deal name.
    :param integer contact_id: (optional). Deal contact id.
    :param integer price: (optional). Deal price.
    :param string currency: (optional). Deal currency.
    :param integer probability: (optional). Deal probability.
    :param due_date: (optional). Deal should be won by this date.
    :type due_date: string or date object
    :param string background: (optional). Deal background.
    :param integer status_id: (optional). Deal status id.
    :param integer category_id: (optional). Deal category id.
    :param integer assigned_to_id: (optional). Deal will be assigned to this user id.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].

    :return: Deal resource object

.. code-block:: python

    >>> deal = redmine.deal.create(project_id='vacation', name='FooBar', contact_id=1, price=1000, currency='EUR', probability=80, due_date=date(2014, 12, 12), background='some deal background', status_id=1, category_id=1, assigned_to_id=12, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    >>> deal
    <redmine.resources.Deal #123>

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty deal resource but doesn't save it to the CRM plugin. This is useful if
    you want to set some resource fields later based on some condition(s) and only after
    that save it to the CRM plugin. Valid attributes are the same as for ``create`` method above.

    :return: Deal resource object

.. code-block:: python

    >>> deal = redmine.deal.new()
    >>> deal.project_id = 'vacation'
    >>> deal.name = 'FooBar'
    >>> deal.contact_id = 1
    >>> deal.price = 1000
    >>> deal.currency = 'EUR'
    >>> deal.probability = 80
    >>> deal.due_date = date(2014, 12, 12)
    >>> deal.background = 'some deal background'
    >>> deal.status_id = 1
    >>> deal.category_id = 1
    >>> deal.assigned_to_id = 12
    >>> deal.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> deal.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single deal resource from the CRM plugin by it's id.

    :param integer resource_id: (required). Id of the deal.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - notes

    :return: Deal resource object

.. code-block:: python

    >>> deal = redmine.deal.get(123, include='notes')
    >>> deal
    <redmine.resources.Deal #123>

.. hint::

    Deal resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a Deal
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the Deal resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> deal = redmine.deal.get(123)
        >>> deal.notes
        <redmine.resultsets.ResourceSet object with Note resources>

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all deal resources from the CRM plugin.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> deals = redmine.deal.all(limit=50)
    >>> deals
    <redmine.resultsets.ResourceSet object with Deal resources>

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns deal resources that match the given lookup parameters.

    :param project_id: (optional). Id or identifier of deal's project.
    :type project_id: integer or string
    :param integer assigned_to_id: (optional). Get deals which are assigned to this user id.
    :param integer query_id: (optional). Get deals for the given query id.
    :param integer status_id: (optional). Get deals which have this status id.
    :param string search: (optional). Get deals with the given search string.
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> deals = redmine.deal.filter(project_id='vacation', assigned_to_id=123, status_id=1, search='Smith')
    >>> deals
    <redmine.resultsets.ResourceSet object with Deal resources>

.. hint::

    You can also get deals from a project resource object directly using
    ``deals`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.deals
        <redmine.resultsets.ResourceSet object with Deal resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a deal resource and saves them to the CRM plugin.

    :param integer resource_id: (required). Deal id.
    :param string name: (optional). Deal name.
    :param integer contact_id: (optional). Deal contact id.
    :param integer price: (optional). Deal price.
    :param string currency: (optional). Deal currency.
    :param integer probability: (optional). Deal probability.
    :param due_date: (optional). Deal should be won by this date.
    :type due_date: string or date object
    :param string background: (optional). Deal background.
    :param integer status_id: (optional). Deal status id.
    :param integer category_id: (optional). Deal category id.
    :param integer assigned_to_id: (optional). Deal will be assigned to this user id.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :return: True

.. code-block:: python

    >>> redmine.deal.update(123, name='FooBar', contact_id=1, price=1000, currency='EUR', probability=80, due_date=date(2014, 12, 12), background='some deal background', status_id=1, category_id=1, assigned_to_id=12, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}])
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Deal
    :noindex:

    Saves the current state of a deal resource to the CRM plugin. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> deal = redmine.deal.get(123)
    >>> deal.name = 'FooBar'
    >>> deal.contact_id = 1
    >>> deal.price = 1000
    >>> deal.currency = 'EUR'
    >>> deal.probability = 80
    >>> deal.due_date = date(2014, 12, 12)
    >>> deal.background = 'some deal background'
    >>> deal.status_id = 1
    >>> deal.category_id = 1
    >>> deal.assigned_to_id = 12
    >>> deal.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> deal.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single deal resource from the CRM plugin by it's id.

    :param integer resource_id: (required). Deal id.
    :return: True

.. code-block:: python

    >>> redmine.deal.delete(123)
    True
