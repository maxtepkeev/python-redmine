from tests import unittest, mock, Redmine, URL
from redmine.resultsets import ResourceSet

responses = {
    'project': {
        'get': {'project': {'name': 'Foo', 'id': 1, 'identifier': 'foo'}},
        'all': {'projects': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'issue': {
        'get': {'issue': {'subject': 'Foo', 'id': 1}},
        'all': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
        'filter': {'issues': [{'subject': 'Foo', 'id': 1}, {'subject': 'Bar', 'id': 2}]},
    },
    'time_entry': {
        'get': {'time_entry': {'hours': 2, 'id': 1}},
        'all': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
        'filter': {'time_entries': [{'hours': 3, 'id': 1}, {'hours': 4, 'id': 2}]},
    },
    'enumeration': {
        'filter': {'time_entry_activities': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'attachment': {
        'get': {'attachment': {'filename': 'foo.jpg', 'id': 1}},
    },
    'wiki_page': {
        'get': {'wiki_page': {'title': 'Foo', 'version': 1}},
        'filter': {'wiki_pages': [{'title': 'Foo', 'version': 1}, {'title': 'Bar', 'version': 2}]},
    },
    'project_membership': {
        'get': {'membership': {'id': 1}},
        'filter': {'memberships': [{'id': 1}, {'id': 2}]},
    },
    'issue_category': {
        'get': {'issue_category': {'id': 1, 'name': 'Foo'}},
        'filter': {'issue_categories': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'issue_relation': {
        'get': {'relation': {'id': 1}},
        'filter': {'relations': [{'id': 1}, {'id': 2}]},
    },
    'version': {
        'get': {'version': {'id': 1, 'name': 'Foo'}},
        'filter': {'versions': [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]},
    },
    'user': {
        'get': {'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1}},
        'all': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
        'filter': {'users': [{'firstname': 'John', 'id': 1}, {'firstname': 'Jack', 'id': 2}]},
    },
    'group': {
        'get': {'group': {'name': 'Foo', 'id': 1}},
        'all': {'groups': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'role': {
        'get': {'role': {'name': 'Foo', 'id': 1}},
        'all': {'roles': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'news': {
        'all': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
        'filter': {'news': [{'title': 'Foo', 'id': 1}, {'title': 'Bar', 'id': 2}]},
    },
    'issue_status': {
        'all': {'issue_statuses': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'tracker': {
        'all': {'trackers': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'query': {
        'all': {'queries': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'custom_field': {
        'all': {'custom_fields': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'contact_tag': {
        'all': {'tags': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'deal_status': {
        'all': {'deal_statuses': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'deal_category': {
        'filter': {'deal_categories': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'crm_query': {
        'filter': {'queries': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
    'note': {
        'get': {'note': {'content': 'foobar', 'id': 1}},
    },
    'contact': {
        'get': {'contact': {'first_name': 'Foo', 'id': 1}},
        'all': {'contacts': [{'first_name': 'Foo', 'id': 1}, {'first_name': 'Bar', 'id': 2}]},
        'filter': {'contacts': [{'first_name': 'Foo', 'id': 1}, {'first_name': 'Bar', 'id': 2}]},
    },
    'deal': {
        'get': {'deal': {'name': 'Foo', 'id': 1}},
        'all': {'deals': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
        'filter': {'deals': [{'name': 'Foo', 'id': 1}, {'name': 'Bar', 'id': 2}]},
    },
}


class TestResources(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.redmine = Redmine(self.url)
        self.response = mock.Mock(status_code=200)
        patcher_get = mock.patch('redmine.requests.get', return_value=self.response)
        patcher_post = mock.patch('redmine.requests.post', return_value=self.response)
        patcher_put = mock.patch('redmine.requests.put', return_value=self.response)
        patcher_delete = mock.patch('redmine.requests.delete', return_value=self.response)
        patcher_get.start()
        patcher_post.start()
        patcher_put.start()
        patcher_delete.start()
        self.addCleanup(patcher_get.stop)
        self.addCleanup(patcher_post.stop)
        self.addCleanup(patcher_put.stop)
        self.addCleanup(patcher_delete.stop)

    def test_supports_dictionary_like_attribute_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project['id'], 1)
        self.assertEqual(project['name'], 'Foo')

    def test_supports_url_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).url, '{0}/projects/foo'.format(self.url))

    def test_supports_internal_id(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).internal_id, 1)

    def test_supports_setting_of_attributes(self):
        project = self.redmine.project.new()
        project.name = 'Foo'
        project.description = 'Bar'
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.description, 'Bar')

    def test_supports_setting_of_date_datetime_attributes(self):
        from datetime import date, datetime
        issue = self.redmine.issue.new()
        issue.start_date = date(2014, 3, 9)
        self.assertEqual(issue._attributes['start_date'], date(2014, 3, 9))
        self.assertEqual(issue._changes['start_date'], '2014-03-09')
        issue.start_date = datetime(2014, 3, 9, 20, 2, 2)
        self.assertEqual(issue._attributes['start_date'], datetime(2014, 3, 9, 20, 2, 2))
        self.assertEqual(issue._changes['start_date'], '2014-03-09T20:02:02Z')

    def test_supports_setting_of_attributes_via_dict(self):
        project = self.redmine.project.new()
        project['name'] = 'Foo'
        project['description'] = 'Bar'
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.description, 'Bar')

    def test_setting_create_readonly_attrs_raises_exception(self):
        from redmine.exceptions import ReadonlyAttrError
        with self.assertRaises(ReadonlyAttrError):
            project = self.redmine.project.new()
            project.id = 1

    def test_setting_update_readonly_attrs_raises_exception(self):
        from redmine.exceptions import ReadonlyAttrError
        with self.assertRaises(ReadonlyAttrError):
            self.response.json.return_value = responses['project']['get']
            project = self.redmine.project.get(1)
            project.identifier = 1

    def test_control_raising_of_resource_attr_exception(self):
        from redmine.exceptions import ResourceAttrError
        self.response.json.return_value = responses['project']['get']
        self.redmine.raise_attr_exception = False
        self.assertEqual(self.redmine.project.get(1).foo, None)
        self.redmine.raise_attr_exception = ('Project',)
        self.assertRaises(ResourceAttrError, lambda: self.redmine.project.get(1).foo)
        self.redmine.raise_attr_exception = True
        self.assertRaises(ResourceAttrError, lambda: self.redmine.project.get(1).foo)

    def test_saving_new_resource_creates_it(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.new()
        project.name = 'Foo'
        self.assertEqual(project.save(), True)
        self.assertEqual(project.id, 1)

    def test_saving_existing_resource_updates_it(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        project.name = 'Bar'
        self.assertEqual(project.save(), True)
        self.response.json.return_value = {'project': {'id': 1, 'name': 'Bar'}}
        project = project.refresh()
        self.assertEqual(project.name, 'Bar')

    def test_custom_int(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(int(self.redmine.project.get(1)), 1)

    def test_custom_str(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(str(self.redmine.project.get(1)), 'Foo')

    def test_custom_repr(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(repr(self.redmine.project.get(1)), '<redmine.resources.Project #1 "Foo">')

    def test_can_refresh_itself(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, 'Foo')
        self.response.json.return_value = {'project': {'id': 2, 'name': 'Bar'}}
        project = project.refresh()
        self.assertEqual(project.id, 2)
        self.assertEqual(project.name, 'Bar')

    def test_resource_dict_is_converted_to_resource_object(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._attributes['author'] = {'id': 1, 'name': 'John Smith'}
        self.assertEqual(repr(issue.author), '<redmine.resources.User #1 "John Smith">')

    def test_resource_list_of_dicts_is_converted_to_resource_set(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._attributes['custom_fields'] = [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]
        self.assertEqual(
            repr(issue.custom_fields),
            '<redmine.resultsets.ResourceSet object with CustomField resources>'
        )

    def test_dir_returns_resource_attributes(self):
        self.response.json.return_value = responses['issue']['get']
        attributes = dir(self.redmine.issue.get(1))
        self.assertIn('id', attributes)
        self.assertIn('subject', attributes)
        self.assertIn('relations', attributes)
        self.assertIn('time_entries', attributes)

    def test_supports_iteration(self):
        self.response.json.return_value = responses['project']['get']
        project = list(self.redmine.project.get(1))
        self.assertIn(('name', 'Foo'), project)
        self.assertIn(('id', 1), project)

    def test_setting_custom_field_raises_exception_if_not_list_of_dicts(self):
        from redmine.exceptions import CustomFieldValueError
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1}]}}
        project = self.redmine.project.get(1)
        with self.assertRaises(CustomFieldValueError):
            project.custom_fields = 'foo'

    def test_resource_is_picklable(self):
        import pickle
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        unpickled_project = pickle.loads(pickle.dumps(project))
        self.assertEqual(project.id, unpickled_project.id)
        self.assertEqual(project.name, unpickled_project.name)

    def test_project_version(self):
        self.assertEqual(self.redmine.project.resource_class.redmine_version, '1.0')

    def test_project_get(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, 'Foo')

    def test_project_all(self):
        self.response.json.return_value = responses['project']['all']
        projects = self.redmine.project.all()
        self.assertEqual(projects[0].id, 1)
        self.assertEqual(projects[0].name, 'Foo')
        self.assertEqual(projects[1].id, 2)
        self.assertEqual(projects[1].name, 'Bar')

    def test_project_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.create(name='Foo', identifier='foo')
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, 'Foo')

    def test_project_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.project.delete(1), True)

    def test_project_update(self):
        self.response.json.return_value = {
            'project': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        project = self.redmine.project.get(1)
        project.homepage = 'http://foo.bar'
        project.parent_id = 3
        project.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertEqual(project.save(), True)
        self.assertEqual(project.custom_fields[0].value, 'bar')

    def test_project_relations(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertIsInstance(project.wiki_pages, ResourceSet)
        self.assertIsInstance(project.memberships, ResourceSet)
        self.assertIsInstance(project.issue_categories, ResourceSet)
        self.assertIsInstance(project.versions, ResourceSet)
        self.assertIsInstance(project.news, ResourceSet)
        self.assertIsInstance(project.issues, ResourceSet)

    def test_project_includes(self):
        response_includes = responses['project']['get']
        self.response.json.return_value = response_includes
        project = self.redmine.project.get(1)
        response_includes['project'].update(responses['issue_category']['filter'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.issue_categories, ResourceSet)
        response_includes['project'].update(responses['tracker']['all'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.trackers, ResourceSet)
        response_includes['project'].update({'enabled_modules': [{'id': 36, 'name': 'issue_tracking'}]})
        self.response.json.return_value = response_includes
        self.assertEqual(project.enabled_modules, ['issue_tracking'])

    def test_project_returns_status_without_conversion(self):
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'status': 1}}
        project = self.redmine.project.get(1)
        self.assertEqual(project.status, 1)

    def test_project_is_new(self):
        project = self.redmine.project.new()
        self.assertEqual(int(project), 0)
        self.assertEqual(str(project), '')
        self.assertEqual(repr(project), '<redmine.resources.Project #0 "">')

    def test_project_url(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).url, '{0}/projects/foo'.format(self.url))

    def test_project_parent_converts_to_resource(self):
        from redmine.resources import Project
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'parent': {'id': 2}}}
        parent = self.redmine.project.get(1).parent
        self.assertIsInstance(parent, Project)
        self.assertEqual(parent.id, 2)

    def test_issue_version(self):
        self.assertEqual(self.redmine.issue.resource_class.redmine_version, '1.0')

    def test_issue_get(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.assertEqual(issue.id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_issue_all(self):
        self.response.json.return_value = responses['issue']['all']
        issues = self.redmine.issue.all()
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[0].subject, 'Foo')
        self.assertEqual(issues[1].id, 2)
        self.assertEqual(issues[1].subject, 'Bar')

    def test_issue_filter(self):
        self.response.json.return_value = responses['issue']['filter']
        issues = self.redmine.issue.filter(project_id=1)
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[0].subject, 'Foo')
        self.assertEqual(issues[1].id, 2)
        self.assertEqual(issues[1].subject, 'Bar')

    def test_issue_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.create(project_id='bar', subject='Foo', version_id=1)
        self.assertEqual(issue.id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_issue_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.issue.delete(1), True)

    def test_issue_update(self):
        self.response.json.return_value = {
            'issue': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        issue = self.redmine.issue.get(1)
        issue.subject = 'Foo'
        issue.description = 'foobar'
        issue.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertEqual(issue.save(), True)
        self.assertEqual(issue.custom_fields[0].value, 'bar')

    def test_issue_relations(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.assertIsInstance(issue.relations, ResourceSet)
        self.assertIsInstance(issue.time_entries, ResourceSet)

    def test_issue_includes(self):
        response_includes = responses['issue']['get']
        self.response.json.return_value = response_includes
        issue = self.redmine.issue.get(1)
        response_includes['issue']['children'] = responses['issue']['all']['issues']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.children, ResourceSet)
        response_includes['issue']['attachments'] = responses['attachment']['get']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.attachments, ResourceSet)
        response_includes['issue']['relations'] = responses['issue_relation']['get']['relation']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.relations, ResourceSet)
        response_includes['issue']['journals'] = [{'id': 1}, {'id': 2}]
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.journals, ResourceSet)
        response_includes['issue']['watchers'] = responses['user']['all']['users']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.watchers, ResourceSet)

    def test_issue_add_watcher_raises_exception_if_wrong_version(self):
        from redmine.exceptions import ResourceVersionMismatchError
        self.response.json.return_value = responses['issue']['get']
        self.redmine.ver = '2.2.0'
        issue = self.redmine.issue.get(1)
        self.assertRaises(ResourceVersionMismatchError, lambda: issue.watcher.add(1))

    def test_issue_add_watcher(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.response.content = ''
        self.assertEqual(issue.watcher.add(1), True)

    def test_issue_remove_watcher(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.response.content = ''
        self.assertEqual(issue.watcher.remove(1), True)

    def test_issue_custom_repr(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(repr(self.redmine.issue.get(1)), '<redmine.resources.Issue #1 "Foo">')

    def test_issue_custom_repr_without_subject(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        del issue['_attributes']['subject']
        self.assertEqual(repr(issue), '<redmine.resources.Issue #1>')

    def test_issue_custom_str(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(str(self.redmine.issue.get(1)), 'Foo')

    def test_issue_custom_str_without_subject(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        del issue['_attributes']['subject']
        self.assertEqual(str(issue), '1')

    def test_issue_journals(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._attributes['journals'] = [{'id': 1}]
        self.assertEqual(str(issue.journals[0]), '1')
        self.assertEqual(repr(issue.journals[0]), '<redmine.resources.IssueJournal #1>')

    def test_issue_journals_url(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._attributes['journals'] = [{'id': 1}]
        self.assertEqual(issue.journals[0].url, None)

    def test_issue_version_can_be_retrieved_via_version_attribute(self):
        from redmine.resources import Version
        self.response.json.return_value = {
            'issue': {'subject': 'Foo', 'id': 1, 'fixed_version': {'id': 1, 'name': 'Foo'}}}
        issue = self.redmine.issue.get(1)
        self.assertIsInstance(issue.version, Version)

    def test_issue_version_can_be_set_via_version_attribute(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue.version_id = 1
        self.assertEqual(issue.fixed_version.id, 1)

    def test_issue_is_new(self):
        issue = self.redmine.issue.new()
        self.assertEqual(int(issue), 0)
        self.assertEqual(str(issue), '')
        self.assertEqual(repr(issue), '<redmine.resources.Issue #0 "">')

    def test_issue_url(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(self.redmine.issue.get(1).url, '{0}/issues/1'.format(self.url))

    def test_issue_parent_converts_to_resource(self):
        from redmine.resources import Issue
        self.response.json.return_value = {'issue': {'subject': 'Foo', 'id': 1, 'parent': {'id': 2}}}
        parent = self.redmine.issue.get(1).parent
        self.assertIsInstance(parent, Issue)
        self.assertEqual(parent.id, 2)

    def test_time_entry_version(self):
        self.assertEqual(self.redmine.time_entry.resource_class.redmine_version, '1.1')

    def test_time_entry_get(self):
        self.response.json.return_value = responses['time_entry']['get']
        time_entry = self.redmine.time_entry.get(1)
        self.assertEqual(time_entry.id, 1)
        self.assertEqual(time_entry.hours, 2)

    def test_time_entry_all(self):
        self.response.json.return_value = responses['time_entry']['all']
        time_entries = self.redmine.time_entry.all()
        self.assertEqual(time_entries[0].id, 1)
        self.assertEqual(time_entries[0].hours, 3)
        self.assertEqual(time_entries[1].id, 2)
        self.assertEqual(time_entries[1].hours, 4)

    def test_time_entry_filter(self):
        self.response.json.return_value = responses['time_entry']['filter']
        time_entries = self.redmine.time_entry.filter(issue_id=1)
        self.assertEqual(time_entries[0].id, 1)
        self.assertEqual(time_entries[0].hours, 3)
        self.assertEqual(time_entries[1].id, 2)
        self.assertEqual(time_entries[1].hours, 4)

    def test_time_entry_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['time_entry']['get']
        time_entry = self.redmine.time_entry.create(issue_id=1, hours=2)
        self.assertEqual(time_entry.id, 1)
        self.assertEqual(time_entry.hours, 2)

    def test_time_entry_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.time_entry.delete(1), True)

    def test_time_entry_update(self):
        self.response.json.return_value = {
            'time_entry': {'hours': 2, 'id': 1, 'issue': {'id': 1}, 'activity': {'id': 1}}}
        time_entry = self.redmine.time_entry.get(1)
        time_entry.hours = 3
        time_entry.issue_id = 2
        time_entry.activity_id = 2
        self.assertEqual(time_entry.save(), True)

    def test_time_entry_translate_params(self):
        manager = self.redmine.time_entry
        manager.filter(from_date='2013-12-30', to_date='2013-12-31')
        self.assertIn('from', manager.params)
        self.assertIn('to', manager.params)

    def test_time_entry_custom_str(self):
        self.response.json.return_value = responses['time_entry']['get']
        self.assertEqual(str(self.redmine.time_entry.get(1)), '1')

    def test_time_entry_custom_repr(self):
        self.response.json.return_value = responses['time_entry']['get']
        self.assertEqual(repr(self.redmine.time_entry.get(1)), '<redmine.resources.TimeEntry #1>')

    def test_time_entry_is_new(self):
        time_entry = self.redmine.time_entry.new()
        self.assertEqual(int(time_entry), 0)
        self.assertEqual(str(time_entry), '0')
        self.assertEqual(repr(time_entry), '<redmine.resources.TimeEntry #0>')

    def test_time_entry_url(self):
        self.response.json.return_value = responses['time_entry']['get']
        self.assertEqual(self.redmine.time_entry.get(1).url, '{0}/time_entries/1'.format(self.url))

    def test_enumeration_version(self):
        self.assertEqual(self.redmine.enumeration.resource_class.redmine_version, '2.2')

    def test_enumeration_filter(self):
        self.response.json.return_value = responses['enumeration']['filter']
        enumerations = self.redmine.enumeration.filter(resource='time_entry_activities')
        self.assertEqual(enumerations[0].id, 1)
        self.assertEqual(enumerations[0].name, 'Foo')
        self.assertEqual(enumerations[1].id, 2)
        self.assertEqual(enumerations[1].name, 'Bar')

    def test_enumeration_url(self):
        self.response.json.return_value = responses['enumeration']['filter']
        self.assertEqual(
            self.redmine.enumeration.filter(resource='time_entry_activities')[0].url,
            '{0}/enumerations/1/edit'.format(self.url)
        )

    def test_attachment_version(self):
        self.assertEqual(self.redmine.attachment.resource_class.redmine_version, '1.3')

    def test_attachment_get(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        self.assertEqual(attachment.id, 1)
        self.assertEqual(attachment.filename, 'foo.jpg')

    def test_attachment_custom_str(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(str(self.redmine.attachment.get(1)), 'foo.jpg')

    def test_attachment_custom_str_without_filename(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        del attachment['_attributes']['filename']
        self.assertEqual(str(attachment), '1')

    def test_attachment_custom_repr(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(repr(self.redmine.attachment.get(1)), '<redmine.resources.Attachment #1 "foo.jpg">')

    def test_attachment_custom_repr_without_subject(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        del attachment['_attributes']['filename']
        self.assertEqual(repr(attachment), '<redmine.resources.Attachment #1>')

    def test_attachment_url(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(self.redmine.attachment.get(1).url, '{0}/attachments/1'.format(self.url))

    @mock.patch('redmine.open', mock.mock_open(), create=True)
    def test_attachment_download(self):
        response = responses['attachment']['get']
        response['attachment']['content_url'] = 'http://foo/bar.txt'
        self.response.json.return_value = response
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.attachment.get(1).download('/some/path'), '/some/path/bar.txt')

    def test_wiki_page_version(self):
        self.assertEqual(self.redmine.wiki_page.resource_class.redmine_version, '2.2')

    def test_wiki_page_get(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.assertEqual(wiki_page.title, 'Foo')

    def test_wiki_page_filter(self):
        self.response.json.return_value = responses['wiki_page']['filter']
        wiki_pages = self.redmine.wiki_page.filter(project_id=1)
        self.assertEqual(wiki_pages[0].title, 'Foo')
        self.assertEqual(wiki_pages[1].title, 'Bar')

    def test_wiki_page_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.create(project_id='foo', title='Foo')
        self.assertEqual(wiki_page.title, 'Foo')

    def test_wiki_page_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.wiki_page.delete('Foo', project_id=1), True)

    def test_wiki_page_update(self):
        self.response.json.return_value = \
            {'wiki_page': {'title': 'Foo', 'version': 1, 'created_on': '2012-06-27T12:48:15Z'}}
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        wiki_page.text = 'Foo'
        self.assertEqual(wiki_page.save(), True)
        self.assertEqual(wiki_page.version, 2)

    def test_wiki_page_refresh_by_title(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.assertEqual(wiki_page.title, 'Foo')
        self.response.json.return_value = {'wiki_page': {'title': 'Bar'}}
        wiki_page = wiki_page.refresh()
        self.assertEqual(wiki_page.title, 'Bar')

    def test_wiki_page_refreshes_itself_if_text_attribute_not_exists(self):
        self.response.json.return_value = {'wiki_page': {'title': 'Foo', 'created_on': '2012-06-27T12:48:15Z'}}
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.response.json.return_value = {'wiki_page': {'title': 'Foo', 'text': 'foo'}}
        self.assertEqual(wiki_page.text, 'foo')

    def test_wiki_page_supports_internal_id(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(self.redmine.wiki_page.get('Foo', project_id=1).internal_id, 'Foo')

    def test_wiki_page_custom_int(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(int(self.redmine.wiki_page.get('Foo', project_id=1)), 1)

    def test_wiki_page_custom_str(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(str(self.redmine.wiki_page.get('Foo', project_id=1)), 'Foo')

    def test_wiki_page_custom_repr(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(repr(self.redmine.wiki_page.get('Foo', project_id=1)), '<redmine.resources.WikiPage "Foo">')

    def test_wiki_page_includes(self):
        response_includes = responses['wiki_page']['get']
        self.response.json.return_value = response_includes
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        response_includes['wiki_page']['attachments'] = responses['attachment']['get']['attachment']
        self.response.json.return_value = response_includes
        self.assertIsInstance(wiki_page.attachments, ResourceSet)

    def test_wiki_page_is_new(self):
        wiki_page = self.redmine.wiki_page.new()
        self.assertEqual(int(wiki_page), 0)
        self.assertEqual(str(wiki_page), '')
        self.assertEqual(repr(wiki_page), '<redmine.resources.WikiPage "">')

    def test_wiki_page_url(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(
            self.redmine.wiki_page.get('Foo', project_id='Foo').url,
            '{0}/projects/Foo/wiki/Foo'.format(self.url)
        )

    def test_wiki_page_parent_converts_to_resource(self):
        from redmine.resources import WikiPage
        self.response.json.return_value = {'wiki_page': {'title': 'Foo', 'project_id': 1, 'parent': {'title': 'Bar'}}}
        parent = self.redmine.wiki_page.get('Foo', project_id=1).parent
        self.assertIsInstance(parent, WikiPage)
        self.assertEqual(parent.title, 'Bar')

    def test_project_membership_version(self):
        self.assertEqual(self.redmine.project_membership.resource_class.redmine_version, '1.4')

    def test_project_membership_get(self):
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        self.assertEqual(membership.id, 1)

    def test_project_membership_filter(self):
        self.response.json.return_value = responses['project_membership']['filter']
        memberships = self.redmine.project_membership.filter(project_id=1)
        self.assertEqual(memberships[0].id, 1)
        self.assertEqual(memberships[1].id, 2)

    def test_project_membership_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.create(project_id='foo', user_id=1, role_ids=[1, 2])
        self.assertEqual(membership.id, 1)

    def test_project_membership_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.project_membership.delete(1), True)

    def test_project_membership_update(self):
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        membership.role_ids = [1, 2]
        self.assertEqual(membership.save(), True)
        self.assertEqual(membership.roles[0].id, 1)
        self.assertEqual(membership.roles[1].id, 2)

    def test_project_membership_custom_str(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(str(self.redmine.project_membership.get(1)), '1')

    def test_project_membership_custom_repr(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(repr(self.redmine.project_membership.get(1)), '<redmine.resources.ProjectMembership #1>')

    def test_project_membership_is_new(self):
        membership = self.redmine.project_membership.new()
        self.assertEqual(int(membership), 0)
        self.assertEqual(str(membership), '0')
        self.assertEqual(repr(membership), '<redmine.resources.ProjectMembership #0>')

    def test_project_membership_url(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(self.redmine.project_membership.get(1).url, '{0}/memberships/1'.format(self.url))

    def test_issue_category_version(self):
        self.assertEqual(self.redmine.issue_category.resource_class.redmine_version, '1.3')

    def test_issue_category_get(self):
        self.response.json.return_value = responses['issue_category']['get']
        issue_category = self.redmine.issue_category.get(1)
        self.assertEqual(issue_category.id, 1)
        self.assertEqual(issue_category.name, 'Foo')

    def test_issue_category_filter(self):
        self.response.json.return_value = responses['issue_category']['filter']
        categories = self.redmine.issue_category.filter(project_id=1)
        self.assertEqual(categories[0].id, 1)
        self.assertEqual(categories[0].name, 'Foo')
        self.assertEqual(categories[1].id, 2)
        self.assertEqual(categories[1].name, 'Bar')

    def test_issue_category_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['issue_category']['get']
        category = self.redmine.issue_category.create(project_id='foo', name='Foo')
        self.assertEqual(category.name, 'Foo')

    def test_issue_category_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.issue_category.delete(1), True)

    def test_issue_category_update(self):
        self.response.json.return_value = responses['issue_category']['get']
        category = self.redmine.issue_category.get(1)
        category.name = 'Bar'
        self.assertEqual(category.save(), True)

    def test_issue_category_is_new(self):
        category = self.redmine.issue_category.new()
        self.assertEqual(int(category), 0)
        self.assertEqual(str(category), '')
        self.assertEqual(repr(category), '<redmine.resources.IssueCategory #0 "">')

    def test_issue_category_url(self):
        self.response.json.return_value = responses['issue_category']['get']
        self.assertEqual(self.redmine.issue_category.get(1).url, '{0}/issue_categories/1'.format(self.url))

    def test_issue_relation_version(self):
        self.assertEqual(self.redmine.issue_relation.resource_class.redmine_version, '1.3')

    def test_issue_relation_get(self):
        self.response.json.return_value = responses['issue_relation']['get']
        relation = self.redmine.issue_relation.get(1)
        self.assertEqual(relation.id, 1)

    def test_issue_relation_filter(self):
        self.response.json.return_value = responses['issue_relation']['filter']
        relations = self.redmine.issue_relation.filter(issue_id=1)
        self.assertEqual(relations[0].id, 1)
        self.assertEqual(relations[1].id, 2)

    def test_issue_relation_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['issue_relation']['get']
        relation = self.redmine.issue_relation.create(issue_id=1, issue_to_id=2)
        self.assertEqual(relation.id, 1)

    def test_issue_relation_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.issue_relation.delete(1), True)

    def test_issue_relation_custom_str(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(str(self.redmine.issue_relation.get(1)), '1')

    def test_issue_relation_custom_repr(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(repr(self.redmine.issue_relation.get(1)), '<redmine.resources.IssueRelation #1>')

    def test_issue_relation_is_new(self):
        relation = self.redmine.issue_relation.new()
        self.assertEqual(int(relation), 0)
        self.assertEqual(str(relation), '0')
        self.assertEqual(repr(relation), '<redmine.resources.IssueRelation #0>')

    def test_issue_relation_url(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(self.redmine.issue_relation.get(1).url, '{0}/relations/1'.format(self.url))

    def test_version_version(self):
        self.assertEqual(self.redmine.version.resource_class.redmine_version, '1.3')

    def test_version_get(self):
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        self.assertEqual(version.id, 1)
        self.assertEqual(version.name, 'Foo')

    def test_version_filter(self):
        self.response.json.return_value = responses['version']['filter']
        versions = self.redmine.version.filter(project_id=1)
        self.assertEqual(versions[0].id, 1)
        self.assertEqual(versions[0].name, 'Foo')
        self.assertEqual(versions[1].id, 2)
        self.assertEqual(versions[1].name, 'Bar')

    def test_version_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.create(project_id='foo', name='Foo')
        self.assertEqual(version.name, 'Foo')

    def test_version_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.version.delete(1), True)

    def test_version_update(self):
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        version.name = 'Bar'
        self.assertEqual(version.save(), True)

    def test_version_returns_status_without_conversion(self):
        self.response.json.return_value = {'version': {'id': 1, 'name': 'Foo', 'status': 'foo'}}
        version = self.redmine.version.get(1)
        self.assertEqual(version.status, 'foo')

    def test_version_is_new(self):
        version = self.redmine.version.new()
        self.assertEqual(int(version), 0)
        self.assertEqual(str(version), '')
        self.assertEqual(repr(version), '<redmine.resources.Version #0 "">')

    def test_version_url(self):
        self.response.json.return_value = responses['version']['get']
        self.assertEqual(self.redmine.version.get(1).url, '{0}/versions/1'.format(self.url))

    def test_user_version(self):
        self.assertEqual(self.redmine.user.resource_class.redmine_version, '1.1')

    def test_user_get(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.firstname, 'John')

    def test_user_all(self):
        self.response.json.return_value = responses['user']['all']
        users = self.redmine.user.all()
        self.assertEqual(users[0].id, 1)
        self.assertEqual(users[0].firstname, 'John')
        self.assertEqual(users[1].id, 2)
        self.assertEqual(users[1].firstname, 'Jack')

    def test_user_filter(self):
        self.response.json.return_value = responses['user']['filter']
        users = self.redmine.user.filter(status_id=2)
        self.assertEqual(users[0].id, 1)
        self.assertEqual(users[0].firstname, 'John')
        self.assertEqual(users[1].id, 2)
        self.assertEqual(users[1].firstname, 'Jack')

    def test_user_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.create(firstname='John', lastname='Smith')
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.lastname, 'Smith')

    def test_user_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.user.delete(1), True)

    def test_user_update(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        user.lastname = 'Foo'
        user.firstname = 'Bar'
        self.assertEqual(user.save(), True)

    def test_user_custom_str(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(str(self.redmine.user.get(1)), 'John Smith')

    def test_user_custom_repr(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(repr(self.redmine.user.get(1)), '<redmine.resources.User #1 "John Smith">')

    def test_user_relations(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.assertIsInstance(user.issues, ResourceSet)
        self.assertIsInstance(user.time_entries, ResourceSet)
        self.assertIsInstance(user.contacts, ResourceSet)
        self.assertIsInstance(user.deals, ResourceSet)

    def test_user_includes(self):
        response_includes = responses['user']['get']
        self.response.json.return_value = response_includes
        user = self.redmine.user.get(1)
        response_includes['user']['memberships'] = responses['project_membership']['filter']['memberships']
        self.response.json.return_value = response_includes
        self.assertIsInstance(user.memberships, ResourceSet)
        response_includes['user']['groups'] = responses['group']['all']['groups']
        self.response.json.return_value = response_includes
        self.assertIsInstance(user.groups, ResourceSet)

    def test_user_returns_status_without_conversion(self):
        self.response.json.return_value = {'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1, 'status': 1}}
        user = self.redmine.user.get(1)
        self.assertEqual(user.status, 1)

    def test_user_is_new(self):
        user = self.redmine.user.new()
        self.assertEqual(int(user), 0)
        self.assertEqual(str(user), '')
        self.assertEqual(repr(user), '<redmine.resources.User #0 "">')

    def test_user_url(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(self.redmine.user.get(1).url, '{0}/users/1'.format(self.url))

    def test_group_version(self):
        self.assertEqual(self.redmine.group.resource_class.redmine_version, '2.1')

    def test_group_get(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        self.assertEqual(group.id, 1)
        self.assertEqual(group.name, 'Foo')

    def test_group_all(self):
        self.response.json.return_value = responses['group']['all']
        groups = self.redmine.group.all()
        self.assertEqual(groups[0].id, 1)
        self.assertEqual(groups[0].name, 'Foo')
        self.assertEqual(groups[1].id, 2)
        self.assertEqual(groups[1].name, 'Bar')

    def test_group_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.create(name='Foo')
        self.assertEqual(group.name, 'Foo')

    def test_group_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.group.delete(1), True)

    def test_group_update(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        group.name = 'Bar'
        self.assertEqual(group.save(), True)

    def test_group_includes(self):
        response_includes = responses['group']['get']
        self.response.json.return_value = response_includes
        group = self.redmine.group.get(1)
        response_includes['group']['memberships'] = responses['project_membership']['filter']['memberships']
        self.response.json.return_value = response_includes
        self.assertIsInstance(group.memberships, ResourceSet)
        response_includes['group']['users'] = responses['user']['all']['users']
        self.response.json.return_value = response_includes
        self.assertIsInstance(group.users, ResourceSet)

    def test_group_add_user(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        self.response.content = ''
        self.assertEqual(group.user.add(1), True)

    def test_group_remove_user(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        self.response.content = ''
        self.assertEqual(group.user.remove(1), True)

    def test_group_is_new(self):
        group = self.redmine.group.new()
        self.assertEqual(int(group), 0)
        self.assertEqual(str(group), '')
        self.assertEqual(repr(group), '<redmine.resources.Group #0 "">')

    def test_group_url(self):
        self.response.json.return_value = responses['group']['get']
        self.assertEqual(self.redmine.group.get(1).url, '{0}/groups/1'.format(self.url))

    def test_role_version(self):
        self.assertEqual(self.redmine.role.resource_class.redmine_version, '1.4')

    def test_role_get(self):
        self.response.json.return_value = responses['role']['get']
        role = self.redmine.role.get(1)
        self.assertEqual(role.id, 1)
        self.assertEqual(role.name, 'Foo')

    def test_role_all(self):
        self.response.json.return_value = responses['role']['all']
        roles = self.redmine.role.all()
        self.assertEqual(roles[0].id, 1)
        self.assertEqual(roles[0].name, 'Foo')
        self.assertEqual(roles[1].id, 2)
        self.assertEqual(roles[1].name, 'Bar')

    def test_role_url(self):
        self.response.json.return_value = responses['role']['get']
        self.assertEqual(self.redmine.role.get(1).url, '{0}/roles/1'.format(self.url))

    def test_news_version(self):
        self.assertEqual(self.redmine.news.resource_class.redmine_version, '1.1')

    def test_news_all(self):
        self.response.json.return_value = responses['news']['all']
        news = self.redmine.news.all()
        self.assertEqual(news[0].id, 1)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 2)
        self.assertEqual(news[1].title, 'Bar')

    def test_news_filter(self):
        self.response.json.return_value = responses['news']['filter']
        news = self.redmine.news.filter(project_id=1)
        self.assertEqual(news[0].id, 1)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 2)
        self.assertEqual(news[1].title, 'Bar')

    def test_news_url(self):
        self.response.json.return_value = responses['news']['filter']
        self.assertEqual(self.redmine.news.filter(project_id=1)[0].url, '{0}/news/1'.format(self.url))

    def test_news_repr(self):
        self.response.json.return_value = responses['news']['filter']
        self.assertEqual(repr(self.redmine.news.filter(project_id=1)[0]), '<redmine.resources.News #1 "Foo">')

    def test_issue_status_version(self):
        self.assertEqual(self.redmine.issue_status.resource_class.redmine_version, '1.3')

    def test_issue_status_all(self):
        self.response.json.return_value = responses['issue_status']['all']
        statuses = self.redmine.issue_status.all()
        self.assertEqual(statuses[0].id, 1)
        self.assertEqual(statuses[0].name, 'Foo')
        self.assertEqual(statuses[1].id, 2)
        self.assertEqual(statuses[1].name, 'Bar')

    def test_issue_status_url(self):
        self.response.json.return_value = responses['issue_status']['all']
        self.assertEqual(self.redmine.issue_status.all()[0].url, '{0}/issue_statuses/1/edit'.format(self.url))

    def test_tracker_version(self):
        self.assertEqual(self.redmine.tracker.resource_class.redmine_version, '1.3')

    def test_tracker_all(self):
        self.response.json.return_value = responses['tracker']['all']
        trackers = self.redmine.tracker.all()
        self.assertEqual(trackers[0].id, 1)
        self.assertEqual(trackers[0].name, 'Foo')
        self.assertEqual(trackers[1].id, 2)
        self.assertEqual(trackers[1].name, 'Bar')

    def test_tracker_url(self):
        self.response.json.return_value = responses['tracker']['all']
        self.assertEqual(self.redmine.tracker.all()[0].url, '{0}/trackers/1/edit'.format(self.url))

    def test_query_version(self):
        self.assertEqual(self.redmine.query.resource_class.redmine_version, '1.3')

    def test_query_all(self):
        self.response.json.return_value = responses['query']['all']
        queries = self.redmine.query.all()
        self.assertEqual(queries[0].id, 1)
        self.assertEqual(queries[0].name, 'Foo')
        self.assertEqual(queries[1].id, 2)
        self.assertEqual(queries[1].name, 'Bar')

    def test_query_url(self):
        self.response.json.return_value = responses['query']['all']
        self.assertEqual(self.redmine.query.all()[0].url, '{0}/projects/0/issues?query_id=1'.format(self.url))

    def test_custom_field_version(self):
        self.assertEqual(self.redmine.custom_field.resource_class.redmine_version, '2.4')

    def test_custom_field_all(self):
        self.response.json.return_value = responses['custom_field']['all']
        fields = self.redmine.custom_field.all()
        self.assertEqual(fields[0].id, 1)
        self.assertEqual(fields[0].name, 'Foo')
        self.assertEqual(fields[1].id, 2)
        self.assertEqual(fields[1].name, 'Bar')

    def test_custom_field_return_value_even_if_there_is_none(self):
        self.response.json.return_value = responses['custom_field']['all']
        fields = self.redmine.custom_field.all()
        self.assertEqual(fields[0].id, 1)
        self.assertEqual(fields[0].name, 'Foo')
        self.assertEqual(fields[0].value, '')

    def test_custom_field_returns_single_tracker_instead_of_multiple_trackers(self):
        self.response.json.return_value = {
            'custom_fields': [{'name': 'Foo', 'id': 1, 'trackers': {'tracker': {'id': 1, 'name': 'Bar'}}}]}
        fields = self.redmine.custom_field.all()
        self.assertEqual(fields[0].trackers[0].id, 1)
        self.assertEqual(fields[0].trackers[0].name, 'Bar')

    def test_custom_field_url(self):
        self.response.json.return_value = responses['custom_field']['all']
        self.assertEqual(self.redmine.custom_field.all()[0].url, '{0}/custom_fields/1/edit'.format(self.url))

    def test_contact_tag_version(self):
        self.assertEqual(self.redmine.contact_tag.resource_class.redmine_version, '2.3')

    def test_contact_tag_requirements(self):
        self.assertEqual(self.redmine.contact_tag.resource_class.requirements, (('CRM plugin', '3.4.0'),))

    def test_contact_tag_all(self):
        self.response.json.return_value = responses['contact_tag']['all']
        tags = self.redmine.contact_tag.all()
        self.assertEqual(tags[0].id, 1)
        self.assertEqual(tags[0].name, 'Foo')
        self.assertEqual(tags[1].id, 2)
        self.assertEqual(tags[1].name, 'Bar')

    def test_contact_tag_url(self):
        self.response.json.return_value = responses['contact_tag']['all']
        self.assertEqual(self.redmine.contact_tag.all()[0].url, '{0}/contacts_tags/1/edit'.format(self.url))

    def test_deal_status_version(self):
        self.assertEqual(self.redmine.deal_status.resource_class.redmine_version, '2.3')

    def test_deal_status_requirements(self):
        self.assertEqual(self.redmine.deal_status.resource_class.requirements, (('CRM plugin', '3.3.0'),))

    def test_deal_status_all(self):
        self.response.json.return_value = responses['deal_status']['all']
        statuses = self.redmine.deal_status.all()
        self.assertEqual(statuses[0].id, 1)
        self.assertEqual(statuses[0].name, 'Foo')
        self.assertEqual(statuses[1].id, 2)
        self.assertEqual(statuses[1].name, 'Bar')

    def test_deal_status_url(self):
        self.response.json.return_value = responses['deal_status']['all']
        self.assertEqual(self.redmine.deal_status.all()[0].url, '{0}/deal_statuses/1/edit'.format(self.url))

    def test_deal_category_version(self):
        self.assertEqual(self.redmine.deal_category.resource_class.redmine_version, '2.3')

    def test_deal_category_requirements(self):
        self.assertEqual(self.redmine.deal_category.resource_class.requirements, (('CRM plugin', '3.3.0'),))

    def test_deal_category_filter(self):
        self.response.json.return_value = responses['deal_category']['filter']
        categories = self.redmine.deal_category.filter(project_id=1)
        self.assertEqual(categories[0].id, 1)
        self.assertEqual(categories[0].name, 'Foo')
        self.assertEqual(categories[1].id, 2)
        self.assertEqual(categories[1].name, 'Bar')

    def test_deal_category_url(self):
        self.response.json.return_value = responses['deal_category']['filter']
        self.assertEqual(
            self.redmine.deal_category.filter(project_id=1)[0].url,
            '{0}/deal_categories/edit?id=1'.format(self.url)
        )

    def test_crm_query_version(self):
        self.assertEqual(self.redmine.crm_query.resource_class.redmine_version, '2.3')

    def test_crm_query_requirements(self):
        self.assertEqual(self.redmine.crm_query.resource_class.requirements, (('CRM plugin', '3.3.0'),))

    def test_crm_query_filter(self):
        self.response.json.return_value = responses['crm_query']['filter']
        queries = self.redmine.crm_query.filter(resource='contact')
        self.assertEqual(queries[0].id, 1)
        self.assertEqual(queries[0].name, 'Foo')
        self.assertEqual(queries[1].id, 2)
        self.assertEqual(queries[1].name, 'Bar')

    def test_crm_query_url(self):
        self.response.json.return_value = responses['crm_query']['filter']
        self.assertEqual(
            self.redmine.crm_query.filter(resource='contact')[0].url,
            '{0}/projects/0/contacts?query_id=1'.format(self.url)
        )

    def test_note_version(self):
        self.assertEqual(self.redmine.note.resource_class.redmine_version, '2.1')

    def test_note_requirements(self):
        self.assertEqual(self.redmine.note.resource_class.requirements, (('CRM plugin', '3.2.4'),))

    def test_note_get(self):
        self.response.json.return_value = responses['note']['get']
        note = self.redmine.note.get(1)
        self.assertEqual(note.id, 1)
        self.assertEqual(note.content, 'foobar')

    def test_note_source_to_resource_conversion(self):
        from redmine.resources import Contact
        self.response.json.return_value = {
            'note': {'content': 'foobar', 'id': 1, 'source': {'id': 1, 'name': 'FooBar', 'type': 'Contact'}}}
        note = self.redmine.note.get(1)
        self.assertEqual(note.source.id, 1)
        self.assertEqual(note.source.name, 'FooBar')
        self.assertIsInstance(note.source, Contact)

    def test_note_custom_str(self):
        self.response.json.return_value = responses['note']['get']
        self.assertEqual(str(self.redmine.note.get(1)), 'foobar')

    def test_note_custom_repr(self):
        self.response.json.return_value = responses['note']['get']
        self.assertEqual(repr(self.redmine.note.get(1)), '<redmine.resources.Note #1>')

    def test_contact_version(self):
        self.assertEqual(self.redmine.contact.resource_class.redmine_version, '1.2.1')

    def test_contact_get(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.assertEqual(contact.id, 1)
        self.assertEqual(contact.first_name, 'Foo')

    def test_contact_all(self):
        self.response.json.return_value = responses['contact']['all']
        contacts = self.redmine.contact.all()
        self.assertEqual(contacts[0].id, 1)
        self.assertEqual(contacts[0].first_name, 'Foo')
        self.assertEqual(contacts[1].id, 2)
        self.assertEqual(contacts[1].first_name, 'Bar')

    def test_contact_filter(self):
        self.response.json.return_value = responses['contact']['filter']
        contacts = self.redmine.contact.filter(project_id=1)
        self.assertEqual(contacts[0].id, 1)
        self.assertEqual(contacts[0].first_name, 'Foo')
        self.assertEqual(contacts[1].id, 2)
        self.assertEqual(contacts[1].first_name, 'Bar')

    def test_contact_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.create(project_id='bar', first_name='Foo')
        self.assertEqual(contact.id, 1)
        self.assertEqual(contact.first_name, 'Foo')

    def test_contact_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.contact.delete(1), True)

    def test_contact_update(self):
        self.response.json.return_value = {
            'contact': {'first_name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        contact = self.redmine.contact.get(1)
        contact.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertEqual(contact.save(), True)
        self.assertEqual(contact.custom_fields[0].value, 'bar')

    def test_contact_includes(self):
        response_includes = responses['contact']['get']
        self.response.json.return_value = response_includes
        contact = self.redmine.contact.get(1)
        response_includes['contact']['notes'] = responses['note']['get']
        self.response.json.return_value = response_includes
        self.assertIsInstance(contact.notes, ResourceSet)
        response_includes['contact']['contacts'] = responses['contact']['all']['contacts']
        self.response.json.return_value = response_includes
        self.assertIsInstance(contact.contacts, ResourceSet)
        response_includes['contact']['deals'] = responses['deal']['all']['deals']
        self.response.json.return_value = response_includes
        self.assertIsInstance(contact.deals, ResourceSet)
        response_includes['contact']['issues'] = responses['issue']['all']['issues']
        self.response.json.return_value = response_includes
        self.assertIsInstance(contact.issues, ResourceSet)

    def test_contact_add_project_raises_exception_if_wrong_version(self):
        from redmine.exceptions import ResourceVersionMismatchError
        self.response.json.return_value = responses['contact']['get']
        self.redmine.ver = '2.2.0'
        contact = self.redmine.contact.get(1)
        self.assertRaises(ResourceVersionMismatchError, lambda: contact.project.add(1))

    def test_contact_add_project(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.content = ''
        self.assertEqual(contact.project.add(1), True)

    def test_contact_add_project_raises_exceptions_if_bad_project_requested(self):
        from redmine.exceptions import ValidationError
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.status_code = 403
        self.assertRaises(ValidationError, lambda: contact.project.add(1))
        self.response.status_code = 404
        self.assertRaises(ValidationError, lambda: contact.project.add(1))

    def test_contact_remove_project(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.content = ''
        self.assertEqual(contact.project.remove(1), True)

    def test_contact_remove_project_raises_exception_if_bad_project_requested(self):
        from redmine.exceptions import ValidationError
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        self.response.status_code = 403
        self.assertRaises(ValidationError, lambda: contact.project.remove(1))
        self.response.status_code = 404
        self.assertRaises(ValidationError, lambda: contact.project.remove(1))

    def test_contact_phones_returns_as_list_of_items(self):
        self.response.json.return_value = {'contact': {'phones': [{'number': '123'}, {'number': '456'}]}}
        self.assertEqual(self.redmine.contact.get(1).phones, ['123', '456'])
        self.response.json.return_value = {'contact': {'phones': ['123', '456']}}
        self.assertEqual(self.redmine.contact.get(1).phones, ['123', '456'])

    def test_contact_emails_returns_as_list_of_items(self):
        self.response.json.return_value = {'contact': {'emails': [{'address': 'foo'}, {'address': 'bar'}]}}
        self.assertEqual(self.redmine.contact.get(1).emails, ['foo', 'bar'])
        self.response.json.return_value = {'contact': {'emails': ['foo', 'bar']}}
        self.assertEqual(self.redmine.contact.get(1).emails, ['foo', 'bar'])

    def test_contact_avatar_converts_to_resource(self):
        from redmine.resources import Attachment
        self.response.json.return_value = {'contact': {'first_name': 'Foo', 'id': 1, 'avatar': {'attachment_id': 2}}}
        avatar = self.redmine.contact.get(1).avatar
        self.assertIsInstance(avatar, Attachment)
        self.assertEqual(avatar.id, 2)

    def test_contact_sets_phones_emails_taglist_via_setattr(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        contact.phones = ['123', '456']
        contact.emails = ['foo@bar', 'bar@foo']
        contact.tag_list = ['foo', 'bar']
        self.assertEqual(contact._changes['phone'], '123,456')
        self.assertEqual(contact._changes['email'], 'foo@bar,bar@foo')
        self.assertEqual(contact._changes['tag_list'], 'foo,bar')

    def test_contact_custom_repr(self):
        self.response.json.return_value = responses['contact']['get']
        self.assertEqual(repr(self.redmine.contact.get(1)), '<redmine.resources.Contact #1 "Foo">')

    def test_contact_with_lastname_custom_repr(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        contact['_attributes']['last_name'] = 'Bar'
        self.assertEqual(repr(contact), '<redmine.resources.Contact #1 "Foo Bar">')

    def test_contact_custom_str(self):
        self.response.json.return_value = responses['contact']['get']
        self.assertEqual(str(self.redmine.contact.get(1)), 'Foo')

    def test_contact_with_lastname_custom_str(self):
        self.response.json.return_value = responses['contact']['get']
        contact = self.redmine.contact.get(1)
        contact['_attributes']['last_name'] = 'Bar'
        self.assertEqual(str(contact), 'Foo Bar')

    def test_deal_version(self):
        self.assertEqual(self.redmine.deal.resource_class.redmine_version, '1.2.1')

    def test_deal_get(self):
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.get(1)
        self.assertEqual(deal.id, 1)
        self.assertEqual(deal.name, 'Foo')

    def test_deal_all(self):
        self.response.json.return_value = responses['deal']['all']
        deals = self.redmine.deal.all()
        self.assertEqual(deals[0].id, 1)
        self.assertEqual(deals[0].name, 'Foo')
        self.assertEqual(deals[1].id, 2)
        self.assertEqual(deals[1].name, 'Bar')

    def test_deal_filter(self):
        self.response.json.return_value = responses['deal']['filter']
        deals = self.redmine.deal.filter(project_id=1)
        self.assertEqual(deals[0].id, 1)
        self.assertEqual(deals[0].name, 'Foo')
        self.assertEqual(deals[1].id, 2)
        self.assertEqual(deals[1].name, 'Bar')

    def test_deal_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.create(project_id='bar', name='Foo')
        self.assertEqual(deal.id, 1)
        self.assertEqual(deal.name, 'Foo')

    def test_deal_delete(self):
        self.response.content = ''
        self.assertEqual(self.redmine.deal.delete(1), True)

    def test_deal_update(self):
        self.response.json.return_value = {
            'deal': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        deal = self.redmine.deal.get(1)
        deal.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertEqual(deal.save(), True)
        self.assertEqual(deal.custom_fields[0].value, 'bar')

    def test_deal_includes(self):
        response_includes = responses['deal']['get']
        self.response.json.return_value = response_includes
        deal = self.redmine.deal.get(1)
        response_includes['deal']['notes'] = responses['note']['get']
        self.response.json.return_value = response_includes
        self.assertIsInstance(deal.notes, ResourceSet)

    def test_deal_category_status_converts_to_resource(self):
        from redmine.resources import DealCategory, DealStatus
        self.response.json.return_value = {'deal': {'id': 1, 'category': {'id': 2}, 'status': {'id': 3}}}
        deal = self.redmine.deal.get(1)
        self.assertIsInstance(deal.category, DealCategory)
        self.assertEqual(deal.category.id, 2)
        self.assertIsInstance(deal.status, DealStatus)
        self.assertEqual(deal.status.id, 3)

    def test_deal_custom_repr(self):
        self.response.json.return_value = responses['deal']['get']
        self.assertEqual(repr(self.redmine.deal.get(1)), '<redmine.resources.Deal #1 "Foo">')

    def test_deal_custom_repr_without_name(self):
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.get(1)
        del deal['_attributes']['name']
        self.assertEqual(repr(deal), '<redmine.resources.Deal #1>')

    def test_deal_custom_str(self):
        self.response.json.return_value = responses['deal']['get']
        self.assertEqual(str(self.redmine.deal.get(1)), 'Foo')

    def test_deal_custom_str_without_name(self):
        self.response.json.return_value = responses['deal']['get']
        deal = self.redmine.deal.get(1)
        del deal['_attributes']['name']
        self.assertEqual(str(deal), '1')
