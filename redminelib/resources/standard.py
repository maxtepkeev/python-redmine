"""
Defines standard Redmine resources and resource mappings.
"""

from __future__ import unicode_literals

from distutils.version import LooseVersion

from . import BaseResource
from .. import exceptions


class Project(BaseResource):
    redmine_version = '1.0'
    container_many = 'projects'
    container_one = 'project'
    query_all_export = '/projects.{format}'
    query_all = '/projects.json'
    query_one = '/projects/{0}.json'
    query_create = '/projects.json'
    query_update = '/projects/{0}.json'
    query_delete = '/projects/{0}.json'
    search_hints = ['project']

    _repr = [['id', 'name'], ['title']]
    _includes = ['trackers', 'issue_categories', 'enabled_modules']
    _relations = ['wiki_pages', 'memberships', 'issue_categories', 'time_entries', 'versions', 'news', 'issues']
    _unconvertible = BaseResource._unconvertible + ['identifier', 'status']
    _update_readonly = BaseResource._update_readonly + ['identifier']
    _resource_set_map = {
        'custom_fields': 'CustomField',
        'trackers': 'Tracker',
        'issue_categories': 'IssueCategory',
        'wiki_pages': 'WikiPage',
        'memberships': 'ProjectMembership',
        'time_entries': 'TimeEntry',
        'versions': 'Version',
        'news': 'News',
        'issues': 'Issue',
    }
    _single_attr_id_map = {'parent_id': 'parent'}
    _multiple_attr_id_map = {'tracker_ids': 'trackers'}

    @property
    def url(self):
        return self.manager.redmine.url + self.query_one.format(self.identifier)[:-5]

    @classmethod
    def encode(cls, attr, value, manager):
        if attr == 'enabled_modules':
            return attr, [module['name'] for module in value]

        return super(Project, cls).encode(attr, value, manager)


