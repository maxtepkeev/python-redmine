"""
Defines standard Redmine resources and resource mappings.
"""

from . import BaseResource
from .. import managers, exceptions


class Project(BaseResource):
    redmine_version = (1, 0, 0)
    container_all = 'projects'
    container_one = 'project'
    container_create = 'project'
    container_update = 'project'
    query_all_export = '/projects.{format}'
    query_all = '/projects.json'
    query_one = '/projects/{}.json'
    query_create = '/projects.json'
    query_update = '/projects/{}.json'
    query_delete = '/projects/{}.json'
    search_hints = ['project']
    manager_class = managers.ProjectManager

    _repr = [['id', 'name'], ['title']]
    _includes = ['trackers', 'issue_categories', 'enabled_modules', 'time_entry_activities', 'issue_custom_fields']
    _relations = ['wiki_pages', 'memberships', 'issue_categories', 'time_entries', 'versions',
                  'news', 'issues', 'files']
    _unconvertible = BaseResource._unconvertible + ['identifier', 'status']
    _update_readonly = BaseResource._update_readonly + ['identifier']
    _resource_map = {'default_version': 'Version', 'default_assignee': 'User'}
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
        'files': 'File',
        'time_entry_activities': 'Enumeration',
        'issue_custom_fields': 'CustomField',
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

        return super().encode(attr, value, manager)

    def __getattr__(self, attr):
        if attr in ('close', 'reopen', 'archive', 'unarchive'):
            return lambda: getattr(self.manager, attr)(self.internal_id)

        return super().__getattr__(attr)


