Enumeration
===========

Supported by Redmine starting from version 2.2

Manager
-------

All operations on the enumeration resource are provided via it's manager. To get access to
it you have to call ``redmine.enumeration`` where ``redmine`` is a configured redmine object.
See the :doc:`../configuration` about how to configure redmine object.

Create methods
--------------

Not supported by Redmine

Read methods
------------

get
+++

Not supported by Redmine

all
+++

Not supported by Redmine

filter
++++++

.. py:method:: filter(**filters)
    :module: redmine.managers.ResourceManager
    :noindex:

    Returns enumeration resources that match the given lookup parameters.

    :param string resource:
      .. raw:: html

          (required). Get enumerations for the requested resource. Available resources are:

      - issue_priorities
      - time_entry_activities

    :return: ResourceSet object

.. code-block:: python

    >>> enumerations = redmine.enumeration.filter(resource='time_entry_activities')
    >>> enumerations
    <redmine.resultsets.ResourceSet object with Enumeration resources>

Update methods
--------------

Not supported by Redmine

Delete methods
--------------

Not supported by Redmine
