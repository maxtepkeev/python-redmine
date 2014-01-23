Changelog
=========

0.3.2 (2014-0X-XX)
------------------

- Added: New exceptions:

  * ConflictError
  * ReadonlyAttrError

0.3.1 (2014-01-23)
------------------

- Added: An ability to pass Requests parameters as a dictionary via requests keyword
  argument on Redmine initialization, i.e. Redmine('\http://redmine.url', requests={}).
- Fixed: `Issue #1 <https://github.com/maxtepkeev/python-redmine/issues/1>`_ (unable
  to connect to Redmine server with invalid ssl certificate).

0.3.0 (2014-01-18)
------------------

- Added: Delete functionality for resources via delete method (see docs for details):

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

- Changed: ResourceManager get() method now raises a ``ValidationError`` exception if
  required keyword arguments aren't passed

0.2.0 (2014-01-16)
------------------

- Added: New exceptions:

  * ServerError
  * NoFileError
  * ValidationError
  * VersionMismatchError
  * ResourceNoFieldsProvidedError
  * ResourceNotFoundError

- Added: Create functionality for resources via create method (see docs for details):

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

- Added: File upload support, see upload() method in Redmine class
- Added: Integer representation to all resources, i.e. __int__()
- Added: Informal string representation to all resources, i.e. __str__()
- Fixed: Conversion of issue priorities to enumeration resource object didn't work
- Changed: Renamed version attribute to redmine_version in all resources to avoid name intersections
- Changed: ResourceManager get() method now raises a ``ResourceNotFoundError`` exception if
  resource wasn't found instead of returning None in previous versions
- Changed: reimplemented fix for __repr__() from 0.1.1

0.1.1 (2014-01-10)
------------------

- Added: Python 2.6 support
- Fixed: Resource representation, i.e. __repr__(), was broken in Python 2.7
- Fixed: dir() call on a resource object didn't work in Python 3.2
- Changed: WikiPage resource refresh() method now automatically determines it's project_id

0.1.0 (2014-01-09)
------------------

- Initial release
