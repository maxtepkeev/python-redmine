Changelog
---------

2.0.1 (2017-04-10)
++++++++++++++++++

- Fix PyPI package

2.0.0 (2017-04-10)
++++++++++++++++++

This version brings a lot of new features and changes, some of them are backward-incompatible, so please
look carefully at the changelog below to find out what needs to be changed in your code to make it work
with this version. Also Python-Redmine now comes in 2 editions: Standard and Pro, please have a look at
this `document <https://python-redmine.com/editions.html>`__ for more details. Documentation was
also significantly rewritten, so it is recommended to reread it even if you are an experienced Python-Redmine
user.

**New Features**:

- RedmineUP `Checklist plugin <https://www.redmineup.com/pages/plugins/checklists>`__ support
- `Request Engines <https://python-redmine.com/advanced/request_engines.html>`__ support. It is
  now possible to create engines to define how requests to Redmine are made, e.g. synchronous (one by one)
  or asynchronous using threads or processes etc
- ``redmine.session()`` context manager which allows to temporary redefine engine's behaviour
- Search API support (`Issue #138 <https://github.com/maxtepkeev/python-redmine/issues/138>`__)
- Export functionality (`Issue #58 <https://github.com/maxtepkeev/python-redmine/issues/58>`__)
- REDMINE_USE_EXTERNAL_REQUESTS environmental variable for emergency cases which allows to use external
  requests instead of bundled one even if external requests version is lower than the bundled one
- Wrong HTTP protocol usage detector, e.g. one use HTTP when HTTPS should be used

**Improvements**:

- ResourceSet objects were completely rewritten:

  * ``ResourceSet`` object that was already sliced now supports reslicing
  * ``ResourceSet`` object's ``delete()``, ``update()``, ``filter()`` and ``get()`` methods have been
    optimized for speed
  * ``ResourceSet`` object's ``delete()`` and ``update()`` methods now call the corresponding Resource's
    ``pre_*()`` and ``post_*()`` methods
  * ``ResourceSet`` object's ``get()`` and ``filter()`` methods now supports non-integer id's, e.g.
    WikiPage's title can now be used with it
  * ``ValuesResourceSet`` class has been removed
  * ``ResourceSet.values()`` method now returns an iterable of dicts instead of ``ValuesResourceSet`` object
  * ``ResourceSet.values_list()`` method has been added which returns an iterable of tuples with Resource
    values or single values if flattened, i.e. ``flat=True``

- New ``Resource`` object methods:

  * ``delete()`` deletes current resource from Redmine
  * ``pre_delete()`` and ``post_delete()`` can be used to execute tasks that should be done before/after
    deleting the resource through ``delete()`` method
  * ``bulk_decode()``, ``bulk_encode()``, ``decode()`` and ``encode()`` which are used to translate
    attributes of the resource to/from Python/Redmine

- Attachment ``delete()`` method support (requires Redmine >= 3.3.0)
- RedmineUP CRM Note resource now provides ``type`` attribute which shows text representation of ``type_id``
- RedmineUP CRM DealStatus resource now provides ``status`` attribute which shows text representation of
  ``status_type``
- WikiPage resource now provides ``project_id`` attribute
- Unicode handling was significantly rewritten and shouldn't cause any more troubles
- ``UnknownError`` exception now contains ``status_code`` attribute which can be used to handle the
  exception instead of parsing code from exception's text
- Sync engine's speed improved to 8-12% depending on the amount of resources fetched

**Changes**:

- Renamed package name from ``redmine`` to ``redminelib``
- Resource class attributes that were previously tuples are now lists
- ``__Resource`` class renamed to ``Resource``
- ``Redmine.custom_resource_paths`` keyword argument renamed to ``resource_paths``
- ``Redmine.download()`` method now returns a `requests.Response <http://docs.python-requests.org/
  en/latest/api/#requests.Response>`__ object directly instead of ``iter_content()`` method if a ``savepath``
  param wasn't provided, this gives user even more control over response data
- ``Resource.refresh()`` now really refreshes itself instead of returning a new refreshed
  resource, to get the previous behaviour use ``itself`` param, e.g. ``Resource.refresh(itself=False)``
- Removed Python 3.2 support
- Removed ``container_filter``, ``container_create`` and ``container_update`` attributes on ``Resource``
  object in favor of ``container_many`` attribute
- Removed ``Resource.translate_params()`` and ``ResourceManager.prepare_params()`` in favor of
  ``Resource.bulk_decode()``
- Removed ``is_unicode()``, ``is_string()`` and ``to_string()`` from ``redminelib.utilities``
- Updated bundled requests library to v2.13.0

**Bugfixes**:

- Infinite loop when uploading zero-length files (`Issue #152 <https://github.com/maxtepkeev/python-redmine/
  issues/152>`__)
- Unsupported Redmine resource error while trying to use Python-Redmine without installation (`Issue #156
  <https://github.com/maxtepkeev/python-redmine/issues/156>`__)
