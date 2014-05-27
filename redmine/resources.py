from datetime import datetime
from distutils.version import LooseVersion
from redmine.utilities import to_string
from redmine.managers import ResourceManager
from redmine.exceptions import (
    ResourceAttrError,
    ReadonlyAttrError,
    CustomFieldValueError,
    ResourceVersionMismatchError
)

# Resources which when accessed from some other
# resource should become a ResourceSet object
_RESOURCE_SET_MAP = {
    'trackers': 'Tracker',
    'issue_categories': 'IssueCategory',
    'custom_fields': 'CustomField',
    'groups': 'Group',
    'users': 'User',
    'memberships': 'ProjectMembership',
    'relations': 'IssueRelation',
    'attachments': 'Attachment',
    'watchers': 'User',
    'journals': 'IssueJournal',
    'children': 'Issue',
    'roles': 'Role',
}

# Resources which when accessed from some other
# resource should become a Resource object
_RESOURCE_MAP = {
    'author': 'User',
    'assigned_to': 'User',
    'project': 'Project',
    'tracker': 'Tracker',
    'status': 'IssueStatus',
    'user': 'User',
    'issue': 'Issue',
    'priority': 'Enumeration',
    'activity': 'Enumeration',
    'category': 'IssueCategory',
    'fixed_version': 'Version',
}

# Resources which when access from some other
# resource should be requested from Redmine
_RESOURCE_RELATIONS_MAP = {
    'wiki_pages': 'WikiPage',
    'memberships': 'ProjectMembership',
    'issue_categories': 'IssueCategory',
    'versions': 'Version',
    'news': 'News',
    'relations': 'IssueRelation',
    'time_entries': 'TimeEntry',
    'issues': 'Issue',
}

# Resource attributes which when set should
# also set another resource id to its value
_RESOURCE_SINGLE_ATTR_ID_MAP = {
    'parent_id': 'parent',
    'project_id': 'project',
    'tracker_id': 'tracker',
    'priority_id': 'priority',
    'assigned_to_id': 'assigned_to',
    'category_id': 'category',
    'fixed_version_id': 'fixed_version',
    'parent_issue_id': 'parent',
    'issue_id': 'issue',
    'activity_id': 'activity',
}

# Resource attributes which when set should
# also set another resource ids to their value
_RESOURCE_MULTIPLE_ATTR_ID_MAP = {
    'user_ids': 'users',
    'role_ids': 'roles',
}


