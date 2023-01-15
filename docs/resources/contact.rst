Contact
=======

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the Contact resource are provided by its manager. To get access to it
you have to call ``redmine.contact`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Contact resource with given fields and saves it to the CRM plugin.

   :param project_id: (required). Id or identifier of contact's project.
   :type project_id: int or string
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
   :param bool is_company: (optional). Whether contact is a company.
   :param int assigned_to_id: (optional). Contact will be assigned to this user id.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param dict address_attributes:
    .. raw:: html

       (optional). Address attributes as dict, available keys are:

    - street1 - first line for the street details
    - street2 - second line for the street details
    - city - city
    - region - region (state)
    - postcode - ZIP code
    - country_code - country code as two-symbol abbreviation (e.g. US)

   :param int visibility:
    .. raw:: html

       (optional). Contact visibility:

    - 0 - project
    - 1 - public
    - 2 - private

   :return: :ref:`Resource` object

.. code-block:: python

   >>> contact = redmine.contact.create(
   ...     project_id='vacation',
   ...     first_name='Ivan',
   ...     last_name='Ivanov',
   ...     middle_name='Ivanovich',
   ...     company='Ivan Gmbh',
   ...     phones=['1234567'],
   ...     emails=['ivan@ivanov.com'],
   ...     website='ivanov.com',
   ...     skype_name='ivan.ivanov',
   ...     birthday=datetime.date(1980, 10, 21),
   ...     background='some background here',
   ...     job_title='CEO',
   ...     tag_list=['vip', 'online'],
   ...     is_company=False,
   ...     address_attributes={'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'},
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     visibility=0
   ... )
   >>> contact
   <redminelib.resources.Contact #1 "Ivan Ivanov">

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Contact resource but saves it to the the CRM plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

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
   >>> contact.birthday = datetime.date(1980, 10, 21)
   >>> contact.background = 'some background here'
   >>> contact.job_title = 'CEO'
   >>> contact.tag_list = ['vip', 'online']
   >>> contact.is_company = False
   >>> contact.address_attributes = {'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}
   >>> contact.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> contact.visibility = 0
   >>> contact.save()
   <redminelib.resources.Contact #1 "Ivan Ivanov">

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Contact resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the contact.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - notes
    - contacts
    - deals
    - issues
    - projects
    - tickets (requires Pro Edition and `Helpdesk plugin <https://www.redmineup.com/pages/plugins/helpdesk>`_ >= 4.1.12)

   :return: :ref:`Resource` object

.. code-block:: python

   >>> contact = redmine.contact.get(12345, include=['notes', 'contacts', 'deals', 'issues', 'projects'])
   >>> contact
   <redminelib.resources.Contact #12345 "Ivan Ivanov">

.. hint::

   Contact resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Contact
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Contact resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> contact = redmine.contact.get(12345)
      >>> contact.issues
      <redminelib.resultsets.ResourceSet object with Issue resources>

.. hint::

   Contact resource object provides you with some relations. Relations are the other
   resource objects wrapped in a :ref:`ResourceSet` which are somehow related to a Contact
   resource object. The relations provided by the Contact resource object are:

   * invoices (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_
     >= 4.1.3)
   * payments (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_
     >= 4.1.3)
   * expenses (requires Pro Edition and `Invoices plugin <https://www.redmineup.com/pages/plugins/invoices>`_
     >= 4.1.3)

   .. code-block:: python

      >>> contact = redmine.contact.get(12345)
      >>> contact.invoices
      <redminelib.resultsets.ResourceSet object with Invoice resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Contact resources from the CRM plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> contacts = redmine.contact.all(offset=10, limit=100)
   >>> contacts
   <redminelib.resultsets.ResourceSet object with Contact resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Contact resources that match the given lookup parameters.

   :param project_id: (optional). Id or identifier of contact's project.
   :type project_id: int or string
   :param int assigned_to_id: (optional). Get contacts assigned to this user id.
   :param int query_id: (optional). Get contacts for the given query id.
   :param string search: (optional). Get contacts with given search string.
   :param string tags: (optional). Get contacts with given tags (separated by ``,``).
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> contacts = redmine.contact.filter(project_id='vacation', assigned_to_id=123, search='Smith', tags='one,two')
   >>> contacts
   <redminelib.resultsets.ResourceSet object with Contact resources>

