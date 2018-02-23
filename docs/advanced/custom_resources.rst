Custom Resources
================

Sometimes there is a need to redefine a resource behaviour to achieve the needed goal.
Python-Redmine provides a feature for such a case called custom resources. Basically this
is just a normal class inheritance made specifically for Python-Redmine.

Existing Resources
------------------

The list of existing resource class names that can be inherited from is available :doc:`here <../resources/index>`.

Creation
--------

To create a custom resource choose which resource behavior you want to change, e.g. WikiPage:

.. code-block:: python

   from redminelib.resources import WikiPage

   class CustomWikiPage(WikiPage):
       pass

Name
----

Python-Redmine converts underscore to camelcase when it tries to import the resource, which means
that it is important to follow this convention to make everything work properly, e.g when you do:

.. code-block:: python

   custom_wiki_page = redmine.custom_wiki_page.get('Foo')

Python-Redmine is searching for a resource class named CustomWikiPage. The location of the class
doesn't matter since all classes that inherit from any Python-Redmine resource class are automatically
added to the special resource registry.

Methods and Attributes
----------------------

All existing resources are derived from a ``BaseResource`` class which you usually won't inherit from
directly unless you want to add support for a new resource which Python-Redmine doesn't support.
Below you will find methods and attributes which can be redefined in your custom resource:

.. autoclass:: redminelib.resources.BaseResource
   :members: __getattr__, __setattr__, decode, encode, bulk_decode, bulk_encode, raw, refresh, pre_create, post_create, pre_update, post_update, pre_delete, post_delete, save, delete, export, export_url, is_new
   :undoc-members:
   :private-members:
