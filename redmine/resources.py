from datetime import datetime

from distutils.version import LooseVersion

from .utilities import to_string
from .managers import ResourceManager
from .exceptions import (
    ValidationError,
    ForbiddenError,
    ResourceAttrError,
    ReadonlyAttrError,
    CustomFieldValueError,
    ResourceVersionMismatchError,
    ResourceNotFoundError
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
    'issues': 'Issue',
    'projects': 'Project',
    'notes': 'Note',
    'deals': 'Deal',
    'contacts': 'Contact',
    'related_contacts': 'Contact',
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
    'contact': 'Contact',
}

# Resources which when accessed from some other
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
    'contacts': 'Contact',
    'deals': 'Deal',
    'deal_categories': 'DealCategory',
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
    'status_id': 'status',
    'contact_id': 'contact',
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
    requirements = ()
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

    translations = {}

    _includes = ()
    _relations = ()
    _relations_name = None
    _unconvertible = ('name', 'description')
    _members = ('manager',)
    _create_readonly = ('id', 'created_on', 'updated_on', 'author', 'user', 'project', 'issue')
    _update_readonly = _create_readonly
    __length_hint__ = None  # fixes Python 2.6 list() call on resource object

    def __init__(self, manager, attributes):
        """Accepts manager instance object and resource attributes dict"""
        self.manager = manager
        self._attributes = dict((include, None) for include in self._includes)
        self._attributes.update(dict((relation, None) for relation in self._relations))
        self._attributes.update(attributes)
        self._create_readonly += self._relations + self._includes
        self._update_readonly += self._relations + self._includes
        self._changes = {}

        if self._relations_name is None:
            self._relations_name = self.__class__.__name__.lower()

    def __getitem__(self, item):
        """Provides a dictionary-like access to resource attributes"""
        return getattr(self, item)

    def __setitem__(self, item, value):
        """Provides a dictionary-like setter for resource attributes"""
        return setattr(self, item, value)

    def __getattr__(self, item):
        """Returns the requested attribute and makes a conversion if needed"""
        if item.startswith('_'):
            raise AttributeError

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
                filters = {'{0}_id'.format(self._relations_name): self.internal_id}
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
        elif item in self._create_readonly and self.is_new():
            raise ReadonlyAttrError
        elif item in self._update_readonly and not self.is_new():
            raise ReadonlyAttrError
        elif item == 'custom_fields':
            for org_index, org_field in enumerate(self._attributes.setdefault('custom_fields', [])):
                if 'value' not in org_field:
                    self._attributes['custom_fields'][org_index]['value'] = '0'

                try:
                    for new_index, new_field in enumerate(value):
                        if org_field['id'] == new_field['id']:
                            self._attributes['custom_fields'][org_index]['value'] = self.manager.prepare_params(
                                value.pop(new_index))['value']
                except (TypeError, KeyError):
                    raise CustomFieldValueError

            self._attributes['custom_fields'].extend(value)
            self._changes[item] = self._attributes['custom_fields']
        else:
            prep_item, prep_value = self.manager.prepare_params({item: value}).popitem()
            self._changes[prep_item] = prep_value
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
        """Checks if resource was just created and not yet saved to Redmine or it is an existing resource"""
        return False if 'id' in self._attributes or 'created_on' in self._attributes else True

    def _action_if_attribute_absent(self):
        """Whether we should raise an exception in case of attribute absence or just return None"""
        raise_attr_exception = self.manager.redmine.raise_attr_exception

        if isinstance(raise_attr_exception, bool) and raise_attr_exception:
            raise ResourceAttrError
        elif isinstance(raise_attr_exception, (list, tuple)) and self.__class__.__name__ in raise_attr_exception:
            raise ResourceAttrError

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

    _includes = ('trackers', 'issue_categories', 'enabled_modules')
    _relations = (
        'wiki_pages',
        'memberships',
        'issue_categories',
        'time_entries',
        'versions',
        'news',
        'issues',
        'contacts',
        'deals',
        'deal_categories',
    )
    _unconvertible = _Resource._unconvertible + ('identifier', 'status')
    _update_readonly = _Resource._update_readonly + ('identifier',)

    def __getattr__(self, item):
        if item == 'parent' and item in self._attributes:
            return ResourceManager(self.manager.redmine, 'Project').to_resource(self._attributes[item])

        value = super(Project, self).__getattr__(item)

        if item == 'enabled_modules':
            value = [module.get('name') if isinstance(module, dict) else module for module in value]

        return value


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

    translations = {'version_id': ('fixed_version_id', lambda x: x)}

    _includes = ('children', 'attachments', 'relations', 'changesets', 'journals', 'watchers')
    _relations = ('relations', 'time_entries')
    _unconvertible = _Resource._unconvertible + ('subject', 'notes')
    _create_readonly = _Resource._create_readonly + ('spent_hours',)
    _update_readonly = _create_readonly

    class Watcher:
        """An issue watcher implementation"""
        def __init__(self, issue):
            self._redmine = issue.manager.redmine
            self._issue_id = issue.internal_id

            if self._redmine.ver is not None and LooseVersion(str(self._redmine.ver)) < LooseVersion('2.3'):
                raise ResourceVersionMismatchError

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
            super(Issue, self).__setattr__('fixed_version_id', value)
        else:
            super(Issue, self).__setattr__(item, value)

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

    translations = {
        'from_date': ('from', lambda x: x),
        'to_date': ('to', lambda x: x),
    }

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

    def download(self, savepath=None, filename=None):
        return self.manager.redmine.download(self.content_url, savepath, filename)

    def __str__(self):
        try:
            return to_string(self.filename)
        except ResourceAttrError:
            return str(self.id)

    def __repr__(self):
        try:
            return '<{0}.{1} #{2} "{3}">'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id,
                to_string(self.filename)
            )
        except ResourceAttrError:
            return '<{0}.{1} #{2}>'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id
            )