- It was impossible to set ``data``, ``params`` and ``headers`` via ``requests`` keyword argument on
  Redmine object
- Calling ``str()`` or ``repr()`` on a Resource was giving incorrect results if exception raising
  was turned off for a resource

**Documentation**:

- Switched to the alabaster theme
- Added new sections:

  * `Editions <https://python-redmine.com/editions.html>`__
  * `Introduction <https://python-redmine.com/introduction.html>`__
  * `Request Engines <https://python-redmine.com/advanced/request_engines.html>`__

- Added info about Issue Journals (`Issue #120 <https://github.com/maxtepkeev/python-redmine/issues/120>`__)
- Added note about open/closed issues (`Issue #136 <https://github.com/maxtepkeev/python-redmine/issues/136>`__)
- Added note about regexp custom field filter (`Issue #164 <https://github.com/maxtepkeev/python-redmine/
  issues/164>`__)
- Added some new information here and there

1.5.1 (2016-03-27)
++++++++++++++++++

- Changed: Updated bundled requests package to 2.9.1
- Changed: `Issue #124 <https://github.com/maxtepkeev/python-redmine/issues/124>`__ (``project.url``
  now uses ``identifier`` rather than ``id`` to generate url for the project resource)
- Fixed: `Issue #122 <https://github.com/maxtepkeev/python-redmine/issues/122>`__ (``ValidationError`` for
  empty custom field values was possible under some circumstances with Redmine < 2.5.0)
- Fixed: `Issue #112 <https://github.com/maxtepkeev/python-redmine/issues/112>`__ (``UnicodeEncodeError``
  on Python 2 if ``resource_id`` was of ``unicode`` type) (thanks to `Digenis <https://github.com/Digenis>`__)

1.5.0 (2015-11-26)
++++++++++++++++++

