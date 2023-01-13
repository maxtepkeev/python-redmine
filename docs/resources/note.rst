Note
====

Requires Pro Edition and `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`_ >= 3.3.0.

Manager
-------

All operations on the Note resource are provided by its manager. To get access to
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
   :module: redminelib.managers.ResourceManager
   :noindex:

   Returns single Note resource from the CRM plugin by its id.

   :param int resource_id: (required). Id of the note.
   :return: :ref:`Resource` object

.. code-block:: python

   >>> note = redmine.note.get(12345)
   >>> note
   <redminelib.resources.Note #12345>

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

Export
------

Not supported by CRM plugin