class Issue(BaseResource):
    redmine_version = '1.0'
    container_many = 'issues'
    container_one = 'issue'
    query_all_export = '/issues.{format}'
    query_one_export = '/issues/{0}.{format}'
    query_all = '/issues.json'
    query_one = '/issues/{0}.json'
    query_filter = '/issues.json'
    query_create = '/projects/{project_id}/issues.json'
    query_update = '/issues/{0}.json'
    query_delete = '/issues/{0}.json'
    search_hints = ['issue', 'issue closed']

    _repr = [['id', 'subject'], ['title'], ['id']]
    _includes = ['children', 'attachments', 'relations', 'changesets', 'journals', 'watchers']
    _relations = ['relations', 'time_entries']
    _unconvertible = BaseResource._unconvertible + ['subject', 'notes']
    _create_readonly = BaseResource._create_readonly + ['spent_hours']
    _update_readonly = _create_readonly[:]
    _resource_map = {
        'project': 'Project',
        'tracker': 'Tracker',
        'status': 'IssueStatus',
        'priority': 'Enumeration',
        'author': 'User',
        'assigned_to': 'User',
        'category': 'IssueCategory',
        'fixed_version': 'Version',
    }
    _resource_set_map = {
        'custom_fields': 'CustomField',
        'attachments': 'Attachment',
        'journals': 'IssueJournal',
        'children': 'Issue',
        'relations': 'IssueRelation',
        'watchers': 'User',
        'time_entries': 'TimeEntry',
    }
    _single_attr_id_map = {
        'project_id': 'project',
        'tracker_id': 'tracker',
        'status_id': 'status',
        'priority_id': 'priority',
        'category_id': 'category',
        'fixed_version_id': 'fixed_version',
        'assigned_to_id': 'assigned_to',
        'parent_issue_id': 'parent',
    }
    _multiple_attr_id_map = {'watcher_user_ids': 'watchers'}

    class Watcher:
        """
        An issue watcher implementation.
        """
        def __init__(self, issue):
            self._redmine = issue.manager.redmine
            self._issue_id = issue.internal_id

            if self._redmine.ver is not None and LooseVersion(str(self._redmine.ver)) < LooseVersion('2.3'):
                raise exceptions.ResourceVersionMismatchError

        def add(self, user_id):
            """
            Adds user to issue watchers list.

            :param int user_id: (required). User id.
            """
            url = '{0}/issues/{1}/watchers.json'.format(self._redmine.url, self._issue_id)
            return self._redmine.engine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from issue watchers list.

            :param int user_id: (required). User id.
            """
            url = '{0}/issues/{1}/watchers/{2}.json'.format(self._redmine.url, self._issue_id, user_id)
            return self._redmine.engine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'watcher':
            return Issue.Watcher(self)

        if attr == 'version':
            attr = 'fixed_version'

        return super(Issue, self).__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr == 'version_id':
            attr = 'fixed_version_id'

        super(Issue, self).__setattr__(attr, value)

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'version_id':
            return 'fixed_version_id', value

        if attr == 'checklists':
            return 'checklists_attributes', value

        return super(Issue, cls).decode(attr, value, manager)


class TimeEntry(BaseResource):
    redmine_version = '1.1'
    container_many = 'time_entries'
    container_one = 'time_entry'
    query_all_export = '/time_entries.{format}'
    query_all = '/time_entries.json'
    query_one = '/time_entries/{0}.json'
    query_filter = '/time_entries.json'
    query_create = '/time_entries.json'
    query_update = '/time_entries/{0}.json'
    query_delete = '/time_entries/{0}.json'

    _repr = [['id']]
    _resource_map = {'project': 'Project', 'issue': 'Issue', 'user': 'User', 'activity': 'Enumeration'}
    _resource_set_map = {'custom_fields': 'CustomField'}
    _single_attr_id_map = {'issue_id': 'issue', 'activity_id': 'activity'}

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'from_date':
            attr = 'from'
        elif attr == 'to_date':
            attr = 'to'

        return super(TimeEntry, cls).decode(attr, value, manager)


class Enumeration(BaseResource):
    redmine_version = '2.2'
    container_many = '{resource}'
    query_filter = '/enumerations/{resource}.json'

    @property
    def url(self):
        return '{0}/enumerations/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Attachment(BaseResource):
    redmine_version = '1.3'
    container_one = 'attachment'
    query_one = '/attachments/{0}.json'
    query_delete = '/attachments/{0}.json'

    _repr = [['id', 'filename'], ['id']]
    _resource_map = {'author': 'User'}

    def download(self, savepath=None, filename=None):
        return self.manager.redmine.download(self.content_url, savepath, filename)


class IssueJournal(BaseResource):
    redmine_version = '1.0'

    _repr = [['id']]
    _unconvertible = ['notes']
    _resource_map = {'user': 'User'}


class WikiPage(BaseResource):
    internal_id_key = 'title'
    redmine_version = '2.2'
    container_many = 'wiki_pages'
    container_one = 'wiki_page'
    query_one_export = '/projects/{project_id}/wiki/{0}.{format}'
    query_filter = '/projects/{project_id}/wiki/index.json'
    query_one = '/projects/{project_id}/wiki/{0}.json'
    query_create = '/projects/{project_id}/wiki/{title}.json'
    query_update = '/projects/{project_id}/wiki/{0}.json'
    query_delete = '/projects/{project_id}/wiki/{0}.json'
    search_hints = ['wiki-page']
    http_method_create = 'put'

    _repr = [['title']]
    _includes = ['attachments']
    _unconvertible = BaseResource._unconvertible + ['title', 'text']
    _create_readonly = BaseResource._create_readonly + ['version']
    _update_readonly = _create_readonly[:]
    _resource_map = {'author': 'User'}
    _resource_set_map = {'attachments': 'Attachment'}
    _single_attr_id_map = {'project_id': 'project'}

    @classmethod
    def encode(cls, attr, value, manager):
        if attr == 'parent':
            value = manager.new_manager(cls.__name__, project_id=manager.params.get('project_id', 0)).to_resource(value)
            return attr, value

        return super(WikiPage, cls).encode(attr, value, manager)

    def refresh(self, **params):
        return super(WikiPage, self).refresh(**dict(params, project_id=self.project_id))

    def post_update(self):
        self._encoded_attrs['version'] = self._decoded_attrs['version'] = self._decoded_attrs.get('version', 0) + 1

    def delete(self, **params):
        return super(WikiPage, self).delete(**dict(params, project_id=self.project_id))

    def export_url(self, fmt):
        return self.manager.redmine.url + self.query_one_export.format(
            self.internal_id, project_id=self.project_id, format=fmt)

    @property
    def project_id(self):
        return self.manager.params.get('project_id', 0)

    @property
    def url(self):
        return self.manager.redmine.url + self.query_one.format(self.internal_id, project_id=self.project_id)[:-5]

    def __getattr__(self, attr):
        # If a text attribute of a resource is missing, we should
        # refresh a resource automatically for user's convenience
        if attr == 'text' and attr not in self._decoded_attrs:
            self._decoded_attrs[attr] = self.refresh(itself=False).raw()[attr]

        return super(WikiPage, self).__getattr__(attr)

    def __int__(self):
        return self.version


class ProjectMembership(BaseResource):
    redmine_version = '1.4'
    container_many = 'memberships'
    container_one = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{0}.json'
    query_create = '/projects/{project_id}/memberships.json'
    query_update = '/memberships/{0}.json'
    query_delete = '/memberships/{0}.json'

    _repr = [['id']]
    _create_readonly = BaseResource._create_readonly + ['user', 'roles']
    _update_readonly = _create_readonly[:]
    _resource_map = {'project': 'Project', 'user': 'User'}
    _resource_set_map = {'roles': 'Role'}
    _single_attr_id_map = {'project_id': 'project', 'user_id': 'users'}
    _multiple_attr_id_map = {'role_ids': 'roles'}


class IssueCategory(BaseResource):
    redmine_version = '1.3'
    container_many = 'issue_categories'
    container_one = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{0}.json'
    query_create = '/projects/{project_id}/issue_categories.json'
    query_update = '/issue_categories/{0}.json'
    query_delete = '/issue_categories/{0}.json'

    _resource_map = {'project': 'Project', 'assigned_to': 'User'}


class IssueRelation(BaseResource):
    redmine_version = '1.3'
    container_many = 'relations'
    container_one = 'relation'
    query_filter = '/issues/{issue_id}/relations.json'
    query_one = '/relations/{0}.json'
    query_create = '/issues/{issue_id}/relations.json'
    query_delete = '/relations/{0}.json'

    _repr = [['id']]
    _single_attr_id_map = {'issue_id': 'issue'}


class Version(BaseResource):
    redmine_version = '1.3'
    container_many = 'versions'
    container_one = 'version'
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{0}.json'
    query_create = '/projects/{project_id}/versions.json'
    query_update = '/versions/{0}.json'
    query_delete = '/versions/{0}.json'

    _unconvertible = ['status']
    _resource_map = {'project': 'Project'}
    _single_attr_id_map = {'project_id': 'project'}


class User(BaseResource):
    redmine_version = '1.1'
    container_many = 'users'
    container_one = 'user'
    query_all = '/users.json'
    query_one = '/users/{0}.json'
    query_filter = '/users.json'
    query_create = '/users.json'
    query_update = '/users/{0}.json'
    query_delete = '/users/{0}.json'

    _repr = [['id', 'firstname', 'lastname'], ['id', 'name']]
    _includes = ['memberships', 'groups']
    _relations = ['issues', 'time_entries']
    _relations_name = 'assigned_to'
    _unconvertible = ['status']
    _create_readonly = BaseResource._create_readonly + ['api_key', 'last_login_on']
    _update_readonly = _create_readonly[:]
    _resource_set_map = {
        'custom_fields': 'CustomField',
        'groups': 'Group',
        'memberships': 'ProjectMembership',
        'issues': 'Issue',
        'time_entries': 'TimeEntry',
    }

    def __getattr__(self, attr):
        if attr == 'time_entries' and attr not in self._encoded_attrs:
            self._relations_name = 'user'
            value = super(User, self).__getattr__(attr)
            self._relations_name = 'assigned_to'
            return value

        return super(User, self).__getattr__(attr)


class Group(BaseResource):
    redmine_version = '2.1'
    container_many = 'groups'
    container_one = 'group'
    query_all = '/groups.json'
    query_one = '/groups/{0}.json'
    query_create = '/groups.json'
    query_update = '/groups/{0}.json'
    query_delete = '/groups/{0}.json'

    _includes = ['memberships', 'users']
    _resource_set_map = {'memberships': 'ProjectMembership', 'users': 'User'}
    _multiple_attr_id_map = {'user_ids': 'users'}

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
            return self._redmine.engine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from a group.

            :param int user_id: (required). User id.
            """
            url = '{0}/groups/{1}/users/{2}.json'.format(self._redmine.url, self._group_id, user_id)
            return self._redmine.engine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'user':
            return Group.User(self)

        return super(Group, self).__getattr__(attr)