- Added: Documented support for new fields and values in User, Issue and IssueRelation resources
- Added: `Issue #109 <https://github.com/maxtepkeev/python-redmine/issues/109>`__ (Smart imports for
  vendored packages (see `docs <https://python-redmine.com/installation.html#dependencies>`__
  for details)
- Added: `Issue #115 <https://github.com/maxtepkeev/python-redmine/issues/115>`__ (File upload support
  for WikiPage resource)

1.4.0 (2015-10-18)
++++++++++++++++++

- Added: `Requests <http://docs.python-requests.org>`__ is now embedded into Python-Redmine
- Added: Python-Redmine is now embeddable to other libraries
- Fixed: Previous release was broken on PyPI

1.3.0 (2015-10-18)
++++++++++++++++++

- Added: `Issue #108 <https://github.com/maxtepkeev/python-redmine/issues/108>`__ (Tests are now
  built-in into source package distributed via PyPI)

1.2.0 (2015-07-09)
++++++++++++++++++

- Added: `wheel <http://wheel.readthedocs.io>`__ support
- Added: `Issue #93 <https://github.com/maxtepkeev/python-redmine/issues/93>`__ (``JSONDecodeError``
  exception now contains a ``response`` attribute which can be inspected to identify the cause of the
  exception)
- Added: `Issue #98 <https://github.com/maxtepkeev/python-redmine/issues/98>`__ (Support for setting
  WikiPage resource parent title and converting parent attribute to Resource object instead of being
  a dict)

1.1.2 (2015-05-20)
++++++++++++++++++

- Fixed: `Issue #90 <https://github.com/maxtepkeev/python-redmine/issues/90>`__ (Python-Redmine
  fails to install on systems with LC_ALL=C) (thanks to `spikergit1 <https://github.com/spikergit1>`__)

1.1.1 (2015-03-26)
++++++++++++++++++

- Fixed: `Issue #85 <https://github.com/maxtepkeev/python-redmine/issues/85>`__ (Python-Redmine
  was trying to convert field to date/datetime even when it shouldn't, i.e. if a field looked like
  YYYY-MM-DD but wasn't actually a date/datetime field, e.g. wiki page title or issue subject)

1.1.0 (2015-02-20)
++++++++++++++++++

- Added: PyPy2/3 is now officially supported
- Added: Introduced ``enabled_modules`` on demand include in Project resource
- Fixed: `Issue #78 <https://github.com/maxtepkeev/python-redmine/issues/78>`__ (Redmine <2.5.2
  returns only single tracker instead of a list of all available trackers when requested from
  a CustomField resource which caused an Exception in Python-Redmine, see `this <http://www.
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
  raised during JSON decoding process, it should be catched and reraised as Python-Redmine's own
  exception, i.e ``redmine.exceptions.JSONDecodeError``)
- Fixed: `Issue #76 <https://github.com/maxtepkeev/python-redmine/issues/76>`__ (It was impossible
  to retrieve more than 100 resources for resources which don't support limit/offset natively by
  Redmine, i.e. this functionality is emulated by Python-Redmine, e.g. WikiPage, Groups, Roles etc)

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

- Added: Support for the `CRM plugin <https://www.redmineup.com/pages/plugins/crm>`__ resources:

  * `Contact <https://python-redmine.com/resources/contact.html>`__
  * `ContactTag <https://python-redmine.com/resources/contact_tag.html>`__
  * `Note <https://python-redmine.com/resources/note.html>`__
  * `Deal <https://python-redmine.com/resources/deal.html>`__
  * `DealStatus <https://python-redmine.com/resources/deal_status.html>`__
  * `DealCategory <https://python-redmine.com/resources/deal_category.html>`__
  * `CrmQuery <https://python-redmine.com/resources/crm_query.html>`__

- Added: Introduced new relations for the following resource objects:

  * Project - time_entries, deals, contacts and deal_categories relations
  * User - issues, time_entries, deals and contacts relations
  * Tracker - issues relation
  * IssueStatus - issues relation

- Added: Introduced a ``values()`` method in a ResourceSet which returns ValuesResourceSet - a
  ResourceSet subclass that returns dictionaries when used as an iterable, rather than resource-instance
  objects (see `docs <https://python-redmine.com/introduction.html#methods>`__ for details)
- Added: Introduced ``update()`` and ``delete()`` methods in a ResourceSet object which allow to
  bulk update or bulk delete all resources in a ResourceSet object (see
  `docs <https://python-redmine.com/introduction.html#methods>`__ for details)
- Fixed: It was impossible to use ResourceSet's ``get()`` and ``filter()`` methods with WikiPage
  resource
- Fixed: Several small fixes and enhancements here and there

0.9.0 (2014-09-11)
++++++++++++++++++

- Added: Introduced support for file downloads (see
  `docs <https://python-redmine.com/advanced/working_with_files.html>`__ for details)
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
- Fixed: Python-Redmine was unable to upload any binary files
- Fixed: `Issue #20 <https://github.com/maxtepkeev/python-redmine/issues/20>`__ (Lowered
  Requests version requirements. Python-Redmine now requires Requests starting from 0.12.1
  instead of 2.1.0 in previous versions)
- Fixed: `Issue #23 <https://github.com/maxtepkeev/python-redmine/issues/23>`__ (File uploads
  via ``update()`` method didn't work)

0.7.2 (2014-03-17)
++++++++++++++++++

- Fixed: `Issue #19 <https://github.com/maxtepkeev/python-redmine/issues/19>`__ (Resources
  obtained via ``filter()`` and ``all()`` methods have incomplete url attribute)
- Fixed: Redmine server url with forward slash could cause errors in rare cases
- Fixed: Python-Redmine was incorrectly raising ``ResourceAttrError`` when trying to call
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
- Fixed: `Issue #14 <https://github.com/maxtepkeev/python-redmine/issues/14>`__ (Python-Redmine
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
  Redmine user database (see `docs <https://python-redmine.com/advanced/external_auth.html>`__
  for details)
- Fixed: ``JSONDecodeError`` was raised in some Redmine versions during some create/update
  operations (thanks to `0x55aa <https://github.com/0x55aa>`__)
- Fixed: User resource ``status`` attribute was converted to IssueStatus resource by mistake

0.5.0 (2014-02-09)
++++++++++++++++++

- Added: An ability to create custom resources which allow to easily redefine the behaviour
  of existing resources (see `docs <https://python-redmine.com/advanced/custom_resources.html>`__
  for details)
- Added: An ability to add/remove watcher to/from issue (see `docs
  <https://python-redmine.com/resources/issue.html#watchers>`__ for details)
- Added: An ability to add/remove users to/from group (see `docs
  <https://python-redmine.com/resources/group.html#users>`__ for details)

0.4.0 (2014-02-08)
++++++++++++++++++

- Added: New exceptions:

  * ConflictError
  * ReadonlyAttrError
  * ResultSetTotalCountError
  * CustomFieldValueError

- Added: Update functionality via ``update()`` and ``save()`` methods for resources (see
  `docs <https://python-redmine.com/introduction.html#update>`__ for details):

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
  (see `docs <https://python-redmine.com/resources/index.html>`__ for details)
- Added: ``total_count`` attribute to ResourceSet object which holds the total number
  of resources for the current resource type available in Redmine (thanks to
  `Andrei Avram <https://github.com/andreiavram>`__)
- Added: An ability to return ``None`` instead of raising a ``ResourceAttrError`` for all
  or selected resource objects via ``raise_attr_exception`` kwarg on Redmine object (see
  `docs <https://python-redmine.com/configuration.html#exception-control>`__ for
  details or `Issue #6 <https://github.com/maxtepkeev/python-redmine/issues/6>`__)
- Added: ``pre_create()``, ``post_create()``, ``pre_update()``, ``post_update()`` resource
  object methods which can be used to execute tasks that should be done before/after
  creating/updating the resource through ``save()`` method
- Added: Allow to create resources in alternative way via ``new()`` method (see `docs
  <https://python-redmine.com/introduction.html#new>`__ for details)
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
  <https://python-redmine.com/introduction.html#delete>`__ for details):

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
  <https://python-redmine.com/introduction.html#id1>`__ for details):

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
