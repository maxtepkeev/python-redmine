from datetime import date, datetime

from distutils.version import LooseVersion

from .utilities import to_string
from .managers import ResourceManager
from .exceptions import (
    ResourceAttrError,
    ReadonlyAttrError,
    CustomFieldValueError,
    ResourceVersionMismatchError,
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

# Resources which when accessed from some other
# resource should be requested from Redmine
_RELATIONS_MAP = {
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
_SINGLE_ATTR_ID_MAP = {
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
_MULTIPLE_ATTR_ID_MAP = {
    'user_ids': 'users',
    'role_ids': 'roles',
}


class Resource(object):
    """
    Implementation of Redmine resource.
    """
    redmine_version = None
    requirements = ()
    container_many = None
    container_one = None
    query_all = None
    query_one = None
    query_filter = None
    query_create = None
    query_update = None
    query_delete = None

    _includes = ()
    _relations = ()
    _relations_name = None
    _unconvertible = ('name', 'description')
    _members = ('manager',)
    _create_readonly = ('id', 'created_on', 'updated_on', 'author', 'user', 'project', 'issue')
    _update_readonly = _create_readonly
    __length_hint__ = None  # fixes Python 2.6 list() call on resource object

    def __init__(self, manager, attributes):
        """
        :param managers.ResourceManager manager: (required). Manager instance object.
        :param dict attributes: (required). Resource attributes.
        """
        relations_includes = self._relations + self._includes

        self.manager = manager
        self._create_readonly += relations_includes
        self._update_readonly += relations_includes
        self._attributes = self.bulk_encode(attributes)
        self._changes = {}

        if self._relations_name is None:
            self._relations_name = self.__class__.__name__.lower()

    def __getitem__(self, item):
        """
        Provides a dictionary-like access to Resource attributes.
        """
        return getattr(self, item)

    def __setitem__(self, item, value):
        """
        Provides a dictionary-like setter for Resource attributes.
        """
        return setattr(self, item, value)

    def __getattr__(self, attr):
        """
        Returns the requested attribute and makes a conversion if needed.
        """
        if attr.startswith('_'):
            raise AttributeError

        try:
            return self._attributes[attr]
        except KeyError:
            if attr in self._relations:
                manager = ResourceManager(self.manager.redmine, _RELATIONS_MAP[attr])
                self._attributes[attr] = manager.filter(**{'{0}_id'.format(self._relations_name): self.internal_id})
                return self._attributes[attr]
            elif attr in self._includes:
                self._attributes[attr] = getattr(self.refresh(include=attr), attr)
                return self._attributes[attr]

            if self.is_new():
                if attr in ('id', 'version'):
                    return 0
                return ''

            raise_attr_exception = self.manager.redmine.raise_attr_exception

            if isinstance(raise_attr_exception, bool) and raise_attr_exception:
                raise ResourceAttrError
            elif isinstance(raise_attr_exception, (list, tuple)) and self.__class__.__name__ in raise_attr_exception:
                raise ResourceAttrError

            return None

    def __setattr__(self, attr, value):
        """
        Sets the requested attribute.
        """
        if attr in self._members or attr.startswith('_'):
            super(Resource, self).__setattr__(attr, value)
        elif attr in self._create_readonly and self.is_new():
            raise ReadonlyAttrError
        elif attr in self._update_readonly and not self.is_new():
            raise ReadonlyAttrError
        elif attr == 'custom_fields':
            for org_index, org_field in enumerate(self._attributes.setdefault('custom_fields', [])):
                if 'value' not in org_field:
                    self._attributes['custom_fields'][org_index]['value'] = '0'

                try:
                    for new_index, new_field in enumerate(value):
                        if org_field['id'] == new_field['id']:
                            self._attributes['custom_fields'][org_index]['value'] = self.bulk_decode(
                                value.pop(new_index))['value']
                except (TypeError, KeyError):
                    raise CustomFieldValueError

            self._attributes['custom_fields'].extend(value)
            self._changes[attr] = self._attributes['custom_fields']
        else:
            self._changes.update(self.bulk_decode({attr: value}))

            if attr in _SINGLE_ATTR_ID_MAP:
                self._attributes.update(self.bulk_encode({_SINGLE_ATTR_ID_MAP[attr]: {'id': value}}))
            elif attr in _MULTIPLE_ATTR_ID_MAP:
                self._attributes.update(self.bulk_encode({_MULTIPLE_ATTR_ID_MAP[attr]: [{'id': mid} for mid in value]}))
            else:
                self._attributes[attr] = value

    def decode(self, attr, value):
        """
        Decodes a single attr, value pair from Python representation to the needed Redmine representation.

        :param str attr: (required). Attribute name.
        :param any value: (required). Attribute value.
        """
        type_ = type(value)

        if type_ is date:
            return attr, value.strftime(self.manager.redmine.date_format)
        elif type_ is datetime:
            return attr, value.strftime(self.manager.redmine.datetime_format)

        return attr, value

    def encode(self, attr, value):
        """
        Encodes a single attr, value pair retrieved from Redmine to the needed Python representation.

        :param str attr: (required). Attribute name.
        :param any value: (required). Attribute value.
        """
        if attr in self._unconvertible:
            return attr, value
        elif attr in _RESOURCE_MAP:
            return attr, ResourceManager(self.manager.redmine, _RESOURCE_MAP[attr]).to_resource(value)
        elif attr in _RESOURCE_SET_MAP:
            return attr, ResourceManager(self.manager.redmine, _RESOURCE_SET_MAP[attr]).to_resource_set(value)
        elif attr == 'parent':
            return attr, ResourceManager(self.manager.redmine, self.__class__.__name__).to_resource(value)

        try:
            try:
                return attr, datetime.strptime(value, self.manager.redmine.datetime_format)
            except (TypeError, ValueError):
                return attr, datetime.strptime(value, self.manager.redmine.date_format).date()
        except (TypeError, ValueError):
            return attr, value

    def bulk_decode(self, attrs):
        """
        Decodes resource data from Python representation to the needed Redmine representation.

        :param dict attrs: (required). Attributes in the form of key, value pairs.
        """
        return dict(self.decode(attr, attrs[attr]) for attr in attrs)

    def bulk_encode(self, attrs):
        """
        Encodes resource data retrieved from Redmine to the needed Python representation.

        :param dict attrs: (required). Attributes in the form of key, value pairs.
        """
        return dict(self.encode(attr, attrs[attr]) for attr in attrs)

    def refresh(self, **params):
        """
        Reloads resource data from Redmine.

        :param dict params: (optional). Parameters used for resource retrieval.
        """
        return self.manager.get(self.internal_id, **params)

    def pre_create(self):
        """
        Tasks that should be done before creating the Resource.
        """
        pass

    def post_create(self):
        """
        Tasks that should be done after creating the Resource.
        """
        pass

    def pre_update(self):
        """
        Tasks that should be done before updating the Resource.
        """
        pass

    def post_update(self):
        """
        Tasks that should be done after updating the Resource.
        """
        pass

    def save(self):
        """
        Creates or updates a Resource.
        """
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
        """
        Returns full URL to the Resource for humans if there is one.
        """
        if self.query_one is not None:
            return self.manager.redmine.url + self.query_one.format(self.internal_id).replace('.json', '')
        else:
            return None

    @property
    def internal_id(self):
        """
        Returns identifier of the Resource for usage in internals of the library.
        """
        return self.id

    def is_new(self):
        """
        Checks if Resource was just created and not yet saved to Redmine or it is an existing Resource.
        """
        return False if 'id' in self._attributes or 'created_on' in self._attributes else True

    def __dir__(self):
        """
        Allows dir() to be called on a Resource object and shows Resource attributes.
        """
        return list(self._attributes.keys())

    def __iter__(self):
        """
        Provides a way to iterate through Resource attributes and its values.
        """
        return iter(self._attributes.items())

    def __int__(self):
        """
        Integer representation of a Resource object.
        """
        return self.id

    def __str__(self):
        """
        Informal representation of a Resource object.
        """
        return to_string(self.name)

    def __repr__(self):
        """
        Official representation of a Resource object.
        """
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            to_string(self.name)
        )


class Project(Resource):
    redmine_version = '1.0'
    container_many = 'projects'
    container_one = 'project'
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
    )
    _unconvertible = Resource._unconvertible + ('identifier', 'status')
    _update_readonly = Resource._update_readonly + ('identifier',)

    def encode(self, attr, value):
        if attr == 'enabled_modules':
            return attr, [module['name'] for module in value]

        return super(Project, self).encode(attr, value)


class Issue(Resource):
    redmine_version = '1.0'
    container_many = 'issues'
    container_one = 'issue'
    query_all = '/issues.json'
    query_one = '/issues/{0}.json'
    query_filter = '/issues.json'
    query_create = '/projects/{project_id}/issues.json'
    query_update = '/issues/{0}.json'
    query_delete = '/issues/{0}.json'

    _includes = ('children', 'attachments', 'relations', 'changesets', 'journals', 'watchers')
    _relations = ('relations', 'time_entries')
    _unconvertible = Resource._unconvertible + ('subject', 'notes')
    _create_readonly = Resource._create_readonly + ('spent_hours',)
    _update_readonly = _create_readonly

    class Watcher:
        """
        An issue watcher implementation.
        """
        def __init__(self, issue):
            self._redmine = issue.manager.redmine
            self._issue_id = issue.internal_id

            if self._redmine.ver is not None and LooseVersion(str(self._redmine.ver)) < LooseVersion('2.3'):
                raise ResourceVersionMismatchError

        def add(self, user_id):
            """
            Adds user to issue watchers list.

            :param int user_id: (required). User id.
            """
            url = '{0}/issues/{1}/watchers.json'.format(self._redmine.url, self._issue_id)
            return self._redmine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from issue watchers list.

            :param int user_id: (required). User id.
            """
            url = '{0}/issues/{1}/watchers/{2}.json'.format(self._redmine.url, self._issue_id, user_id)
            return self._redmine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'version':
            return super(Issue, self).__getattr__('fixed_version')
        elif attr == 'watcher':
            return Issue.Watcher(self)

        return super(Issue, self).__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr == 'version_id':
            super(Issue, self).__setattr__('fixed_version_id', value)
        else:
            super(Issue, self).__setattr__(attr, value)

    def decode(self, attr, value):
        if attr == 'version_id':
            return 'fixed_version_id', value

        return super(Issue, self).decode(attr, value)

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


class TimeEntry(Resource):
    redmine_version = '1.1'
    container_many = 'time_entries'
    container_one = 'time_entry'
    query_all = '/time_entries.json'
    query_one = '/time_entries/{0}.json'
    query_filter = '/time_entries.json'
    query_create = '/time_entries.json'
    query_update = '/time_entries/{0}.json'
    query_delete = '/time_entries/{0}.json'

    def decode(self, attr, value):
        if attr == 'from_date':
            attr = 'from'
        elif attr == 'to_date':
            attr = 'to'

        return super(TimeEntry, self).decode(attr, value)

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Enumeration(Resource):
    redmine_version = '2.2'
    container_many = '{resource}'
    query_filter = '/enumerations/{resource}.json'

    @property
    def url(self):
        return '{0}/enumerations/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Attachment(Resource):
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


class IssueJournal(Resource):
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


class WikiPage(Resource):
    redmine_version = '2.2'
    container_many = 'wiki_pages'
    container_one = 'wiki_page'
    query_filter = '/projects/{project_id}/wiki/index.json'
    query_one = '/projects/{project_id}/wiki/{0}.json'
    query_create = '/projects/{project_id}/wiki/{title}.json'
    query_update = '/projects/{project_id}/wiki/{0}.json'
    query_delete = '/projects/{project_id}/wiki/{0}.json'

    _includes = ('attachments',)
    _unconvertible = Resource._unconvertible + ('title', 'text')
    _create_readonly = Resource._create_readonly + ('version',)
    _update_readonly = _create_readonly

    def encode(self, attr, value):
        if attr == 'parent':
            manager = ResourceManager(self.manager.redmine, self.__class__.__name__)
            manager.params['project_id'] = self.manager.params.get('project_id', 0)
            return attr, manager.to_resource(value)

        return super(WikiPage, self).encode(attr, value)

    def refresh(self, **params):
        return super(WikiPage, self).refresh(**dict(params, project_id=self.manager.params.get('project_id', 0)))

    def post_update(self):
        self._attributes['version'] = self._attributes.get('version', 0) + 1

    @property
    def url(self):
        return self.manager.redmine.url + self.query_one.format(
                self.internal_id,
                project_id=self.manager.params.get('project_id', 0)
        ).replace('.json', '')

    @property
    def internal_id(self):
        return to_string(self.title)

    def __getattr__(self, attr):
        # If a text attribute of a resource is missing, we should
        # refresh a resource automatically for user's convenience
        if attr == 'text' and attr not in self._attributes:
            self._attributes[attr] = getattr(self.refresh(), attr)

        return super(WikiPage, self).__getattr__(attr)

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


class ProjectMembership(Resource):
    redmine_version = '1.4'
    container_many = 'memberships'
    container_one = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{0}.json'
    query_create = '/projects/{project_id}/memberships.json'
    query_update = '/memberships/{0}.json'
    query_delete = '/memberships/{0}.json'

    _create_readonly = Resource._create_readonly + ('user', 'roles')
    _update_readonly = _create_readonly

    def __str__(self):
        return str(self.id)

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class IssueCategory(Resource):
    redmine_version = '1.3'
    container_many = 'issue_categories'
    container_one = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{0}.json'
    query_create = '/projects/{project_id}/issue_categories.json'
    query_update = '/issue_categories/{0}.json'
    query_delete = '/issue_categories/{0}.json'


class IssueRelation(Resource):
    redmine_version = '1.3'
    container_many = 'relations'
    container_one = 'relation'
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


class Version(Resource):
    redmine_version = '1.3'
    container_many = 'versions'
    container_one = 'version'
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{0}.json'
    query_create = '/projects/{project_id}/versions.json'
    query_update = '/versions/{0}.json'
    query_delete = '/versions/{0}.json'

    _unconvertible = ('status',)


class User(Resource):
    redmine_version = '1.1'
    container_many = 'users'
    container_one = 'user'
    query_all = '/users.json'
    query_one = '/users/{0}.json'
    query_filter = '/users.json'
    query_create = '/users.json'
    query_update = '/users/{0}.json'
    query_delete = '/users/{0}.json'

    _includes = ('memberships', 'groups')
    _relations = ('issues', 'time_entries')
    _relations_name = 'assigned_to'
    _unconvertible = ('status',)
    _create_readonly = Resource._create_readonly + ('api_key', 'last_login_on')
    _update_readonly = _create_readonly

    def __getattr__(self, attr):
        if attr == 'time_entries' and attr not in self._attributes:
            self._relations_name = 'user'
            value = super(User, self).__getattr__(attr)
            self._relations_name = 'assigned_to'
            return value

        return super(User, self).__getattr__(attr)

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


class Group(Resource):
    redmine_version = '2.1'
    container_many = 'groups'
    container_one = 'group'
    query_all = '/groups.json'
    query_one = '/groups/{0}.json'
    query_create = '/groups.json'
    query_update = '/groups/{0}.json'
    query_delete = '/groups/{0}.json'

    _includes = ('memberships', 'users')

    class User:
        """
        A group user implementation.
        """
        def __init__(self, group):
            self._redmine = group.manager.redmine
            self._group_id = group.internal_id

        def add(self, user_id):
            """
            Adds user to a group.

            :param int user_id: (required). User id.
            """
            url = '{0}/groups/{1}/users.json'.format(self._redmine.url, self._group_id)
            return self._redmine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from a group.

            :param int user_id: (required). User id.
            """
            url = '{0}/groups/{1}/users/{2}.json'.format(self._redmine.url, self._group_id, user_id)
            return self._redmine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'user':
            return Group.User(self)

        return super(Group, self).__getattr__(attr)


class Role(Resource):
    redmine_version = '1.4'
    container_many = 'roles'
    container_one = 'role'
    query_all = '/roles.json'
    query_one = '/roles/{0}.json'


class News(Resource):
    redmine_version = '1.1'
    container_many = 'news'
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


class IssueStatus(Resource):
    redmine_version = '1.3'
    container_many = 'issue_statuses'
    query_all = '/issue_statuses.json'

    _relations = ('issues',)
    _relations_name = 'status'

    @property
    def url(self):
        return '{0}/issue_statuses/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Tracker(Resource):
    redmine_version = '1.3'
    container_many = 'trackers'
    query_all = '/trackers.json'

    _relations = ('issues',)

    @property
    def url(self):
        return '{0}/trackers/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Query(Resource):
    redmine_version = '1.3'
    container_many = 'queries'
    query_all = '/queries.json'

    @property
    def url(self):
        return '{0}/projects/{1}/issues?query_id={2}'.format(
            self.manager.redmine.url,
            self._attributes.get('project_id', 0),
            self.internal_id
        )


class CustomField(Resource):
    redmine_version = '2.4'
    container_many = 'custom_fields'
    query_all = '/custom_fields.json'

    def __getattr__(self, attr):
        # If custom field was created after the creation of the resource,
        # i.e. project, and it's not used in the resource, there will be
        # no value attribute defined, that is why we need to return 0 or
        # we'll get an exception
        if attr == 'value' and attr not in self._attributes:
            return 0

        return super(CustomField, self).__getattr__(attr)

    def encode(self, attr, value):
        # Redmine <2.5.2 returns only single tracker instead of a list of
        # all available trackers, see http://www.redmine.org/issues/16739
        # for details
        if attr == 'trackers' and 'tracker' in value:
            value = [value['tracker']]

        return super(CustomField, self).encode(attr, value)

    @property
    def url(self):
        return '{0}/custom_fields/{1}/edit'.format(self.manager.redmine.url, self.internal_id)