class Role(BaseResource):
    redmine_version = '1.4'
    container_many = 'roles'
    container_one = 'role'
    query_all = '/roles.json'
    query_one = '/roles/{0}.json'


class News(BaseResource):
    redmine_version = '1.1'
    container_many = 'news'
    query_all_export = '/news.{format}'
    query_all = '/news.json'
    query_filter = '/news.json'
    search_hints = ['news']

    _repr = [['id', 'title']]
    _resource_map = {'project': 'Project', 'author': 'User'}

    @property
    def url(self):
        return '{0}/news/{1}'.format(self.manager.redmine.url, self.internal_id)


class IssueStatus(BaseResource):
    redmine_version = '1.3'
    container_many = 'issue_statuses'
    query_all = '/issue_statuses.json'

    _relations = ['issues']
    _relations_name = 'status'
    _resource_set_map = {'issues': 'Issue'}

    @property
    def url(self):
        return '{0}/issue_statuses/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Tracker(BaseResource):
    redmine_version = '1.3'
    container_many = 'trackers'
    query_all = '/trackers.json'

    _relations = ['issues']
    _resource_set_map = {'issues': 'Issue'}

    @property
    def url(self):
        return '{0}/trackers/{1}/edit'.format(self.manager.redmine.url, self.internal_id)


