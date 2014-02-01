from datetime import datetime
from redmine.utilities import to_string
from redmine.managers import ResourceManager
from redmine.exceptions import ResourceAttrError, ReadonlyAttrError

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


class _Resource(object):
    """Implementation of Redmine resource"""
    manager = None
    attributes = {}

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

    _changes = {}
    _relations = {}
    _readonly = ('id', 'created_on', 'updated_on', 'author')
    __length_hint__ = None  # fixes Python 2.6 list() call on resource object

    def __init__(self, manager, attributes):
        """Accepts manager instance object and resource attributes dict"""
        self.manager = manager
        self.attributes = self._relations.copy()
        self.attributes.update(attributes)
        self._readonly += tuple(self._relations.keys())

    def __getitem__(self, item):
        """Provides a dictionary like access to resource attributes"""
        return getattr(self, item)

    def __setitem__(self, item, value):
        """Provides a dictionary like setter for resource attributes"""
        return setattr(self, item, value)

    def __getattr__(self, item):
        """Returns the requested attribute and makes a conversion if needed"""
        if item in self.attributes:
            # If item should be a Resource object, let's convert it
            if item in _RESOURCE_MAP:
                manager = ResourceManager(self.manager.redmine, _RESOURCE_MAP[item])
                return manager.to_resource(self.attributes[item])

            # If item should be a ResourceSet object, let's convert it
            elif item in _RESOURCE_SET_MAP and self.attributes[item] is not None:
                manager = ResourceManager(self.manager.redmine, _RESOURCE_SET_MAP[item])
                return manager.to_resource_set(self.attributes[item])

            # If item should be requested from Redmine, let's do it
            elif item in _RESOURCE_RELATIONS_MAP and self.attributes[item] is None:
                filters = {'{0}_id'.format(self.__class__.__name__.lower()): self.internal_id}
                manager = ResourceManager(self.manager.redmine, _RESOURCE_RELATIONS_MAP[item])
                self.attributes[item] = manager.filter(**filters)
                return self.attributes[item]

        try:
            # If the requested item is a date/datetime string
            # we need to convert it to the appropriate object
            possible_dt = str(self.attributes[item])

            try:
                return datetime.strptime(possible_dt, self.manager.redmine.datetime_format)
            except ValueError:
                return datetime.strptime(possible_dt, self.manager.redmine.date_format).date()
        except ValueError:
            return self.attributes[item]
        except KeyError:
            raise ResourceAttrError()

    def __setattr__(self, item, value):
        """Sets the requested attribute"""
        if item in self.__class__.__base__.__dict__:
            super(_Resource, self).__setattr__(item, value)
        elif item in self._readonly:
            raise ReadonlyAttrError()
        else:
            self._changes[item] = value
            self.attributes[item] = value

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
        if any(item in self.attributes and item not in self._relations for item in self._readonly):
            self.pre_update()
            self.manager.update(self.internal_id, **self._changes)
            self.attributes['updated_on'] = datetime.utcnow().strftime(self.manager.redmine.datetime_format)
            self.post_update()
        else:
            self.pre_create()
            for item, value in self.manager.create(**self._changes):
                self.attributes[item] = value
            self.post_create()

        self._changes = {}
        return True

    @classmethod
    def translate_params(cls, params):
        """Translates internal param names to the real Redmine param names if needed"""
        return params

    @property
    def url(self):
        """Returns full url to the resource for humans"""
        return self.manager.url.replace('.json', '')

    @property
    def internal_id(self):
        """Returns identifier of the resource for usage in internals of the library"""
        return self.id

    def __dir__(self):
        """We need to show only real Redmine resource attributes on dir() call"""
        return list(self.attributes.keys())

    def __iter__(self):
        """Provides a way to iterate through resource attributes and its values"""
        return iter(self.attributes.items())

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

    _relations = {
        'wiki_pages': None,
        'memberships': None,
        'issue_categories': None,
        'versions': None,
        'news': None,
        'issues': None,
    }
    _readonly = _Resource._readonly + ('identifier',)


class Issue(_Resource):
    redmine_version = '1.0'
    container_all = 'issues'
    container_one = 'issue'
    container_filter = 'issues'
    container_create = 'issue'
    query_all = '/issues.json'
    query_one = '/issues/{0}.json'
    query_filter = '/issues.json'
    query_create = '/projects/{project_id}/issues.json'
    query_delete = '/issues/{0}.json'

    _relations = {
        'relations': None,
        'time_entries': None,
    }

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
    query_all = '/time_entries.json'
    query_one = '/time_entries/{0}.json'
    query_filter = '/time_entries.json'
    query_create = '/time_entries.json'
    query_delete = '/time_entries/{0}.json'

    @classmethod
    def translate_params(cls, params):
        if 'from_date' in params:
            params['from'] = params.pop('from_date')

        if 'to_date' in params:
            params['to'] = params.pop('to_date')

        return params

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

    _readonly = _Resource._readonly + ('version',)

    def refresh(self):
        return super(WikiPage, self).refresh(project_id=self.manager.params.get('project_id', 0))

    def post_update(self):
        self.attributes['version'] = self.attributes.get('version', 0) + 1

    @property
    def internal_id(self):
        return self.title

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
    container_create = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{0}.json'
    query_create = '/projects/{project_id}/memberships.json'
    query_delete = '/memberships/{0}.json'

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
    container_create = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{0}.json'
    query_create = '/projects/{project_id}/issue_categories.json'
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
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{0}.json'
    query_create = '/projects/{project_id}/versions.json'
    query_delete = '/versions/{0}.json'

    def __getattr__(self, item):
        # We have to return status attribute as it is, otherwise it
        # will be automatically converted to IssueStatus resource
        # by the parent _Resource object which is not what we want
        if item == 'status':
            try:
                return self.attributes[item]
            except KeyError:
                raise ResourceAttrError()

        return super(Version, self).__getattr__(item)


class User(_Resource):
    redmine_version = '1.1'
    container_all = 'users'
    container_one = 'user'
    container_filter = 'users'
    container_create = 'user'
    query_all = '/users.json'
    query_one = '/users/{0}.json'
    query_filter = '/users.json'
    query_create = '/users.json'
    query_delete = '/users/{0}.json'

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
    query_all = '/groups.json'
    query_one = '/groups/{0}.json'
    query_create = '/groups.json'
    query_delete = '/groups/{0}.json'


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


class IssueStatus(_Resource):
    redmine_version = '1.3'
    container_all = 'issue_statuses'
    query_all = '/issue_statuses.json'


class Tracker(_Resource):
    redmine_version = '1.3'
    container_all = 'trackers'
    query_all = '/trackers.json'


class Query(_Resource):
    redmine_version = '1.3'
    container_all = 'queries'
    query_all = '/queries.json'


class CustomField(_Resource):
    redmine_version = '2.4'
    container_all = 'custom_fields'
    query_all = '/custom_fields.json'

    def __getattr__(self, item):
        # If custom field was created after the creation of the resource,
        # i.e. project, and it's not used in the resource, there will be
        # no value attribute defined, that is why we need to return 0 or
        # we'll get an exception
        if item == 'value' and not item in self.attributes:
            return 0

        return super(CustomField, self).__getattr__(item)
