Changelog
---------

1.1.1 (2015-03-XX)
++++++++++++++++++

- Fixed: `Issue #85 <https://github.com/maxtepkeev/python-redmine/issues/85>`__ (Python Redmine
  was trying to convert field to date/datetime even when it shouldn't, i.e. if a field looked like
  YYYY-MM-DD but wasn't actually a date/datetime field, e.g. wiki page title or issue subject)

1.1.0 (2015-02-20)
++++++++++++++++++

- Added: PyPy2/3 is now officially supported
- Added: Introduced ``enabled_modules`` on demand include in Project resource
- Fixed: `Issue #78 <https://github.com/maxtepkeev/python-redmine/issues/78>`__ (Redmine <2.5.2
  returns only single tracker instead of a list of all available trackers when requested from
  a CustomField resource which caused an Exception in Python Redmine, see `this <http://www.
  redmine.org/issues/16739>`__ for details)
- Fixed: `Issue #80 <https://github.com/maxtepkeev/python-redmine/issues/80>`__ (If a project
  is read-only or doesn't have CRM plugin enabled, an attempt to add/remove Contact resource
  to/from it will lead to improper error message)
- Fixed: `Issue #81 <https://github.com/maxtepkeev/python-redmine/issues/81>`__ (Contact's
  resource ``tag_list`` attribute was always splitted into single chars) (thanks to `Alexander
  Loechel <https://github.com/loechel>`__)

1.0.3 (2015-02-03)
++++++++++++++++++

- Fixed: `Issue #72 <https://github.com/maxtepkeev/python-redmine/issues/72>`__ (If an exception is
  raised during JSON decoding process, it should be catched and reraised as Python Redmine's own
  exception, i.e ``redmine.exceptions.JSONDecodeError``)
- Fixed: `Issue #76 <https://github.com/maxtepkeev/python-redmine/issues/76>`__ (It was impossible
  to retrieve more than 100 resources for resources which don't support limit/offset natively by
  Redmine, i.e. this functionality is emulated by Python Redmine, e.g. WikiPage, Groups, Roles etc)

1.0.2 (2014-11-13)
++++++++++++++++++

- Fixed: `Issue #55 <https://github.com/maxtepkeev/python-redmine/issues/55>`__ (TypeError was
  raised during processing validation errors from Redmine when one of the errors was returned as
  a list)
- Fixed: `Issue #59 <https://github.com/maxtepkeev/python-redmine/issues/59>`__ (Raise ForbiddenError
  when a 403 is encountered) (thanks to `Rick Harris <https://github.com/rconradharris>`__)
- Fixed: `Issue #64 <https://github.com/maxtepkeev/python-redmine/issues/64>`__ (Redmine and Resource
  classes weren't picklable) (thanks to `Rick Harris <https://github.com/rconradharris>`__)
- Fixed: A ResourceSet object with a limit=100, actually returned 125 Resource objects

1.0.1 (2014-09-23)
++++++++++++++++++

- Fixed: `Issue #50 <https://github.com/maxtepkeev/python-redmine/issues/50>`__ (IssueJournal's
  ``notes`` attribute was converted to Note resource by mistake, bug was introduced in v1.0.0)

1.0.0 (2014-09-22)
++++++++++++++++++

- Added: Support for the `CRM plugin <http://redminecrm.com/projects/crm/pages/1>`_ resources:

  * `Contact <http://python-redmine.readthedocs.org/resources/contact.html>`_
  * `ContactTag <http://python-redmine.readthedocs.org/resources/contact_tag.html>`_
  * `Note <http://python-redmine.readthedocs.org/resources/note.html>`_
  * `Deal <http://python-redmine.readthedocs.org/resources/deal.html>`_
  * `DealStatus <http://python-redmine.readthedocs.org/resources/deal_status.html>`_
  * `DealCategory <http://python-redmine.readthedocs.org/resources/deal_category.html>`_
  * `CrmQuery <http://python-redmine.readthedocs.org/resources/crm_query.html>`_

- Added: Introduced new relations for the following resource objects:

  * Project - time_entries, deals, contacts and deal_categories relations
  * User - issues, time_entries, deals and contacts relations
  * Tracker - issues relation
  * IssueStatus - issues relation

- Added: Introduced a ``values()`` method in a ResourceSet which returns ValuesResourceSet — a
  ResourceSet subclass that returns dictionaries when used as an iterable, rather than resource-instance
  objects (see `docs <http://python-redmine.readthedocs.org/operations.html#filter>`__ for details)
- Added: Introduced ``update()`` and ``delete()`` methods in a ResourceSet object which allow to
  bulk update or bulk delete all resources in a ResourceSet object (see `docs <http://python-redmine.
  readthedocs.org/operations.html#filter>`__ for details)
- Fixed: It was impossible to use ResourceSet's ``get()`` and ``filter()`` methods with WikiPage
  resource
- Fixed: Several small fixes and enhancements here and there

0.9.0 (2014-09-11)
++++++++++++++++++

- Added: Introduced support for file downloads (see `docs <http://python-redmine.readthedocs.
  org/advanced/working_with_files.html>`__ for details)
- Added: Introduced new ``_Resource.requirements`` class attribute where all Redmine plugins
  required by resource should be listed (preparations to support non-native resources)
- Added: New exceptions:

  * ResourceRequirementsError

- Fixed: It was impossible to set a custom field of date/datetime type using date/datetime
  Python objects
- Fixed: `Issue #46 <https://github.com/maxtepkeev/python-redmine/issues/46>`__
  (A UnicodeEncodeError was raised in Python 2.x while trying to access a ``url`` property of
  a WikiPage resource if it contained non-ascii characters)

0.8.4 (2014-08-08)
++++++++++++++++++

- Added: Support for anonymous Attachment resource (i.e. attachment with ``id`` attr only)
- Fixed: `Issue #42 <https://github.com/maxtepkeev/python-redmine/issues/42>`__ (It was
  impossible to create a Project resource via ``new()`` method)

0.8.3 (2014-08-01)
++++++++++++++++++

- Fixed: `Issue #39 <https://github.com/maxtepkeev/python-redmine/issues/39>`__ (It was
  impossible to save custom_fields in User resource via ``new()`` method)

0.8.2 (2014-05-27)
++++++++++++++++++

- Added: ResourceSet's ``get()`` method now supports a ``default`` keyword argument which is
  returned when a requested Resource can't be found in a ResourceSet and defaults to ``None``,
  previously this was hardcoded to ``None``
- Added: It is now possible to use ``getattr()`` with default value without raising a
  ``ResourceAttrError`` when calling non-existent resource attribute, see `Issue #30
  <https://github.com/maxtepkeev/python-redmine/issues/30>`__ for details (thanks to
  `hsum <https://github.com/hsum>`__)
- Fixed: `Issue #31 <https://github.com/maxtepkeev/python-redmine/issues/31>`__ (Unlimited
  recursion was possible in some situations when on demand includes were used)

0.8.1 (2014-04-02)
++++++++++++++++++

- Added: New exceptions:

  * RequestEntityTooLargeError
  * UnknownError

- Fixed: `Issue #27 <https://github.com/maxtepkeev/python-redmine/issues/27>`__ (Project and
  Issue resources ``parent`` attribute was returned as a dict instead of being converted to
  Resource object)

0.8.0 (2014-03-27)
++++++++++++++++++

- Added: Introduced the detection of conflicting packages, i.e. if a conflicting package is
  found (PyRedmineWS at this time is the only one), the installation procedure will be aborted
  and a warning message will be shown with the detailed description of the problem
- Added: Introduced new ``_Resource._members`` class attribute where all instance attributes
  which are not started with underscore should be listed. This will resolve recursion issues
  in custom resources because of how ``__setattr__()`` works in Python
- Changed: ``_Resource.attributes`` renamed to ``_Resource._attributes``
- Fixed: Python Redmine was unable to upload any binary files
- Fixed: `Issue #20 <https://github.com/maxtepkeev/python-redmine/issues/20>`__ (Lowered
  Requests version requirements. Python Redmine now requires Requests starting from 0.12.1
  instead of 2.1.0 in previous versions)
- Fixed: `Issue #23 <https://github.com/maxtepkeev/python-redmine/issues/23>`__ (File uploads
  via ``update()`` method didn't work)

0.7.2 (2014-03-17)
++++++++++++++++++

- Fixed: `Issue #19 <https://github.com/maxtepkeev/python-redmine/issues/19>`__ (Resources
  obtained via ``filter()`` and ``all()`` methods have incomplete url attribute)
- Fixed: Redmine server url with forward slash could cause errors in rare cases
- Fixed: Python Redmine was incorrectly raising ``ResourceAttrError`` when trying to call
  ``repr()`` on a News resource

0.7.1 (2014-03-14)
++++++++++++++++++

- Fixed: `Issue #16 <https://github.com/maxtepkeev/python-redmine/issues/16>`__ (When a resource
  was created via a ``new()`` method, the next resource created after that inherited all the
  attribute values of the previous resource)

0.7.0 (2014-03-12)
++++++++++++++++++

- Added: WikiPage resource now automatically requests all of it's available attributes from
  Redmine in case if some of them are not available in an existent resource object
- Added: Support for setting date/datetime resource attributes using date/datetime Python objects
- Added: Support for using date/datetime Python objects in all ResourceManager methods, i.e.
  ``new()``, ``create()``, ``update()``, ``delete()``, ``get()``, ``all()``, ``filter()``
- Fixed: `Issue #14 <https://github.com/maxtepkeev/python-redmine/issues/14>`__ (Python Redmine
  was incorrectly raising ``ResourceAttrError`` when trying to call ``repr()``, ``str()`` and
  ``int()`` on resources, created via ``new()`` method)

0.6.2 (2014-03-09)
++++++++++++++++++

- Fixed: Project resource ``status`` attribute was converted to IssueStatus resource by mistake

0.6.1 (2014-02-27)
++++++++++++++++++

- Fixed: `Issue #10 <https://github.com/maxtepkeev/python-redmine/issues/10>`__ (Python
  Redmine was incorrectly raising ``ResourceAttrError`` while creating some resources via
  ``new()`` method)

0.6.0 (2014-02-19)
++++++++++++++++++

- Added: ``Redmine.auth()`` shortcut for the case if we just want to check if user provided
  valid auth credentials, can be used for user authentication on external resource based on
  Redmine user database (see `docs <http://python-redmine.readthedocs.org/advanced/
  external_auth.html>`__ for details)
- Fixed: ``JSONDecodeError`` was raised in some Redmine versions during some create/update
  operations (thanks to `0x55aa <https://github.com/0x55aa>`__)
- Fixed: User resource ``status`` attribute was converted to IssueStatus resource by mistake

0.5.0 (2014-02-09)
++++++++++++++++++

- Added: An ability to create custom resources which allow to easily redefine the behaviour
  of existing resources (see `docs <http://python-redmine.readthedocs.org/advanced/
  custom_resources.html>`__ for details)
- Added: An ability to add/remove watcher to/from issue (see `docs
  <http://python-redmine.readthedocs.org/resources/issue.html#watchers>`__ for details)
- Added: An ability to add/remove users to/from group (see `docs
  <http://python-redmine.readthedocs.org/resources/group.html#users>`__ for details)

0.4.0 (2014-02-08)
++++++++++++++++++

- Added: New exceptions:

  * ConflictError
  * ReadonlyAttrError
  * ResultSetTotalCountError
  * CustomFieldValueError

- Added: Update functionality via ``update()`` and ``save()`` methods for resources (see
  `docs <http://python-redmine.readthedocs.org/operations.html#update>`__ for details):

  * User
  * Group
  * IssueCategory
  * Version
  * TimeEntry
  * ProjectMembership
  * WikiPage
  * Project
  * Issue

- Added: Limit/offset support via ``all()`` and ``filter()`` methods for resources that
  doesn't support that feature via Redmine:

  * IssueRelation
  * Version
  * WikiPage
  * IssueStatus
  * Tracker
  * Enumeration
  * IssueCategory
  * Role
  * Group
  * CustomField

- Added: On demand includes, e.g. in addition to ``redmine.group.get(1, include='users')``
  users for a group can also be retrieved on demand via ``group.users`` if include wasn't set
  (see `docs <http://python-redmine.readthedocs.org/resources/index.html>`__ for details)
- Added: ``total_count`` attribute to ResourceSet object which holds the total number
  of resources for the current resource type available in Redmine (thanks to
  `Andrei Avram <https://github.com/andreiavram>`__)
- Added: An ability to return ``None`` instead of raising a ``ResourceAttrError`` for all
  or selected resource objects via ``raise_attr_exception`` kwarg on Redmine object (see
  `docs <http://python-redmine.readthedocs.org/configuration.html#exception-control>`__ for
  details or `Issue #6 <https://github.com/maxtepkeev/python-redmine/issues/6>`__)
- Added: ``pre_create()``, ``post_create()``, ``pre_update()``, ``post_update()`` resource
  object methods which can be used to execute tasks that should be done before/after
  creating/updating the resource through ``save()`` method
- Added: Allow to create resources in alternative way via ``new()`` method (see `docs
  <http://python-redmine.readthedocs.org/operations.html#new>`__ for details)
- Added: Allow daterange TimeEntry resource filtering via ``from_date`` and ``to_date``
  keyword arguments (thanks to `Antoni Aloy <https://github.com/aaloy>`__)
- Added: An ability to retrieve Issue version via ``version`` attribute in addition to
  ``fixed_version`` to be more obvious
- Changed: Documentation for resources rewritten from scratch to be more understandable
- Fixed: Saving custom fields to Redmine didn't work in some situations
- Fixed: Issue's ``fixed_version`` attribute was retrieved as dict instead of Version resource
  object
- Fixed: Resource relations were requested from Redmine every time instead of caching the
  result after first request
- Fixed: `Issue #2 <https://github.com/maxtepkeev/python-redmine/issues/2>`__ (limit/offset
  as keyword arguments were broken)
- Fixed: `Issue #5 <https://github.com/maxtepkeev/python-redmine/issues/5>`__ (Version
  resource ``status`` attribute was converted to IssueStatus resource by mistake) (thanks
  to `Andrei Avram <https://github.com/andreiavram>`__)
- Fixed: A lot of small fixes, enhancements and refactoring here and there

0.3.1 (2014-01-23)
++++++++++++++++++

- Added: An ability to pass Requests parameters as a dictionary via ``requests`` keyword
  argument on Redmine initialization, i.e. Redmine('\http://redmine.url', requests={}).
- Fixed: `Issue #1 <https://github.com/maxtepkeev/python-redmine/issues/1>`__ (unable
  to connect to Redmine server with invalid ssl certificate).

0.3.0 (2014-01-18)
++++++++++++++++++

- Added: Delete functionality via ``delete()`` method for resources (see `docs
  <http://python-redmine.readthedocs.org/operations.html#delete>`__ for details):

  * User
  * Group
  * IssueCategory
  * Version
  * TimeEntry
  * IssueRelation
  * ProjectMembership
  * WikiPage
  * Project
  * Issue

- Changed: ResourceManager ``get()`` method now raises a ``ValidationError`` exception if
  required keyword arguments aren't passed

0.2.0 (2014-01-16)
++++++++++++++++++

- Added: New exceptions:

  * ServerError
  * NoFileError
  * ValidationError
  * VersionMismatchError
  * ResourceNoFieldsProvidedError
  * ResourceNotFoundError

- Added: Create functionality via ``create()`` method for resources (see `docs
  <http://python-redmine.readthedocs.org/operations.html#create>`__ for details):

  * User
  * Group
  * IssueCategory
  * Version
  * TimeEntry
  * IssueRelation
  * ProjectMembership
  * WikiPage
  * Project
  * Issue

- Added: File upload support, see ``upload()`` method in Redmine class
- Added: Integer representation to all resources, i.e. ``__int__()``
- Added: Informal string representation to all resources, i.e. ``__str__()``
- Changed: Renamed ``version`` attribute to ``redmine_version`` in all resources to avoid
  name intersections
- Changed: ResourceManager ``get()`` method now raises a ``ResourceNotFoundError`` exception
  if resource wasn't found instead of returning None in previous versions
- Changed: reimplemented fix for ``__repr__()`` from 0.1.1
- Fixed: Conversion of issue priorities to enumeration resource object didn't work

0.1.1 (2014-01-10)
++++++++++++++++++

- Added: Python 2.6 support
- Changed: WikiPage resource ``refresh()`` method now automatically determines it's project_id
- Fixed: Resource representation, i.e. ``__repr__()``, was broken in Python 2.7
- Fixed: ``dir()`` call on a resource object didn't work in Python 3.2

0.1.0 (2014-01-09)
++++++++++++++++++

- Initial release
