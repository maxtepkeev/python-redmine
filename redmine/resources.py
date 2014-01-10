import sys
from datetime import datetime
from redmine.managers import ResourceManager
from redmine.exceptions import ResourceAttrError

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
    version = None
    container_all = None
    container_one = None
    container_filter = None
    query_all = None
    query_one = None
    query_filter = None

    _relations = {}
    __length_hint__ = None  # fixes Python 2.6 list() call on resource object

    def __init__(self, manager, attributes):
        """Accepts manager instance object and resource attributes dict"""
        self.manager = manager
        self.attributes = self._relations.copy()
        self.attributes.update(attributes)

    def __getitem__(self, item):
        """Provides a dictionary like access to resource attributes"""
        return getattr(self, item)

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
                filters = {'{0}_id'.format(self.__class__.__name__.lower()): self.id}
                manager = ResourceManager(self.manager.redmine, _RESOURCE_RELATIONS_MAP[item])
                return manager.filter(**filters)

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

    def refresh(self, **params):
        """Reloads resource data from Redmine"""
        return self.manager.get(self.id, **params)

    @property
    def url(self):
        """Returns full url to the resource for humans"""
        return self.manager.url.replace('.json', '')

    def __dir__(self):
        """We need to show only real Redmine resource attributes on dir() call"""
        return list(self.attributes.keys())

    def __iter__(self):
        """Provides a way to iterate through resource attributes and its values"""
        return iter(self.attributes.items())

    def __repr__(self):
        """Official representation of the Redmine resource"""
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            self.name.encode('utf-8') if sys.version_info[0] < 3 else self.name
        )


class Project(_Resource):
    version = '1.0'
    container_all = 'projects'
    container_one = 'project'
    query_all = '/projects.json'
    query_one = '/projects/{0}.json'

    _relations = {
        'wiki_pages': None,
        'memberships': None,
        'issue_categories': None,
        'versions': None,
        'news': None,
        'issues': None,
    }


class Issue(_Resource):
    version = '1.0'
    container_all = 'issues'
    container_one = 'issue'
    container_filter = 'issues'
    query_all = '/issues.json'
    query_one = '/issues/{0}.json'
    query_filter = '/issues.json'

    _relations = {
        'relations': None,
        'time_entries': None,
    }

    def __repr__(self):
        try:
            return '<{0}.{1} #{2} "{3}">'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id,
                self.subject.encode('utf-8') if sys.version_info[0] < 3 else self.subject
            )
        except ResourceAttrError:
            return '<{0}.{1} #{2}>'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id
            )


class TimeEntry(_Resource):
    version = '1.1'
    container_all = 'time_entries'
    container_one = 'time_entry'
    container_filter = 'time_entries'
    query_all = '/time_entries.json'
    query_one = '/time_entries/{0}.json'
    query_filter = '/issues/{issue_id}/time_entries.json'

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Enumeration(_Resource):
    version = '2.2'
    container_filter = '{resource}'
    query_filter = '/enumerations/{resource}.json'


class Attachment(_Resource):
    version = '1.3'
    container_one = 'attachment'
    query_one = '/attachments/{0}.json'

    def __repr__(self):
        return '<{0}.{1} #{2} "{3}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id,
            self.filename.encode('utf-8') if sys.version_info[0] < 3 else self.filename
        )


class IssueJournal(_Resource):
    version = '1.0'

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class WikiPage(_Resource):
    version = '2.2'
    container_filter = 'wiki_pages'
    container_one = 'wiki_page'
    query_filter = '/projects/{project_id}/wiki/index.json'
    query_one = '/projects/{project_id}/wiki/{0}.json'

    def refresh(self):
        return self.manager.get(self.title, **{'project_id': self.manager.params['project_id']})

    def __repr__(self):
        return '<{0}.{1} "{2}">'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.title.encode('utf-8') if sys.version_info[0] < 3 else self.title
        )


class ProjectMembership(_Resource):
    version = '1.4'
    container_filter = 'memberships'
    container_one = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{0}.json'

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class IssueCategory(_Resource):
    version = '1.3'
    container_filter = 'issue_categories'
    container_one = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{0}.json'


class IssueRelation(_Resource):
    version = '1.3'
    container_filter = 'relations'
    container_one = 'relation'
    query_filter = '/issues/{issue_id}/relations.json'
    query_one = '/relations/{0}.json'

    def __repr__(self):
        return '<{0}.{1} #{2}>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.id
        )


class Version(_Resource):
    version = '1.3'
    container_filter = 'versions'
    container_one = 'version'
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{0}.json'


class User(_Resource):
    version = '1.1'
    container_all = 'users'
    container_one = 'user'
    container_filter = 'users'
    query_all = '/users.json'
    query_one = '/users/{0}.json'
    query_filter = '/users.json'

    def __repr__(self):
        try:
            return super(User, self).__repr__()
        except ResourceAttrError:
            return '<{0}.{1} #{2} "{3} {4}">'.format(
                self.__class__.__module__,
                self.__class__.__name__,
                self.id,
                self.firstname.encode('utf-8') if sys.version_info[0] < 3 else self.firstname,
                self.lastname.encode('utf-8') if sys.version_info[0] < 3 else self.lastname
            )


class Group(_Resource):
    version = '2.1'
    container_all = 'groups'
    container_one = 'group'
    query_all = '/groups.json'
    query_one = '/groups/{0}.json'


class Role(_Resource):
    version = '1.4'
    container_all = 'roles'
    container_one = 'role'
    query_all = '/roles.json'
    query_one = '/roles/{0}.json'


class News(_Resource):
    version = '1.1'
    container_all = 'news'
    container_filter = 'news'
    query_all = '/news.json'
    query_filter = '/projects/{project_id}/news.json'


class IssueStatus(_Resource):
    version = '1.3'
    container_all = 'issue_statuses'
    query_all = '/issue_statuses.json'


class Tracker(_Resource):
    version = '1.3'
    container_all = 'trackers'
    query_all = '/trackers.json'


class Query(_Resource):
    version = '1.3'
    container_all = 'queries'
    query_all = '/queries.json'


class CustomField(_Resource):
    version = '2.4'
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