class Query(BaseResource):
    redmine_version = '1.3'
    container_many = 'queries'
    query_all = '/queries.json'

    @property
    def url(self):
        return '{0}/projects/{1}/issues?query_id={2}'.format(
            self.manager.redmine.url, self._decoded_attrs.get('project_id', 0), self.internal_id)


class CustomField(BaseResource):
    redmine_version = '2.4'
    container_many = 'custom_fields'
    query_all = '/custom_fields.json'

    _resource_set_map = {'trackers': 'Tracker', 'roles': 'Role'}

    def __getattr__(self, attr):
        # If custom field was created after the creation of the resource,
        # i.e. project, and it's not used in the resource, there will be
        # no value attribute defined, that is why we need to return '' or
        # we'll get an exception
        if attr == 'value' and attr not in self._decoded_attrs:
            return ''

        return super(CustomField, self).__getattr__(attr)

    @classmethod
    def encode(cls, attr, value, manager):
        # Redmine <2.5.2 returns only single tracker instead of a list of
        # all available trackers, see http://www.redmine.org/issues/16739
        # for details
        if attr == 'trackers' and 'tracker' in value:
            value = [value['tracker']]

        return super(CustomField, cls).encode(attr, value, manager)

    @property
    def url(self):
        return '{0}/custom_fields/{1}/edit'.format(self.manager.redmine.url, self.internal_id)
