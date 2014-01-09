Enumeration
===========

Supported by Redmine starting from version 2.2

Create
------

Not supported by Redmine

Read
----

Methods
~~~~~~~

Get
+++

Not supported by Redmine

All
+++

Not supported by Redmine

Filter
++++++

Supported keyword arguments: None

Supported filters:

* **resource**. Get enumerations for the requested resource. Available resources are:

  - issue_priorities
  - time_entry_activities

.. code-block:: python

    >>> enumerations = redmine.enumeration.filter(resource='time_entry_activities')
    >>> enumerations
    <redmine.resultsets.ResourceSet object with Enumeration resources>

Update
------

Not supported by Redmine

Delete
------

Not supported by Redmine
