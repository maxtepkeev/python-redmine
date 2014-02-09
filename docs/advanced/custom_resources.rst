Custom Resources
================

Sometimes there is a need to redefine a resource behaviour to achieve the needed goal. Python
Redmine provides a feature for such a case called custom resources. Basically this is just a
normal class inheritance made especially for Python Redmine.

Configuration
-------------

To take advantage of this feature you need to tell Python Redmine where to search for your
custom resources. This should be done with a ``custom_resource_paths`` argument passed to
the Redmine object which accepts a list or tuple of module paths which contain your custom
resources:

.. code-block:: python

    redmine = Redmine('https://redmine.url', custom_resource_paths=('foo.bar', 'bar.baz', 'foo.baz'))

.. note::

    The ordering is very important. Python Redmine will search for the resources in this order:

    #. foo.bar
    #. bar.baz
    #. foo.baz
    #. redmine.resources

Existing Resources
------------------

Here is the list of existing resource class names that can be inherited from:

* Issue
* Project
* ProjectMembership
* User
* TimeEntry
* News
* IssueRelation
* Version
* WikiPage
* Query
* Attachment
* IssueStatus
* Tracker
* Enumeration
* IssueCategory
* Role
* Group
* CustomField

Creation
--------

To create a custom resource choose which resource behavior you want to change, e.g. Project:

.. code-block:: python

    from redmine.resources import Project

    class CustomProject(Project):
        pass

Name
----

Python Redmine converts underscore to camelcase when it tries to import the resource, that means
that it is important to follow this convention to make everything work properly, e.g when you do:

.. code-block:: python

    custom_wiki_page = redmine.custom_wiki_page.get('Foo')

Python Redmine is searching for a resource class named CustomWikiPage in the modules defined via
the ``custom_resource_paths`` argument on Redmine object instantiation.

Methods and Attributes
----------------------

All existing resources are derived from a ``_Resource`` class which you usually won't inherit from
directly unless you want to add support for a new resource which Python Redmine doesn't support.
Below you will find methods and attributes which can be redefined in your custom resource:

.. autoclass:: redmine.resources._Resource
    :members: _readonly, __init__, __getattr__, __setattr__, refresh, pre_create, post_create, pre_update, post_update, save, translate_params
    :undoc-members:
    :private-members:
