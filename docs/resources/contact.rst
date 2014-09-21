Contact
=======

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ is installed.

.. hint::

    It is highly recommended to use CRM plugin 3.3.0 and higher because some bugs and
    inconsistencies in REST API exists in older versions.

Manager
-------

All operations on the contact resource are provided via it's manager. To get access to it
you have to call ``redmine.contact`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new contact resource with given fields and saves it to the CRM plugin.

    :param project_id: (required). Id or identifier of contact's project.
    :type project_id: integer or string
    :param string first_name: (required). Contact first name.
    :param string last_name: (optional). Contact last name.
    :param string middle_name: (optional). Contact middle name.
    :param string company: (optional). Contact company name.
    :param list phones: (optional). List of phone numbers.
    :param list emails: (optional). List of emails.
    :param string website: (optional). Contact website.
    :param string skype_name: (optional). Contact skype.
    :param birthday: (optional). Contact birthday.
    :type birthday: string or date object
    :param string background: (optional). Contact background.
    :param string job_title: (optional). Contact job title.
    :param list tag_list: (optional). List of tags.
    :param boolean is_company: (optional). Whether contact is a company.
    :param integer assigned_to_id: (optional). Contact will be assigned to this user id.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :param dict address_attributes:
      .. raw:: html

          (optional). Address attributes as dict, available keys are:

      - street1 - first line for the street details
      - street2 - second line for the street details
      - city - city
      - region - region (state)
      - postcode - ZIP code
      - country_code - country code as two-symbol abbreviation (e.g. US)

    :param integer visibility:
      .. raw:: html

          (optional). Contact visibility:

      - 0 - project
      - 1 - public
      - 2 - private

    :return: Contact resource object

.. code-block:: python

    >>> contact = redmine.contact.create(project_id='vacation', first_name='Ivan', last_name='Ivanov', middle_name='Ivanovich', company='Ivan Gmbh', phones=['1234567'], emails=['ivan@ivanov.com'], website='ivanov.com', skype_name='ivan.ivanov', birthday='1980-10-21', background='some background here', job_title='CEO', tag_list=['vip', 'online'], is_company=False, address_attributes={'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}], visibility=0)
    >>> contact
    <redmine.resources.Contact #1 "Ivan Ivanov">

new
+++

.. py:method:: new()
    :module: redmine.managers.ResourceManager
    :noindex:

    Creates new empty contact resource but doesn't save it to the CRM plugin. This is useful if
    you want to set some resource fields later based on some condition(s) and only after
    that save it to the CRM plugin. Valid attributes are the same as for ``create`` method above.

    :return: Contact resource object

.. code-block:: python

    >>> contact = redmine.contact.new()
    >>> contact.project_id = 'vacation'
    >>> contact.first_name = 'Ivan'
    >>> contact.last_name = 'Ivanov'
    >>> contact.middle_name = 'Ivanovich'
    >>> contact.company = 'Ivan Gmbh'
    >>> contact.phones = ['1234567']
    >>> contact.emails = ['ivan@ivanov.com']
    >>> contact.website = 'ivanov.com'
    >>> contact.skype_name = 'ivan.ivanov'
    >>> contact.birthday = '1980-10-21'
    >>> contact.background = 'some background here'
    >>> contact.job_title = 'CEO'
    >>> contact.tag_list = ['vip', 'online']
    >>> contact.is_company = False
    >>> contact.address_attributes = {'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}
    >>> contact.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> contact.visibility = 0
    >>> contact.save()
    True

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single contact resource from the CRM plugin by it's id.

    :param integer resource_id: (required). Id of the contact.
    :param string include:
      .. raw:: html

          (optional). Can be used to fetch associated data in one call. Accepted values (separated by comma):

      - notes
      - contacts
      - deals
      - issues

    :return: Contact resource object

.. code-block:: python

    >>> contact = redmine.contact.get(12345, include='notes,contacts,deals,issues')
    >>> contact
    <redmine.resources.Contact #1 "Ivan Ivanov">

.. hint::

    Contact resource object provides you with on demand includes. On demand includes are the
    other resource objects wrapped in a ResourceSet which are associated with a Contact
    resource object. Keep in mind that on demand includes are retrieved in a separate request,
    that means that if the speed is important it is recommended to use ``get`` method with a
    ``include`` keyword argument. The on demand includes provided by the Contact resource object
    are the same as in the ``get`` method above:

    .. code-block:: python

        >>> contact = redmine.contact.get(12345)
        >>> contact.issues
        <redmine.resultsets.ResourceSet object with Issue resources>

all
+++

.. py:method:: all(**params)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns all contact resources from the CRM plugin.

    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> contacts = redmine.contact.all(offset=10, limit=100)
    >>> contacts
    <redmine.resultsets.ResourceSet object with Contact resources>

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns contact resources that match the given lookup parameters.

    :param project_id: (optional). Id or identifier of contact's project.
    :type project_id: integer or string
    :param integer assigned_to_id: (optional). Get contacts which are assigned to this user id.
    :param integer query_id: (optional). Get contacts for the given query id.
    :param string search: (optional). Get contacts with the given search string.
    :param string tags: (optional). Get contacts with the given tags (separated by comma).
    :param integer limit: (optional). How much resources to return.
    :param integer offset: (optional). Starting from what resource to return the other resources.
    :return: ResourceSet object

.. code-block:: python

    >>> contacts = redmine.contact.filter(project_id='vacation', assigned_to_id=123, search='Smith', tags='one,two')
    >>> contacts
    <redmine.resultsets.ResourceSet object with Contact resources>

.. hint::

    You can also get contacts from a project and user resource objects directly using
    ``contacts`` relation:

    .. code-block:: python

        >>> project = redmine.project.get('vacation')
        >>> project.contacts
        <redmine.resultsets.ResourceSet object with Contact resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
    :module: redmine.managers.ResourceManager
    :noindex:

    Updates values of given fields of a contact resource and saves them to the CRM plugin.

    :param integer resource_id: (required). Contact id.
    :param string first_name: (optional). Contact first name.
    :param string last_name: (optional). Contact last name.
    :param string middle_name: (optional). Contact middle name.
    :param string company: (optional). Contact company name.
    :param list phones: (optional). List of phone numbers.
    :param list emails: (optional). List of emails.
    :param string website: (optional). Contact website.
    :param string skype_name: (optional). Contact skype.
    :param birthday: (optional). Contact birthday.
    :type birthday: string or date object
    :param string background: (optional). Contact background.
    :param string job_title: (optional). Contact job title.
    :param list tag_list: (optional). List of tags.
    :param boolean is_company: (optional). Whether contact is a company.
    :param integer assigned_to_id: (optional). Contact will be assigned to this user id.
    :param list custom_fields: (optional). Custom fields in the form of [{'id': 1, 'value': 'foo'}].
    :param dict address_attributes:
      .. raw:: html

          (optional). Address attributes as dict, available keys are:

      - street1 - first line for the street details
      - street2 - second line for the street details
      - city - city
      - region - region (state)
      - postcode - ZIP code
      - country_code - country code as two-symbol abbreviation (e.g. US)

    :param integer visibility:
      .. raw:: html

          (optional). Contact visibility:

      - 0 - project
      - 1 - public
      - 2 - private

    :return: True

.. code-block:: python

    >>> redmine.contact.update(12345, first_name='Ivan', last_name='Ivanov', middle_name='Ivanovich', company='Ivan Gmbh', phones=['1234567'], emails=['ivan@ivanov.com'], website='ivanov.com', skype_name='ivan.ivanov', birthday='1980-10-21', background='some background here', job_title='CEO', tag_list=['vip', 'online'], is_company=False, address_attributes={'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}, custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}], visibility=0)
    True

save
++++

.. py:method:: save()
    :module: redmine.resources.Contact
    :noindex:

    Saves the current state of a contact resource to the CRM plugin. Fields that
    can be changed are the same as for ``update`` method above.

    :return: True

.. code-block:: python

    >>> contact = redmine.contact.get(12345)
    >>> contact.first_name = 'Ivan'
    >>> contact.last_name = 'Ivanov'
    >>> contact.middle_name = 'Ivanovich'
    >>> contact.company = 'Ivan Gmbh'
    >>> contact.phones = ['1234567']
    >>> contact.emails = ['ivan@ivanov.com']
    >>> contact.website = 'ivanov.com'
    >>> contact.skype_name = 'ivan.ivanov'
    >>> contact.birthday = '1980-10-21'
    >>> contact.background = 'some background here'
    >>> contact.job_title = 'CEO'
    >>> contact.tag_list = ['vip', 'online']
    >>> contact.is_company = False
    >>> contact.address_attributes = {'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}
    >>> contact.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
    >>> contact.visibility = 0
    >>> contact.save()
    True

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Deletes single contact resource from the CRM plugin by it's id.

    :param integer resource_id: (required). Contact id.
    :return: True

.. code-block:: python

    >>> redmine.contact.delete(1)
    True

Projects
--------

Python Redmine provides 2 methods to work with contact projects: ``add`` and ``remove``.

add
+++

.. py:method:: add(project_id)
    :module: redmine.resources.Contact.Project
    :noindex:

    Adds project to contact's project list.

    :param project_id: (required). Id or identifier of a project.
    :type project_id: integer or string
    :return: True

.. code-block:: python

    >>> contact = redmine.contact.get(1)
    >>> contact.project.add('vacation')
    True

remove
++++++

.. py:method:: remove(project_id)
    :module: redmine.resources.Contact.Project
    :noindex:

    Removes project from contact's project list.

    :param project_id: (required). Id or identifier of a project.
    :type project_id: integer or string
    :return: True

.. code-block:: python

    >>> contact = redmine.contact.get(1)
    >>> contact.project.remove('vacation')
    True