class IssueJournal(_Resource):
    redmine_version = '1.0'
    _unconvertible = ('notes',)

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
    _unconvertible = _Resource._unconvertible + ('title', 'text')
    _create_readonly = _Resource._create_readonly + ('version',)
    _update_readonly = _create_readonly

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
        return to_string(self.title)

    def __getattr__(self, item):
        if item == 'parent' and item in self._attributes:
            manager = ResourceManager(self.manager.redmine, 'WikiPage')
            manager.params['project_id'] = self.manager.params.get('project_id', 0)
            return manager.to_resource(self._attributes[item])

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
        return self.internal_id

    def __repr__(self):
        return '<{0}.{1} "{2}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.internal_id
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

    _create_readonly = _Resource._create_readonly + ('user', 'roles')
    _update_readonly = _create_readonly

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
    _relations = ('issues', 'time_entries', 'contacts', 'deals')
    _relations_name = 'assigned_to'
    _unconvertible = ('status',)
    _create_readonly = _Resource._create_readonly + ('api_key', 'last_login_on')
    _update_readonly = _create_readonly

    def __getattr__(self, item):
        if item == 'time_entries':
            self._relations_name = 'user'
            value = super(User, self).__getattr__(item)
            self._relations_name = 'assigned_to'
            return value

        return super(User, self).__getattr__(item)

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

    _relations = ('issues',)
    _relations_name = 'status'

    @property
    def url(self):
        return '{0}/issue_statuses/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Tracker(_Resource):
    redmine_version = '1.3'
    container_all = 'trackers'
    query_all = '/trackers.json'

    _relations = ('issues',)

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
        if item == 'value' and item not in self._attributes:
            return 0

        # Redmine <2.5.2 returns only single tracker instead of a list of
        # all available trackers, see http://www.redmine.org/issues/16739
        # for details
        elif item == 'trackers' and 'tracker' in self._attributes[item]:
            self._attributes[item] = [self._attributes[item]['tracker']]

        return super(CustomField, self).__getattr__(item)