.. hint::

   You can also get contacts from a Project and User resource objects directly using
   ``contacts`` relation:

   .. code-block:: python

      >>> project = redmine.project.get('vacation')
      >>> project.contacts
      <redminelib.resultsets.ResourceSet object with Contact resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Contact resource and saves them to the CRM plugin.

   :param int resource_id: (required). Contact id.
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
   :param bool is_company: (optional). Whether contact is a company.
   :param int assigned_to_id: (optional). Contact will be assigned to this user id.
   :param list custom_fields: (optional). Custom fields as [{'id': 1, 'value': 'foo'}].
   :param dict address_attributes:
    .. raw:: html

       (optional). Address attributes as dict, available keys are:

    - street1 - first line for the street details
    - street2 - second line for the street details
    - city - city
    - region - region (state)
    - postcode - ZIP code
    - country_code - country code as two-symbol abbreviation (e.g. US)

   :param int visibility:
    .. raw:: html

       (optional). Contact visibility:

    - 0 - project
    - 1 - public
    - 2 - private

   :return: True

.. code-block:: python

   >>> redmine.contact.update(
   ...     12345,
   ...     first_name='Ivan',
   ...     last_name='Ivanov',
   ...     middle_name='Ivanovich',
   ...     company='Ivan Gmbh',
   ...     phones=['1234567'],
   ...     emails=['ivan@ivanov.com'],
   ...     website='ivanov.com',
   ...     skype_name='ivan.ivanov',
   ...     birthday=datetime.date(1980, 10, 21),
   ...     background='some background here',
   ...     job_title='CEO',
   ...     tag_list=['vip', 'online'],
   ...     is_company=False,
   ...     address_attributes={'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'},
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     visibility=0
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Contact
   :noindex:

   Saves the current state of a Contact resource to the CRM plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

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
   >>> contact.birthday = datetime.date(1980, 10, 21)
   >>> contact.background = 'some background here'
   >>> contact.job_title = 'CEO'
   >>> contact.tag_list = ['vip', 'online']
   >>> contact.is_company = False
   >>> contact.address_attributes = {'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'}
   >>> contact.custom_fields = [{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}]
   >>> contact.visibility = 0
   >>> contact.save()
   <redminelib.resources.Contact #12345 "Ivan Ivanov">

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> contact = redmine.contact.get(12345).save(
   ...     first_name='Ivan',
   ...     last_name='Ivanov',
   ...     middle_name='Ivanovich',
   ...     company='Ivan Gmbh',
   ...     phones=['1234567'],
   ...     emails=['ivan@ivanov.com'],
   ...     website='ivanov.com',
   ...     skype_name='ivan.ivanov',
   ...     birthday=datetime.date(1980, 10, 21),
   ...     background='some background here',
   ...     job_title='CEO',
   ...     tag_list=['vip', 'online'],
   ...     is_company=False,
   ...     address_attributes={'street1': 'foo', 'street2': 'bar', 'city': 'Moscow', 'postcode': '111111', 'country_code': 'RU'},
   ...     custom_fields=[{'id': 1, 'value': 'foo'}, {'id': 2, 'value': 'bar'}],
   ...     visibility = 0
   ... )
   >>> contact
   <redminelib.resources.Contact #12345 "Ivan Ivanov">

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Contact resource from the CRM plugin by its id.

   :param int resource_id: (required). Contact id.
   :return: True

.. code-block:: python

   >>> redmine.contact.delete(1)
   True

.. py:method:: delete()
   :module: redminelib.resources.Contact
   :noindex:

   Deletes current Contact resource object from the CRM plugin.

   :return: True

.. code-block:: python

   >>> contact = redmine.contact.get(1)
   >>> contact.delete()
   True

Export
------

.. versionadded:: 2.0.0

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resources.Contact
   :noindex:

   Exports Contact resource in one of the following formats: atom, vcf

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> contact = redmine.contact.get(123)
   >>> contact.export('pdf', savepath='/home/jsmith')
   '/home/jsmith/123.pdf'

.. py:method:: export(fmt, savepath=None, filename=None)
   :module: redminelib.resultsets.ResourceSet
   :noindex:

   Exports a resource set of Contact resources in one of the following formats: atom, csv, vcf, xls

   :param string fmt: (required). Format to use for export.
   :param string savepath: (optional). Path where to save the file.
   :param string filename: (optional). Name that will be used for the file.
   :return: String or Object

.. code-block:: python

   >>> contacts = redmine.contact.all()
   >>> contacts.export('csv', savepath='/home/jsmith', filename='contacts.csv')
   '/home/jsmith/contacts.csv'

Projects
--------

Python-Redmine provides 2 methods to work with contact projects:

add
+++

.. py:method:: add(project_id)
   :module: redminelib.resources.Contact.Project
   :noindex:

   Adds project to contact's project list.

   :param project_id: (required). Id or identifier of a project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> contact = redmine.contact.get(1)
   >>> contact.project.add('vacation')
   True

remove
++++++

.. py:method:: remove(project_id)
   :module: redminelib.resources.Contact.Project
   :noindex:

   Removes project from contact's project list.

   :param project_id: (required). Id or identifier of a project.
   :type project_id: int or string
   :return: True

.. code-block:: python

   >>> contact = redmine.contact.get(1)
   >>> contact.project.remove('vacation')
   True
