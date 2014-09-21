Note
====

Supported starting from version 1.0.0 and only available if `CRM plugin <http://redminecrm.com/
projects/crm/pages/1>`_ 3.2.4 and higher is installed.

Manager
-------

All operations on the note resource are provided via it's manager. To get access to
it you have to call ``redmine.note`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by CRM plugin

Read methods
------------

get
+++

.. py:method:: get(resource_id)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns single note resource from the Redmine by it's id.

    :param integer resource_id: (required). Id of the note.
    :return: Note resource object

.. code-block:: python

    >>> note = redmine.note.get(12345)
    >>> note
    <redmine.resources.Note #12345>

all
+++

Not supported by CRM plugin

filter
++++++

Not supported by CRM plugin

Update methods
--------------

Not supported by CRM plugin

Delete methods
--------------

Not supported by CRM plugin