class _Resource(object):
    """Implementation of Redmine resource"""
    redmine_version = None
    container_all = None
    container_one = None
    container_filter = None
    container_create = None
    container_update = None
    query_all = None
    query_one = None
    query_filter = None
    query_create = None
    query_update = None
    query_delete = None

    _includes = ()
    _relations = ()
    _unconvertible = ()
    _members = ('manager',)
    _readonly = ('id', 'created_on', 'updated_on', 'author', 'user', 'project', 'issue')
    __length_hint__ = None  # fixes Python 2.6 list() call on resource object

    def __init__(self, manager, attributes):
        """Accepts manager instance object and resource attributes dict"""
        self.manager = manager
        self._attributes = dict((include, None) for include in self._includes)
        self._attributes.update(dict((relation, None) for relation in self._relations))
        self._attributes.update(attributes)
        self._readonly += self._relations + self._includes
        self._changes = {}

    def __getitem__(self, item):
        """Provides a dictionary like access to resource attributes"""
        return getattr(self, item)

    def __setitem__(self, item, value):
        """Provides a dictionary like setter for resource attributes"""
        return setattr(self, item, value)

    def __getattr__(self, item):
        """Returns the requested attribute and makes a conversion if needed"""
        if item in self._attributes:
            # If item shouldn't be converted let's return it as it is
            if item in self._unconvertible:
                return self._attributes[item]

            # If item should be a Resource object, let's convert it
            elif item in _RESOURCE_MAP:
                manager = ResourceManager(self.manager.redmine, _RESOURCE_MAP[item])
                return manager.to_resource(self._attributes[item])

            # If item should be a ResourceSet object, let's convert it
            elif item in _RESOURCE_SET_MAP and self._attributes[item] is not None:
                manager = ResourceManager(self.manager.redmine, _RESOURCE_SET_MAP[item])
                return manager.to_resource_set(self._attributes[item])

            # If item is a relation and should be requested from Redmine, let's do it
            elif item in self._relations and self._attributes[item] is None:
                filters = {'{0}_id'.format(self.__class__.__name__.lower()): self.internal_id}
                manager = ResourceManager(self.manager.redmine, _RESOURCE_RELATIONS_MAP[item])
                self._attributes[item] = manager.filter(**filters)
                return self._attributes[item]

            # If item is an include and should be requested from Redmine, let's do it
            elif item in self._includes and self._attributes[item] is None:
                self._attributes[item] = self.refresh(include=item)._attributes[item] or []
                return getattr(self, item)

        try:
            # If the requested item is a date/datetime string
            # we need to convert it to the appropriate object
            possible_dt = str(self._attributes[item])

            try:
                return datetime.strptime(possible_dt, self.manager.redmine.datetime_format)
            except ValueError:
                return datetime.strptime(possible_dt, self.manager.redmine.date_format).date()
        except ValueError:
            return self._attributes[item]
        except KeyError:
            if self.is_new():
                if item in ('id', 'version'):
                    return 0
                return ''

            return self._action_if_attribute_absent()

    def __setattr__(self, item, value):
        """Sets the requested attribute"""
        if item in self._members or item.startswith('_'):
            super(_Resource, self).__setattr__(item, value)
        elif item in self._readonly:
            raise ReadonlyAttrError()
        elif item == 'custom_fields':
            for org_index, org_field in enumerate(self._attributes.setdefault('custom_fields', [])):
                if 'value' not in org_field:
                    self._attributes['custom_fields'][org_index]['value'] = '0'

                try:
                    for new_index, new_field in enumerate(value):
                        if org_field['id'] == new_field['id']:
                            self._attributes['custom_fields'][org_index]['value'] = value.pop(new_index)['value']
                except (TypeError, KeyError):
                    raise CustomFieldValueError()

            self._attributes['custom_fields'].extend(value)
            self._changes[item] = self._attributes['custom_fields']
        else:
            value = self.manager.prepare_params({item: value})[item]
            self._changes[item] = value
            self._attributes[item] = value

            if item in _RESOURCE_SINGLE_ATTR_ID_MAP:
                self._attributes[_RESOURCE_SINGLE_ATTR_ID_MAP[item]] = {'id': value}
            elif item in _RESOURCE_MULTIPLE_ATTR_ID_MAP:
                self._attributes[_RESOURCE_MULTIPLE_ATTR_ID_MAP[item]] = [{'id': member_id} for member_id in value]

    def refresh(self, **params):
        """Reloads resource data from Redmine"""
        return self.manager.get(self.internal_id, **params)

    def pre_create(self):
        """Tasks that should be done before creating the resource"""
        pass

    def post_create(self):
        """Tasks that should be done after creating the resource"""
        pass

    def pre_update(self):
        """Tasks that should be done before updating the resource"""
        pass

    def post_update(self):
        """Tasks that should be done after updating the resource"""
        pass

    def save(self):
        """Creates or updates a resource"""
        if not self.is_new():
            self.pre_update()
            self.manager.update(self.internal_id, **self._changes)
            self._attributes['updated_on'] = datetime.utcnow().strftime(self.manager.redmine.datetime_format)
            self.post_update()
        else:
            self.pre_create()
            for item, value in self.manager.create(**self._changes):
                self._attributes[item] = value
            self.post_create()

        self._changes = {}
        return True

    @classmethod
    def translate_params(cls, params):
        """Translates internal param names to the real Redmine param names if needed"""
        return params

    @property
    def url(self):
        """Returns full url to the resource for humans if there is one"""
        if self.query_one is not None:
            return '{0}{1}'.format(
                self.manager.redmine.url,
                self.query_one.format(self.internal_id).replace('.json', '')
            )
        else:
            return None

    @property
    def internal_id(self):
        """Returns identifier of the resource for usage in internals of the library"""
        return self.id

    def is_new(self):
        """Checks if resource was just created and not yet saved to Redmine or it is existent resource"""
        return False if 'id' in self._attributes or 'created_on' in self._attributes else True

    def _action_if_attribute_absent(self):
        """Whether we should raise an exception in case of attribute absence or just return None"""
        raise_attr_exception = self.manager.redmine.raise_attr_exception

        if isinstance(raise_attr_exception, bool) and raise_attr_exception:
            raise ResourceAttrError()
        elif isinstance(raise_attr_exception, (list, tuple)) and self.__class__.__name__ in raise_attr_exception:
            raise ResourceAttrError()

        return None

    def __dir__(self):
        """We need to show only real Redmine resource attributes on dir() call"""
        return list(self._attributes.keys())

    def __iter__(self):
        """Provides a way to iterate through resource attributes and its values"""
        return iter(self._attributes.items())

    def __int__(self):
        """Integer representation of the Redmine resource object"""
        return self.id

    def __str__(self):
        """Informal representation of the Redmine resource object"""
        return to_string(self.name)

    def __repr__(self):
        """Official representation of the Redmine resource object"""
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            to_string(self.name)
        )


