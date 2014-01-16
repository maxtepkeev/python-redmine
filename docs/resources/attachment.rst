Attachment
==========

Supported by Redmine starting from version 1.3

Create
------

Not supported by Redmine. Some resources support adding attachments via it's create/update methods, e.g. issue.

Read
----

Methods
~~~~~~~

Get
+++

Supported keyword arguments: None

.. code-block:: python

    >>> attachment = redmine.attachment.get(76905)
    >>> attachment
    <redmine.resources.Attachment #76905 "1(a).png">

All
+++

Not supported by Redmine

Filter
++++++

Not supported by Redmine

Update
------

Not supported by Redmine

Delete
------

Not supported by Redmine
