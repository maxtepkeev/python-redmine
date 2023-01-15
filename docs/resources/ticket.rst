Ticket
======

.. versionadded:: 2.4.0

Requires Pro Edition and `Helpdesk plugin <https://www.redmineup.com/pages/plugins/helpdesk>`_ >= 4.1.12.

Manager
-------

All operations on the Ticket resource are provided by its manager. To get access to it
you have to call ``redmine.ticket`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

create
++++++

.. py:method:: create(**fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new Ticket resource with given fields and saves it to the Helpdesk plugin.

   :param dict contact: (required). Can be either existing (the only required field is ``email`` then)
    contact or a new one, check Contact `docs <https://python-redmine.com/resources/contact.html#create>`_
    for a list of fields.
   :param dict issue:
    .. raw:: html

       (required). New Issue will be created for this ticket, check Issue
       <a href="https://python-redmine.com/resources/issue.html#create">docs</a>
       for a list of fields, required fields are:

    - project_id - ticket issue's project id
    - tracker_id - be sure to set the correct tracker from Helpdesk plugin settings
    - subject - ticket issue's subject
    - description - ticket issue's content

   :param ticket_date: (required). Ticket date.
   :type ticket_date: string or date object
   :param string ticket_time: (required). Ticket time.
   :param string source:
    .. raw:: html

       (optional). Ticket source:

    - 0 - email
    - 1 - web
    - 2 - phone
    - 4 - conversation

   :param string helpdesk_send_as:
    .. raw:: html

       (optional). Send as:

    - 1 - notification
    - 2 - initial message

   :param string to_address: (optional). To addresses (, separated).
   :param string cc_address: (optional). Cc addresses (, separated).
   :param bool is_incoming: (optional). Whether ticket is incoming.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.ticket.create(
   ...     source='2',
   ...     helpdesk_send_as='2',
   ...     ticket_date='2023-01-10',
   ...     ticket_time='10:01',
   ...     to_address='support@product.com',
   ...     cc_address='managers@product.com,jsmith@product.com',
   ...     is_incoming=True,
   ...     issue={
   ...         'project_id': 'helpdesk',
   ...         'subject': 'ticket subject',
   ...         'tracker_id': 6,
   ...         'description': 'ticket content',
   ...     },
   ...     contact={
   ...         'email': 'existing_client@mail.com',
   ...     }
   ... )
   >>> ticket
   <redminelib.resources.Ticket #123>

new
+++

.. py:method:: new()
   :module: redminelib.managers.ResourceManager
   :noindex:

   Creates new empty Ticket resource, but saves it to the Helpdesk plugin only when ``save()`` is called,
   also calls ``pre_create()`` and ``post_create()`` methods of the :ref:`Resource` object. Valid attributes
   are the same as for ``create()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.ticket.new()
   >>> ticket.source = '2'
   >>> ticket.helpdesk_send_as = '2'
   >>> ticket.ticket_date = '2023-01-10'
   >>> ticket.ticket_time = '10:01'
   >>> ticket.to_address = 'support@product.com'
   >>> ticket.cc_address = 'managers@product.com,jsmith@product.com'
   >>> ticket.is_incoming = True
   >>> ticket.issue = {
   ...     'project_id': 'helpdesk',
   ...     'subject': 'ticket subject',
   ...     'tracker_id': 6,
   ...     'description': 'ticket content',
   ... }
   >>> ticket.contact = {
   ...     'email': 'existing_client@mail.com',
   ... }
   >>> ticket.save()
   <redminelib.resources.Ticket #123>

Read methods
------------

get
+++

