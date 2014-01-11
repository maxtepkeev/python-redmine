Changelog
=========

0.1.2 (2014-0X-XX)
------------------

Added: ``ServerError`` and ``ValidationError`` exceptions
Added: Create functionality for User resource
Changed: reimplemented fix for __repr__() from 0.1.1

0.1.1 (2014-01-10)
------------------

- Added: Python 2.6 support
- Fixed: Resource representation, i.e. __repr__(), was broken in Python 2.7
- Fixed: dir() call on a resource object didn't work in Python 3.2
- Changed: WikiPage resource refresh() method now automatically determines it's project_id

0.1.0 (2014-01-09)
------------------

- Initial release
