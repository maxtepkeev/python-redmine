TODO
====

- Create, Update, Delete operations for resources
- Add include support to relations, i.e. in addition to redmine.group.get(1, include='users')
  should also be retrieved on demand via group.users if include wasn't set
- Some API features for some resources are only available starting from specific Redmine version,
  we should check for this and raise an exception if specific feature is not available