class Project(_Resource):
    redmine_version = '1.0'
    container_all = 'projects'
    container_one = 'project'
    container_create = 'project'
    container_update = 'project'
    query_all = '/projects.json'
    query_one = '/projects/{0}.json'
    query_create = '/projects.json'
    query_update = '/projects/{0}.json'
    query_delete = '/projects/{0}.json'

    _includes = ('trackers', 'issue_categories')
    _relations = ('wiki_pages', 'memberships', 'issue_categories', 'versions', 'news', 'issues')
    _unconvertible = ('status',)
    _readonly = _Resource._readonly + ('identifier',)

    def __getattr__(self, item):
        if item == 'parent' and item in self._attributes:
            return ResourceManager(self.manager.redmine, 'Project').to_resource(self._attributes[item])

        return super(Project, self).__getattr__(item)


class Issue(_Resource):
    redmine_version = '1.0'
    container_all = 'issues'
    container_one = 'issue'
    container_filter = 'issues'
    container_create = 'issue'
    container_update = 'issue'
    query_all = '/issues.json'
    query_one = '/issues/{0}.json'
    query_filter = '/issues.json'
    query_create = '/projects/{project_id}/issues.json'
    query_update = '/issues/{0}.json'
    query_delete = '/issues/{0}.json'

    _includes = ('children', 'attachments', 'relations', 'changesets', 'journals', 'watchers')
    _relations = ('relations', 'time_entries')
    _readonly = _Resource._readonly + ('spent_hours',)

    class Watcher:
        """An issue watcher implementation"""
        def __init__(self, issue):
            self._redmine = issue.manager.redmine
            self._issue_id = issue.internal_id

            if self._redmine.ver is not None and LooseVersion(str(self._redmine.ver)) < LooseVersion('2.3'):
                raise ResourceVersionMismatchError()

        def add(self, user_id):
            """Adds user to issue watchers list"""
            url = '{0}/issues/{1}/watchers.json'.format(self._redmine.url, self._issue_id)
            return self._redmine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """Removes user from issue watchers list"""
            url = '{0}/issues/{1}/watchers/{2}.json'.format(self._redmine.url, self._issue_id, user_id)
            return self._redmine.request('delete', url)

    def __getattr__(self, item):
        if item == 'version':
            return super(Issue, self).__getattr__('fixed_version')
        elif item == 'watcher':
            return Issue.Watcher(self)
        elif item == 'parent' and item in self._attributes:
            return ResourceManager(self.manager.redmine, 'Issue').to_resource(self._attributes[item])

        return super(Issue, self).__getattr__(item)

    def __setattr__(self, item, value):
        if item == 'version_id':
            return super(Issue, self).__setattr__('fixed_version_id', value)

        return super(Issue, self).__setattr__(item, value)

    def __str__(self):
        try:
            return to_string(self.subject)
        except ResourceAttrError:
            return str(self.id)

    def __repr__(self):
        try:
            return '<{0}.{1} #{2} "{3}">'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id,
                to_string(self.subject)
            )
        except ResourceAttrError:
            return '<{0}.{1} #{2}>'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id
            )