class Note(_Resource):
    redmine_version = '2.1'
    requirements = (('CRM plugin', '3.2.4'),)
    container_one = 'note'
    query_one = '/notes/{0}.json'

    def __getattr__(self, item):
        if item == 'source' and item in self._attributes and self._attributes[item].get('type') in ('Deal', 'Contact'):
            manager = ResourceManager(self.manager.redmine, self._attributes[item]['type'])
            return manager.to_resource(self._attributes[item])

        return super(Note, self).__getattr__(item)

    def __str__(self):
        return self.content

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Contact(_Resource):
    redmine_version = '1.2.1'
    requirements = ('CRM plugin',)
    container_all = 'contacts'
    container_one = 'contact'
    container_filter = 'contacts'
    container_create = 'contact'
    container_update = 'contact'
    query_all = '/contacts.json'
    query_one = '/contacts/{0}.json'
    query_filter = '/contacts.json'
    query_create = '/projects/{project_id}/contacts.json'
    query_update = '/contacts/{0}.json'
    query_delete = '/contacts/{0}.json'

    translations = {
        'tag_list': ('tag_list', lambda x: ','.join(x) if isinstance(x, (list, tuple)) else x),
        'phones': ('phone', lambda x: ','.join(x)),
        'emails': ('email', lambda x: ','.join(x)),
    }

    _includes = ('notes', 'contacts', 'deals', 'issues')
    _unconvertible = _Resource._unconvertible + ('company', 'skype_name')

    class Project:
        """A contact project implementation"""
        def __init__(self, contact):
            self._redmine = contact.manager.redmine
            self._contact_id = contact.internal_id

            if self._redmine.ver is not None and LooseVersion(str(self._redmine.ver)) < LooseVersion('2.3'):
                raise ResourceVersionMismatchError

        def add(self, project_id):
            """Adds project to contact's project list"""
            url = '{0}/contacts/{1}/projects.json'.format(self._redmine.url, self._contact_id)

            try:
                return self._redmine.request('post', url, data={'project': {'id': project_id}})
            except ResourceNotFoundError:
                raise ValidationError("Attempt to add contact to a project that doesn't exist")
            except ForbiddenError:
                raise ValidationError(
                    'Attempt to add contact to a project that either has contacts module disabled or is read-only')

        def remove(self, project_id):
            """Removes project from contact's project list"""
            url = '{0}/contacts/{1}/projects/{2}.json'.format(self._redmine.url, self._contact_id, project_id)

            try:
                return self._redmine.request('delete', url)
            except ResourceNotFoundError:
                raise ValidationError("Attempt to remove contact from a project that doesn't exist")
            except ForbiddenError:
                raise ValidationError(
                    'Attempt to remove contact from a project that either has contacts module disabled or is read-only')

    def __getattr__(self, item):
        if item == 'project':
            return Contact.Project(self)
        elif item == 'phones':
            return [p.get('number') if isinstance(p, dict) else p for p in self._attributes.get('phones', [])]
        elif item == 'emails':
            return [e.get('address') if isinstance(e, dict) else e for e in self._attributes.get('emails', [])]
        elif item == 'avatar' and item in self._attributes:
            manager = ResourceManager(self.manager.redmine, 'Attachment')
            return manager.to_resource({'id': self._attributes[item].get('attachment_id', 0)})

        return super(Contact, self).__getattr__(item)

    def __str__(self):
        try:
            return super(Contact, self).__str__()
        except ResourceAttrError:
            if not getattr(self, 'last_name', False):
                return '{0}'.format(to_string(self.first_name))
            else:
                return '{0} {1}'.format(to_string(self.first_name), to_string(self.last_name))

    def __repr__(self):
        try:
            return super(Contact, self).__repr__()
        except ResourceAttrError:
            if not getattr(self, 'last_name', False):
                return '<{0}.{1} #{2} "{3}">'.format(
                    self.__class__.__module__,
                    self.__class__.__name__,
                    self.id,
                    to_string(self.first_name),
                )
            else:
                return '<{0}.{1} #{2} "{3} {4}">'.format(
                    self.__class__.__module__,
                    self.__class__.__name__,
                    self.id,
                    to_string(self.first_name),
                    to_string(self.last_name)
                )


class ContactTag(_Resource):
    redmine_version = '2.3'
    requirements = (('CRM plugin', '3.4.0'),)
    container_all = 'tags'
    query_all = '/contacts_tags.json'

    @property
    def url(self):
        return '{0}/contacts_tags/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class CrmQuery(_Resource):
    redmine_version = '2.3'
    requirements = (('CRM plugin', '3.3.0'),)
    container_filter = 'queries'
    query_filter = '/crm_queries.json?object_type={resource}'

    _relations = ('deals',)
    _relations_name = 'query'

    @property
    def url(self):
        return '{0}/projects/{1}/{2}s?query_id={3}'.format(
            self.manager.redmine.url,
            self._attributes.get('project_id', 0),
            self.manager.params.get('resource', ''),
            self.internal_id
        )


class Deal(_Resource):
    redmine_version = '1.2.1'
    requirements = ('CRM plugin',)
    container_all = 'deals'
    container_one = 'deal'
    container_filter = 'deals'
    container_create = 'deal'
    container_update = 'deal'
    query_all = '/deals.json'
    query_one = '/deals/{0}.json'
    query_filter = '/deals.json'
    query_create = '/projects/{project_id}/deals.json'
    query_update = '/deals/{0}.json'
    query_delete = '/deals/{0}.json'

    _includes = ('notes',)

    def __getattr__(self, item):
        if item in ('category', 'status') and item in self._attributes:
            manager = ResourceManager(self.manager.redmine, 'Deal{0}'.format(item.capitalize()))
            return manager.to_resource(self._attributes[item])

        return super(Deal, self).__getattr__(item)

    def __str__(self):
        try:
            return super(Deal, self).__str__()
        except ResourceAttrError:
            return str(self.id)

    def __repr__(self):
        try:
            return super(Deal, self).__repr__()
        except ResourceAttrError:
            return '<{0}.{1} #{2}>'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id
            )


class DealStatus(_Resource):
    redmine_version = '2.3'
    requirements = (('CRM plugin', '3.3.0'),)
    container_all = 'deal_statuses'
    query_all = '/deal_statuses.json'

    _relations = ('deals',)
    _relations_name = 'status'

    @property
    def url(self):
        return '{0}/deal_statuses/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class DealCategory(_Resource):
    redmine_version = '2.3'
    requirements = (('CRM plugin', '3.3.0'),)
    container_filter = 'deal_categories'
    query_filter = '/projects/{project_id}/deal_categories.json'

    @property
    def url(self):
        return '{0}/deal_categories/edit?id={1}'.format(self.manager.redmine.url, self.internal_id)