.. py:method:: get(resource_id, **params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Ticket resource from the Helpdesk plugin by its id.

   :param int resource_id: (required). Id of the ticket.
   :param list include:
    .. raw:: html

       (optional). Fetches associated data in one call. Accepted values:

    - journals

   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.ticket.get(123, include=['journals'])
   >>> ticket
   <redminelib.resources.Ticket #123>

.. hint::

   Ticket resource object provides you with on demand includes. On demand includes are the
   other resource objects wrapped in a :ref:`ResourceSet` which are associated with a Ticket
   resource object. Keep in mind that on demand includes are retrieved in a separate request,
   that means that if the speed is important it is recommended to use ``get()`` method with
   ``include`` keyword argument. On demand includes provided by the Ticket resource object
   are the same as in the ``get()`` method above:

   .. code-block:: python

      >>> ticket = redmine.ticket.get(123)
      >>> ticket.journals
      <redminelib.resultsets.ResourceSet object with TicketJournal resources>

all
+++

.. py:method:: all(**params)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns all Ticket resources from the Helpdesk plugin.

   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> tickets = redmine.ticket.all(limit=50)
   >>> tickets
   <redminelib.resultsets.ResourceSet object with Ticket resources>

filter
++++++

.. py:method:: filter(**filters)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns Ticket resources that match the given lookup parameters.

   :param string source: (optional). Get tickets for the given source.
   :param string from_address: (optional). Get tickets that were sent from this address.
   :param int limit: (optional). How much resources to return.
   :param int offset: (optional). Starting from what resource to return the other resources.
   :return: :ref:`ResourceSet` object

.. code-block:: python

   >>> tickets = redmine.ticket.filter(source='2', from_address='client@mail.com')
   >>> tickets
   <redminelib.resultsets.ResourceSet object with Ticket resources>

.. hint::

   You can also get tickets from a Contact resource object directly using ``tickets`` on demand includes:

   .. code-block:: python

      >>> contact = redmine.contact.get(123)
      >>> contact.tickets
      <redminelib.resultsets.ResourceSet object with Ticket resources>

Update methods
--------------

update
++++++

.. py:method:: update(resource_id, **fields)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Updates values of given fields of a Ticket resource and saves them to the Helpdesk plugin.

   :param int resource_id: (required). Ticket id.
   :param ticket_date: (optional). Ticket date.
   :type ticket_date: string or date object
   :param string ticket_time: (optional). Ticket time.
   :param string source:
    .. raw:: html

       (optional). Ticket source:

    - 0 - email
    - 1 - web
    - 2 - phone
    - 4 - conversation

   :param string from_address: (optional). Updates contact of the ticket.
   :param string to_address: (optional). To addresses (, separated).
   :param string cc_address: (optional). Cc addresses (, separated).
   :param bool is_incoming: (optional). Whether ticket is incoming.
   :return: True

.. code-block:: python

   >>> redmine.ticket.update(
   ...     123,
   ...     source='2',
   ...     ticket_date='2023-01-10',
   ...     ticket_time='10:01',
   ...     from_address='client@mail.com',
   ...     to_address='support@product.com',
   ...     cc_address='managers@product.com,jsmith@product.com',
   ...     is_incoming=True
   ... )
   True

save
++++

.. py:method:: save(**attrs)
   :module: redminelib.resources.Expense
   :noindex:

   Saves the current state of a Ticket resource to the Helpdesk plugin. Attrs that
   can be changed are the same as for ``update()`` method above.

   :return: :ref:`Resource` object

.. code-block:: python

   >>> ticket = redmine.ticket.get(123)
   >>> ticket.source = '2'
   >>> ticket.ticket_date = '2023-01-10'
   >>> ticket.ticket_time = '10:01'
   >>> ticket.to_address = 'support@product.com'
   >>> ticket.cc_address = 'managers@product.com,jsmith@product.com'
   >>> ticket.is_incoming = True
   >>> ticket.save()
   <redminelib.resources.Ticket #123>

.. versionadded:: 2.1.0 Alternative syntax was introduced.

.. code-block:: python

   >>> ticket = redmine.ticket.get(123).save(
   ...     source='2',
   ...     ticket_date='2023-01-10',
   ...     ticket_time='10:01',
   ...     to_address='support@product.com',
   ...     cc_address='managers@product.com,jsmith@product.com',
   ...     is_incoming=True
   ... )
   >>> ticket
   <redminelib.resources.Ticket #123>

Delete methods
--------------

delete
++++++

.. py:method:: delete(resource_id)
   :module: redminelib.managers.ResourceManager
   :noindex:

   Deletes single Ticket resource from the Helpdesk plugin by its id.

   :param int resource_id: (required). Ticket id.
   :return: True

.. code-block:: python

   >>> redmine.ticket.delete(123)
   True

.. py:method:: delete()
   :module: redminelib.resources.Ticket
   :noindex:

   Deletes current Ticket resource object from the Helpdesk plugin.

   :return: True

.. code-block:: python

   >>> ticket = redmine.ticket.get(1)
   >>> ticket.delete()
   True

Export
------

Not supported by Helpdesk plugin, but as tickets are basically issues and share the same ID,
one can export Issue resources and get most of the ticket information from them.

Journals
--------

The history of a ticket is represented as a :ref:`ResourceSet` of ``TicketJournal`` resources.
Currently the following operations are possible:

create
++++++

To reply to a ticket, i.e. create a new record in ticket history, i.e. new journal:

.. code-block:: python

   >>> ticket = redmine.ticket.get(1)
   >>> journal = ticket.reply(
   ...     status_id=2,
   ...     content='we are working on your issue',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> journal
   <redminelib.resources.TicketJournal #321>

Or if you know the `issue_id` beforehand:

   >>> journal = redmine.ticket_journal.create(
   ...     issue_id=123,
   ...     status_id=2,
   ...     content='we are working on your issue',
   ...     uploads=[{'path': '/absolute/path/to/file'}, {'path': BytesIO(b'I am content of file 2')}]
   ... )
   >>> journal
   <redminelib.resources.TicketJournal #321>

read
++++

Recommended way to access ticket journals is through associated data includes:

.. code-block:: python

   >>> ticket = redmine.ticket.get(1, include=['journals'])
   >>> ticket.journals
   <redminelib.resultsets.ResourceSet object with TicketJournal resources>

But they can also be accessed through on demand includes:

.. code-block:: python

   >>> ticket = redmine.ticket.get(1)
   >>> ticket.journals
   <redminelib.resultsets.ResourceSet object with TicketJournal resources>

After that they can be used as usual:

.. code-block:: python

   >>> for journal in ticket.journals:
   ...     print(journal.id, journal.notes)
   ...
   1 foobar
   2 lalala
   3 hohoho

update
++++++

To update `notes` attribute (the only attribute that can be updated) of a journal:

.. code-block:: python

   >>> ticket = redmine.ticket.get(1, include=['journals'])
   >>> for journal in ticket.journals:
   ...     journal.save(notes='setting notes to a new value')
   ...

Or if you know the `id` beforehand:

.. code-block:: python

   >>> redmine.ticket_journal.update(1, notes='setting notes to a new value')
   True

delete
++++++

To delete a journal, set its `notes` attribute to an empty string:

.. code-block:: python

   >>> ticket = redmine.ticket.get(1, include=['journals'])
   >>> for journal in ticket.journals:
   ...     journal.save(notes='')
   ...

Or if you know the `id` beforehand:

.. code-block:: python

   >>> redmine.ticket_journal.update(1, notes='')
   True

.. note::

   You can only delete a journal that doesn't have the associated `details` attribute.