class TimeEntry(_Resource):
    redmine_version = '1.1'
    container_all = 'time_entries'
    container_one = 'time_entry'
    container_filter = 'time_entries'
    container_create = 'time_entry'
    container_update = 'time_entry'
    query_all = '/time_entries.json'
    query_one = '/time_entries/{0}.json'
    query_filter = '/time_entries.json'
    query_create = '/time_entries.json'
    query_update = '/time_entries/{0}.json'
    query_delete = '/time_entries/{0}.json'

    @classmethod
    def translate_params(cls, params):
        if 'from_date' in params:
            params['from'] = params.pop('from_date')

        if 'to_date' in params:
            params['to'] = params.pop('to_date')

        return super(TimeEntry, cls).translate_params(params)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Enumeration(_Resource):
    redmine_version = '2.2'
    container_filter = '{resource}'
    query_filter = '/enumerations/{resource}.json'

    @property
    def url(self):
        return '{0}/enumerations/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Attachment(_Resource):
    redmine_version = '1.3'
    container_one = 'attachment'
    query_one = '/attachments/{0}.json'

    def __str__(self):
        return to_string(self.filename)

    def __repr__(self):
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            to_string(self.filename)
        )


class IssueJournal(_Resource):
    redmine_version = '1.0'

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class WikiPage(_Resource):
    redmine_version = '2.2'
    container_filter = 'wiki_pages'
    container_one = 'wiki_page'
    container_create = 'wiki_page'
    container_update = 'wiki_page'
    query_filter = '/projects/{project_id}/wiki/index.json'
    query_one = '/projects/{project_id}/wiki/{0}.json'
    query_create = '/projects/{project_id}/wiki/{title}.json'
    query_update = '/projects/{project_id}/wiki/{0}.json'
    query_delete = '/projects/{project_id}/wiki/{0}.json'

    _includes = ('attachments',)
    _readonly = _Resource._readonly + ('version',)

    def refresh(self, **params):
        return super(WikiPage, self).refresh(**dict(params, project_id=self.manager.params.get('project_id', 0)))

    def post_update(self):
        self._attributes['version'] = self._attributes.get('version', 0) + 1

    @property
    def url(self):
        return '{0}{1}'.format(
            self.manager.redmine.url,
            self.query_one.format(
                self.internal_id,
                project_id=self.manager.params.get('project_id', 0)
            ).replace('.json', '')
        )

    @property
    def internal_id(self):
        return self.title

    def __getattr__(self, item):
        # If a text attribute of a resource is missing, we should
        # refresh a resource automatically for user's convenience
        try:
            return super(WikiPage, self).__getattr__(item)
        except ResourceAttrError:
            if 'text' not in self._attributes:
                self._attributes = self.refresh()._attributes

            return super(WikiPage, self).__getattr__(item)

    def __int__(self):
        return self.version

    def __str__(self):
        return to_string(self.title)

    def __repr__(self):
        return '<{0}.{1} "{2}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            to_string(self.title)
        )


class ProjectMembership(_Resource):
    redmine_version = '1.4'
    container_filter = 'memberships'
    container_one = 'membership'
    container_update = 'membership'
    container_create = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{0}.json'
    query_create = '/projects/{project_id}/memberships.json'
    query_update = '/memberships/{0}.json'
    query_delete = '/memberships/{0}.json'

    _readonly = _Resource._readonly + ('user', 'roles')

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class IssueCategory(_Resource):
    redmine_version = '1.3'
    container_filter = 'issue_categories'
    container_one = 'issue_category'
    container_update = 'issue_category'
    container_create = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{0}.json'
    query_create = '/projects/{project_id}/issue_categories.json'
    query_update = '/issue_categories/{0}.json'
    query_delete = '/issue_categories/{0}.json'


class IssueRelation(_Resource):
    redmine_version = '1.3'
    container_filter = 'relations'
    container_one = 'relation'
    container_create = 'relation'
    query_filter = '/issues/{issue_id}/relations.json'
    query_one = '/relations/{0}.json'
    query_create = '/issues/{issue_id}/relations.json'
    query_delete = '/relations/{0}.json'

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Version(_Resource):
    redmine_version = '1.3'
    container_filter = 'versions'
    container_one = 'version'
    container_create = 'version'
    container_update = 'version'
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{0}.json'
    query_create = '/projects/{project_id}/versions.json'
    query_update = '/versions/{0}.json'
    query_delete = '/versions/{0}.json'

    _unconvertible = ('status',)