class Issue(BaseResource):
    redmine_version = (1, 0, 0)
    container_all = 'issues'
    container_one = 'issue'
    container_filter = 'issues'
    container_create = 'issue'
    container_update = 'issue'
    query_all_export = '/issues.{format}'
    query_one_export = '/issues/{}.{format}'
    query_all = '/issues.json?status_id=*'
    query_one = '/issues/{}.json'
    query_filter = '/issues.json'
    query_create = '/projects/{project_id}/issues.json'
    query_update = '/issues/{}.json'
    query_delete = '/issues/{}.json'
    search_hints = ['issue', 'issue closed', 'issue-closed']
    extra_export_columns = ['description', 'last_notes']
    manager_class = managers.IssueManager

    _repr = [['id', 'subject'], ['title'], ['id']]
    _includes = ['children', 'attachments', 'relations', 'changesets', 'journals', 'watchers', 'allowed_statuses']
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
        'allowed_statuses': 'IssueStatus',
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

            if self._redmine.ver is not None and self._redmine.ver < (2, 3, 0):
                raise exceptions.ResourceVersionMismatchError

        def add(self, user_id):
            """
            Adds user to issue watchers list.

            :param int user_id: (required). User id.
            """
            url = f'{self._redmine.url}/issues/{self._issue_id}/watchers.json'
            return self._redmine.engine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from issue watchers list.

            :param int user_id: (required). User id.
            """
            url = f'{self._redmine.url}/issues/{self._issue_id}/watchers/{user_id}.json'
            return self._redmine.engine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'watcher':
            return Issue.Watcher(self)

        if attr == 'version':
            attr = 'fixed_version'

        return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        if attr == 'version_id':
            attr = 'fixed_version_id'

        super().__setattr__(attr, value)

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'version_id':
            return 'fixed_version_id', value
        elif attr == 'assigned_to_id' and value in (None, 0):
            return attr, ''
        elif attr == 'checklists':
            return 'checklists_attributes', value

        return super().decode(attr, value, manager)

    def copy(self, link_original=True, include=(), **fields):
        if 'project_id' not in fields and not self.is_new():
            fields['project_id'] = self._decoded_attrs['project']['id']

        return self.manager.copy(self.internal_id, link_original=link_original, include=include, **fields)


class TimeEntry(BaseResource):
    redmine_version = (1, 1, 0)
    container_all = 'time_entries'
    container_one = 'time_entry'
    container_filter = 'time_entries'
    container_create = 'time_entry'
    container_update = 'time_entry'
    query_all_export = '/time_entries.{format}'
    query_all = '/time_entries.json'
    query_one = '/time_entries/{}.json'
    query_filter = '/time_entries.json'
    query_create = '/time_entries.json'
    query_update = '/time_entries/{}.json'
    query_delete = '/time_entries/{}.json'

    _repr = [['id']]
    _resource_map = {'project': 'Project', 'issue': 'Issue', 'user': 'User', 'activity': 'Enumeration'}
    _resource_set_map = {'custom_fields': 'CustomField'}
    _single_attr_id_map = {'project_id': 'project', 'issue_id': 'issue', 'activity_id': 'activity'}

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'from_date':
            attr = 'from'
        elif attr == 'to_date':
            attr = 'to'

        return super().decode(attr, value, manager)


class Enumeration(BaseResource):
    redmine_version = (2, 2, 0)
    container_filter = '{resource}'
    query_filter = '/enumerations/{resource}.json'
    query_url = '/enumerations/{}/edit'

    _resource_set_map = {'custom_fields': 'CustomField'}


class Attachment(BaseResource):
    redmine_version = (1, 3, 0)
    container_one = 'attachment'
    container_update = 'attachment'
    query_one = '/attachments/{}.json'
    query_update = '/attachments/{}.json'
    query_delete = '/attachments/{}.json'
    http_method_update = 'patch'

    _repr = [['id', 'filename'], ['id']]
    _resource_map = {'author': 'User'}

    def download(self, savepath=None, filename=None):
        return self.manager.redmine.download(self.content_url, savepath, filename)


class File(Attachment):
    redmine_version = (3, 4, 0)
    container_filter = 'files'
    container_create = 'file'
    query_filter = '/projects/{project_id}/files.json'
    query_create = '/projects/{project_id}/files.json'
    manager_class = managers.FileManager

    _resource_map = {'author': 'User', 'version': 'Version'}

    @classmethod
    def decode(cls, attr, value, manager):
        if attr == 'path':
            return 'token', manager.redmine.upload(value)['token']

        return super().decode(attr, value, manager)


class IssueJournal(BaseResource):
    redmine_version = (1, 0, 0)
    container_update = 'journal'
    query_update = '/journals/{}.json'

    _repr = [['id']]
    _unconvertible = ['notes']
    _resource_map = {'user': 'User'}


class WikiPage(BaseResource):
    internal_id_key = 'title'
    redmine_version = (2, 2, 0)
    container_filter = 'wiki_pages'
    container_one = 'wiki_page'
    container_create = 'wiki_page'
    container_update = 'wiki_page'
    query_one_export = '/projects/{project_id}/wiki/{}.{format}'
    query_filter = '/projects/{project_id}/wiki/index.json'
    query_one = '/projects/{project_id}/wiki/{}.json'
    query_create = '/projects/{project_id}/wiki/{title}.json'
    query_update = '/projects/{project_id}/wiki/{}.json'
    query_delete = '/projects/{project_id}/wiki/{}.json'
    search_hints = ['wiki-page']
    http_method_create = 'put'
    manager_class = managers.WikiPageManager

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

        return super().encode(attr, value, manager)

    def refresh(self, **params):
        return super().refresh(**dict(params, project_id=self.project_id))

    def post_update(self):
        self._encoded_attrs['version'] = self._decoded_attrs['version'] = self._decoded_attrs.get('version', 0) + 1

    def delete(self, **params):
        return super().delete(**dict(params, project_id=self.project_id))

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

        return super().__getattr__(attr)

    def __int__(self):
        return self.version


class ProjectMembership(BaseResource):
    redmine_version = (1, 4, 0)
    container_filter = 'memberships'
    container_one = 'membership'
    container_update = 'membership'
    container_create = 'membership'
    query_filter = '/projects/{project_id}/memberships.json'
    query_one = '/memberships/{}.json'
    query_create = '/projects/{project_id}/memberships.json'
    query_update = '/memberships/{}.json'
    query_delete = '/memberships/{}.json'

    _repr = [['id']]
    _create_readonly = BaseResource._create_readonly + ['user', 'roles']
    _update_readonly = _create_readonly[:]
    _resource_map = {'project': 'Project', 'user': 'User', 'group': 'Group'}
    _resource_set_map = {'roles': 'Role'}
    _single_attr_id_map = {'project_id': 'project', 'user_id': 'user'}
    _multiple_attr_id_map = {'role_ids': 'roles'}


class IssueCategory(BaseResource):
    redmine_version = (1, 3, 0)
    container_filter = 'issue_categories'
    container_one = 'issue_category'
    container_update = 'issue_category'
    container_create = 'issue_category'
    query_filter = '/projects/{project_id}/issue_categories.json'
    query_one = '/issue_categories/{}.json'
    query_create = '/projects/{project_id}/issue_categories.json'
    query_update = '/issue_categories/{}.json'
    query_delete = '/issue_categories/{}.json'

    _resource_map = {'project': 'Project', 'assigned_to': 'User'}
    _single_attr_id_map = {'project_id': 'project', 'assigned_to_id': 'assigned_to'}


class IssueRelation(BaseResource):
    redmine_version = (1, 3, 0)
    container_filter = 'relations'
    container_one = 'relation'
    container_create = 'relation'
    query_filter = '/issues/{issue_id}/relations.json'
    query_one = '/relations/{}.json'
    query_create = '/issues/{issue_id}/relations.json'
    query_delete = '/relations/{}.json'

    _repr = [['id']]
    _single_attr_id_map = {'issue_id': 'issue'}


class Version(BaseResource):
    redmine_version = (1, 3, 0)
    container_filter = 'versions'
    container_one = 'version'
    container_create = 'version'
    container_update = 'version'
    query_filter = '/projects/{project_id}/versions.json'
    query_one = '/versions/{}.json'
    query_create = '/projects/{project_id}/versions.json'
    query_update = '/versions/{}.json'
    query_delete = '/versions/{}.json'

    _unconvertible = ['status']
    _resource_map = {'project': 'Project'}
    _resource_set_map = {'custom_fields': 'CustomField'}
    _single_attr_id_map = {'project_id': 'project'}


class User(BaseResource):
    redmine_version = (1, 1, 0)
    container_all = 'users'
    container_one = 'user'
    container_filter = 'users'
    container_create = 'user'
    container_update = 'user'
    query_all_export = '/users.{format}'
    query_all = '/users.json?status='
    query_one = '/users/{}.json'
    query_filter = '/users.json'
    query_create = '/users.json'
    query_update = '/users/{}.json'
    query_delete = '/users/{}.json'
    manager_class = managers.UserManager

    _repr = [['id', 'firstname', 'lastname'], ['id', 'name']]
    _includes = ['memberships', 'groups']
    _relations = ['issues', 'issues_assigned', 'issues_authored', 'time_entries']
    _relations_name = 'assigned_to'
    _unconvertible = ['status']
    _create_readonly = BaseResource._create_readonly + ['api_key', 'last_login_on']
    _update_readonly = _create_readonly[:]
    _resource_set_map = {
        'custom_fields': 'CustomField',
        'groups': 'Group',
        'memberships': 'ProjectMembership',
        'issues': 'Issue',
        'issues_assigned': 'Issue',
        'issues_authored': 'Issue',
        'time_entries': 'TimeEntry',
    }

    def __getattr__(self, attr):
        if attr in self._relations and attr not in self._encoded_attrs:
            if attr == 'issues_authored':
                self._relations_name = 'author'
            elif attr == 'time_entries':
                self._relations_name = 'user'

            value = super().__getattr__(attr)
            self._relations_name = 'assigned_to'
            return value

        return super().__getattr__(attr)


class Group(BaseResource):
    redmine_version = (2, 1, 0)
    container_all = 'groups'
    container_one = 'group'
    container_create = 'group'
    container_update = 'group'
    query_all = '/groups.json'
    query_one = '/groups/{}.json'
    query_create = '/groups.json'
    query_update = '/groups/{}.json'
    query_delete = '/groups/{}.json'

    _includes = ['memberships', 'users']
    _resource_set_map = {'memberships': 'ProjectMembership', 'users': 'User', 'custom_fields': 'CustomField'}
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
            url = f'{self._redmine.url}/groups/{self._group_id}/users.json'
            return self._redmine.engine.request('post', url, data={'user_id': user_id})

        def remove(self, user_id):
            """
            Removes user from a group.

            :param int user_id: (required). User id.
            """
            url = f'{self._redmine.url}/groups/{self._group_id}/users/{user_id}.json'
            return self._redmine.engine.request('delete', url)

    def __getattr__(self, attr):
        if attr == 'user':
            return Group.User(self)

        return super().__getattr__(attr)


class Role(BaseResource):
    redmine_version = (1, 4, 0)
    container_all = 'roles'
    container_one = 'role'
    query_all = '/roles.json'
    query_one = '/roles/{}.json'


class News(BaseResource):
    redmine_version = (1, 1, 0)
    container_all = 'news'
    container_one = 'news'
    container_filter = 'news'
    container_create = 'news'
    container_update = 'news'
    query_all_export = '/news.{format}'
    query_all = '/news.json'
    query_one = '/news/{}.json'
    query_filter = '/news.json'
    query_create = '/projects/{project_id}/news.json'
    query_update = '/news/{}.json'
    query_delete = '/news/{}.json'
    search_hints = ['news']
    manager_class = managers.NewsManager

    _repr = [['id', 'title']]
    _includes = ['attachments', 'comments']
    _resource_map = {'project': 'Project', 'author': 'User'}
    _resource_set_map = {'attachments': 'Attachment'}
    _single_attr_id_map = {'project_id': 'project'}


class IssueStatus(BaseResource):
    redmine_version = (1, 3, 0)
    container_all = 'issue_statuses'
    query_all = '/issue_statuses.json'
    query_url = '/issue_statuses/{}/edit'

    _relations = ['issues']
    _relations_name = 'status'
    _resource_set_map = {'issues': 'Issue'}


class Tracker(BaseResource):
    redmine_version = (1, 3, 0)
    container_all = 'trackers'
    query_all = '/trackers.json'
    query_url = '/trackers/{}/edit'

    _relations = ['issues']
    _resource_set_map = {'issues': 'Issue'}


class Query(BaseResource):
    redmine_version = (1, 3, 0)
    container_all = 'queries'
    query_all = '/queries.json'
    query_url = '/projects/{}/issues?query_id={}'

    @property
    def url(self):
        return self.manager.redmine.url + self.query_url.format(
            self._decoded_attrs.get('project_id', 0), self.internal_id)


class CustomField(BaseResource):
    redmine_version = (2, 4, 0)
    container_all = 'custom_fields'
    query_all = '/custom_fields.json'
    query_url = '/custom_fields/{}/edit'

    _resource_set_map = {'trackers': 'Tracker', 'roles': 'Role'}

    def __getattr__(self, attr):
        # If custom field was created after the creation of the resource,
        # i.e. project, and it's not used in the resource, there will be
        # no value attribute defined, that is why we need to return '' or
        # we'll get an exception
        if attr == 'value' and attr not in self._decoded_attrs:
            return ''

        return super().__getattr__(attr)

    @classmethod
    def encode(cls, attr, value, manager):
        # Redmine <2.5.2 returns only single tracker instead of a list of
        # all available trackers, see http://www.redmine.org/issues/16739
        # for details
        if attr == 'trackers' and 'tracker' in value:
            value = [value['tracker']]

        return super().encode(attr, value, manager)