class User(_Resource):
    redmine_version = '1.1'
    container_all = 'users'
    container_one = 'user'
    container_filter = 'users'
    container_create = 'user'
    container_update = 'user'
    query_all = '/users.json'
    query_one = '/users/{0}.json'
    query_filter = '/users.json'
    query_create = '/users.json'
    query_update = '/users/{0}.json'
    query_delete = '/users/{0}.json'

    _includes = ('memberships', 'groups')
    _unconvertible = ('status',)
    _readonly = _Resource._readonly + ('api_key', 'last_login_on', 'custom_fields')

    def __str__(self):
        try:
            return super(User, self).__str__()
        except ResourceAttrError:
            return '{0} {1}'.format(to_string(self.firstname), to_string(self.lastname))

    def __repr__(self):
        try:
            return super(User, self).__repr__()
        except ResourceAttrError:
            return '<{0}.{1} #{2} "{3} {4}">'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id,
                to_string(self.firstname),
                to_string(self.lastname)
            )


class Group(_Resource):
    redmine_version = '2.1'
    container_all = 'groups'
    container_one = 'group'
    container_create = 'group'
    container_update = 'group'
    query_all = '/groups.json'
    query_one = '/groups/{0}.json'
    query_create = '/groups.json'
    query_update = '/groups/{0}.json'
    query_delete = '/groups/{0}.json'

    _includes = ('memberships', 'users')

    class User:
        """A group user implementation"""
        def __init__(self, group):
            self._redmine = group.manager.redmine
            self._group_id = group.internal_id

        def add(self, user_id):
            """Adds user to a group"""
            url = '{0}/groups/{1}/users.json'.format(self._redmine.url, self._group_id)
            return self._redmine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """Removes user from a group"""
            url = '{0}/groups/{1}/users/{2}.json'.format(self._redmine.url, self._group_id, user_id)
            return self._redmine.request('delete', url)

    def __getattr__(self, item):
        if item == 'user':
            return Group.User(self)

        return super(Group, self).__getattr__(item)


class Role(_Resource):
    redmine_version = '1.4'
    container_all = 'roles'
    container_one = 'role'
    query_all = '/roles.json'
    query_one = '/roles/{0}.json'


class News(_Resource):
    redmine_version = '1.1'
    container_all = 'news'
    container_filter = 'news'
    query_all = '/news.json'
    query_filter = '/news.json'

    @property
    def url(self):
        return '{0}/news/{1}'.format(self.manager.redmine.url, self.internal_id)

    def __repr__(self):
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            to_string(self.title)
        )


class IssueStatus(_Resource):
    redmine_version = '1.3'
    container_all = 'issue_statuses'
    query_all = '/issue_statuses.json'

    @property
    def url(self):
        return '{0}/issue_statuses/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Tracker(_Resource):
    redmine_version = '1.3'
    container_all = 'trackers'
    query_all = '/trackers.json'

    @property
    def url(self):
        return '{0}/trackers/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Query(_Resource):
    redmine_version = '1.3'
    container_all = 'queries'
    query_all = '/queries.json'

    @property
    def url(self):
        return '{0}/projects/{1}/issues?query_id={2}'.format(
            self.manager.redmine.url,
            self._attributes.get('project_id', 0),
            self.internal_id
        )


class CustomField(_Resource):
    redmine_version = '2.4'
    container_all = 'custom_fields'
    query_all = '/custom_fields.json'

    @property
    def url(self):
        return '{0}/custom_fields/{1}/edit'.format(self.manager.redmine.url, self.internal_id)

    def __getattr__(self, item):
        # If custom field was created after the creation of the resource,
        # i.e. project, and it's not used in the resource, there will be
        # no value attribute defined, that is why we need to return 0 or
        # we'll get an exception
        if item == 'value' and not item in self._attributes:
            return 0

        return super(CustomField, self).__getattr__(item)
