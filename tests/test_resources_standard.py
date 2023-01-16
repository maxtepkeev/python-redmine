from . import mock, BaseRedmineTestCase
from .responses import responses

from redminelib import resources, resultsets, exceptions


class StandardResourcesTestCase(BaseRedmineTestCase):
    def test_supports_dictionary_like_attribute_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project['id'], 1)
        self.assertEqual(project['name'], 'Foo')

    def test_supports_url_retrieval(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).url, f'{self.url}/projects/foo')

    def test_supports_export_url_retrieval(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(self.redmine.issue.get(1).export_url('pdf'), f'{self.url}/issues/1.pdf')
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(self.redmine.attachment.get(1).export_url('pdf'), None)

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export(self):
        self.response.json.return_value = responses['issue']['get']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.get(1).export('txt', '/foo/bar'), '/foo/bar/1.txt')

    def test_export_not_supported_exception(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertRaises(exceptions.ExportNotSupported, lambda: self.redmine.attachment.get(1).export('pdf'))

    def test_export_format_not_supported_exception(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.response.status_code = 406
        self.assertRaises(exceptions.ExportFormatNotSupportedError, lambda: issue.export('foo'))

    def test_export_reraises_unknown_error(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.response.status_code = 999
        self.assertRaises(exceptions.UnknownError, lambda: issue.export('foo'))

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
        from datetime import date, datetime, timezone
        issue = self.redmine.issue.new()
        issue.start_date = date(2014, 3, 9)
        self.assertEqual(issue.start_date, date(2014, 3, 9))
        self.assertEqual(issue._decoded_attrs['start_date'], '2014-03-09')
        self.assertEqual(issue._changes['start_date'], '2014-03-09')
        issue.start_date = datetime(2014, 3, 9, 20, 2, 2)
        self.assertEqual(issue._decoded_attrs['start_date'], '2014-03-09T20:02:02Z')
        self.assertEqual(issue._changes['start_date'], '2014-03-09T20:02:02Z')
        self.assertEqual(issue.start_date, datetime(2014, 3, 9, 20, 2, 2))
        self.redmine.timezone = timezone.utc
        issue.start_date = datetime(2014, 3, 9, 20, 2, 2, tzinfo=datetime.strptime('+0800', '%z').tzinfo)
        self.assertEqual(issue._decoded_attrs['start_date'], '2014-03-09T12:02:02Z')
        self.assertEqual(issue._changes['start_date'], '2014-03-09T12:02:02Z')
        self.assertEqual(issue.start_date, datetime(
            2014, 3, 9, 20, 2, 2, tzinfo=datetime.strptime('+0800', '%z').tzinfo))

    def test_supports_setting_of_attributes_via_dict(self):
        project = self.redmine.project.new()
        project['name'] = 'Foo'
        project['description'] = 'Bar'
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.description, 'Bar')

    def test_setting_create_readonly_attrs_raises_exception(self):
        with self.assertRaises(exceptions.ReadonlyAttrError):
            project = self.redmine.project.new()
            project.id = 1

    def test_setting_update_readonly_attrs_raises_exception(self):
        with self.assertRaises(exceptions.ReadonlyAttrError):
            self.response.json.return_value = responses['project']['get']
            project = self.redmine.project.get(1)
            project.identifier = 1

    def test_control_raising_of_resource_attr_exception(self):
        self.response.json.return_value = responses['project']['get']
        self.redmine.raise_attr_exception = False
        self.assertEqual(self.redmine.project.get(1).foo, None)
        self.redmine.raise_attr_exception = ('Project',)
        self.assertRaises(exceptions.ResourceAttrError, lambda: self.redmine.project.get(1).foo)
        self.redmine.raise_attr_exception = True
        self.assertRaises(exceptions.ResourceAttrError, lambda: self.redmine.project.get(1).foo)

    def test_saving_new_resource_creates_it(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.new()
        project.name = 'Foo'
        self.assertIsInstance(project.save(), resources.Project)
        self.assertEqual(project.id, 1)
        project = self.redmine.project.new().save(name='Foo')
        self.assertIsInstance(project, resources.Project)
        self.assertEqual(project.id, 1)

    def test_saving_existing_resource_updates_it(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        project.name = 'Bar'
        self.assertIsInstance(project.save(), resources.Project)
        self.response.json.return_value = {'project': {'id': 1, 'name': 'Bar'}}
        project.refresh()
        self.assertEqual(project.name, 'Bar')

    def test_custom_int(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(int(self.redmine.project.get(1)), 1)

    def test_custom_str(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(str(self.redmine.project.get(1)), 'Foo')

    def test_custom_repr(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(repr(self.redmine.project.get(1)), '<redminelib.resources.Project #1 "Foo">')

    def test_can_refresh_itself(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertEqual(project.id, 1)
        self.assertEqual(project.name, 'Foo')
        self.response.json.return_value = {'project': {'id': 2, 'name': 'Bar'}}
        project.refresh()
        self.assertEqual(project.id, 2)
        self.assertEqual(project.name, 'Bar')

    def test_bulk_decode(self):
        from datetime import date, datetime
        encoded = {'start_date': date(2014, 3, 9), 'created_at': datetime(2014, 3, 9, 20, 2, 2), 'include': ['a', 'b']}
        decoded = self.redmine.project.resource_class.bulk_decode(encoded, self.redmine.project)
        self.assertEqual(decoded['start_date'], '2014-03-09')
        self.assertEqual(decoded['created_at'], '2014-03-09T20:02:02Z')
        self.assertEqual(decoded['include'], 'a,b')

    def test_bulk_encode(self):
        from datetime import date, datetime, timezone, timedelta
        decoded = {'start_date': '2014-03-09', 'created_at': '2014-03-09T20:02:02Z'}
        encoded = self.redmine.project.resource_class.bulk_encode(decoded, self.redmine.project)
        self.assertEqual(encoded['start_date'], date(2014, 3, 9))
        self.assertEqual(encoded['created_at'], datetime(2014, 3, 9, 20, 2, 2))
        self.redmine.timezone = datetime.strptime('+0800', '%z').tzinfo
        encoded = self.redmine.project.resource_class.bulk_encode(decoded, self.redmine.project)
        self.assertEqual(encoded['start_date'], date(2014, 3, 9))
        self.assertEqual(encoded['created_at'], datetime(
            2014, 3, 10, 4, 2, 2, tzinfo=timezone(timedelta(seconds=28800))))

    def test_resource_dict_is_converted_to_resource_object(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['author'] = {'id': 1, 'name': 'John Smith'}
        self.assertEqual(repr(issue.author), '<redminelib.resources.User #1 "John Smith">')

    def test_resource_list_of_dicts_is_converted_to_resource_set(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['custom_fields'] = [{'id': 1, 'name': 'Foo'}, {'id': 2, 'name': 'Bar'}]
        self.assertEqual(
            repr(issue.custom_fields),
            '<redminelib.resultsets.ResourceSet object with CustomField resources>'
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
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1}]}}
        project = self.redmine.project.get(1)
        with self.assertRaises(exceptions.CustomFieldValueError):
            project.custom_fields = 'foo'

    def test_resource_is_picklable(self):
        import pickle
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        unpickled_project = pickle.loads(pickle.dumps(project))
        self.assertEqual(project.id, unpickled_project.id)
        self.assertEqual(project.name, unpickled_project.name)

    def test_project_version(self):
        self.assertEqual(self.redmine.project.resource_class.redmine_version, (1, 0, 0))

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
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.response.content = ''
        self.assertEqual(project.delete(), True)
        self.assertEqual(self.redmine.project.delete(1), True)

    def test_project_update(self):
        self.response.json.return_value = {
            'project': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        project = self.redmine.project.get(1)
        project.homepage = 'http://foo.bar'
        project.parent_id = 3
        project.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertIsInstance(project.save(), resources.Project)
        self.assertEqual(project.custom_fields[0].value, 'bar')

    def test_project_relations(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.assertIsInstance(project.wiki_pages, resultsets.ResourceSet)
        self.assertIsInstance(project.memberships, resultsets.ResourceSet)
        self.assertIsInstance(project.issue_categories, resultsets.ResourceSet)
        self.assertIsInstance(project.time_entries, resultsets.ResourceSet)
        self.assertIsInstance(project.versions, resultsets.ResourceSet)
        self.assertIsInstance(project.news, resultsets.ResourceSet)
        self.assertIsInstance(project.issues, resultsets.ResourceSet)
        self.assertIsInstance(project.files, resultsets.ResourceSet)

    def test_project_includes(self):
        response_includes = responses['project']['get']
        self.response.json.return_value = response_includes
        project = self.redmine.project.get(1)
        response_includes['project'].update(responses['issue_category']['filter'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.issue_categories, resultsets.ResourceSet)
        response_includes['project'].update(responses['tracker']['all'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.trackers, resultsets.ResourceSet)
        response_includes['project'].update({'enabled_modules': [{'id': 36, 'name': 'issue_tracking'}]})
        self.response.json.return_value = response_includes
        self.assertEqual(project.enabled_modules, ['issue_tracking'])
        response_includes['project'].update(responses['enumeration']['filter'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.time_entry_activities, resultsets.ResourceSet)
        response_includes['project'].update(responses['custom_field']['all'])
        self.response.json.return_value = response_includes
        self.assertIsInstance(project.issue_custom_fields, resultsets.ResourceSet)

    def test_project_returns_status_without_conversion(self):
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'status': 1}}
        project = self.redmine.project.get(1)
        self.assertEqual(project.status, 1)

    def test_project_is_new(self):
        project = self.redmine.project.new()
        self.assertEqual(int(project), 0)
        self.assertEqual(str(project), '')
        self.assertEqual(repr(project), '<redminelib.resources.Project #0 "">')

    def test_project_url(self):
        self.response.json.return_value = responses['project']['get']
        self.assertEqual(self.redmine.project.get(1).url, f'{self.url}/projects/foo')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_project_export(self):
        self.response.json.return_value = responses['project']['all']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.project.all().export('txt', '/foo/bar'), '/foo/bar/projects.txt')

    def test_project_parent_converts_to_resource(self):
        self.response.json.return_value = {'project': {'name': 'Foo', 'id': 1, 'parent': {'id': 2}}}
        parent = self.redmine.project.get(1).parent
        self.assertIsInstance(parent, resources.Project)
        self.assertEqual(parent.id, 2)

    def test_project_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        project._decoded_attrs['default_version'] = {'id': 2, 'name': 'Release 4.0'}
        self.assertIsInstance(project.default_version, resources.Version)
        self.assertEqual(project.default_version.id, 2)
        project._decoded_attrs['default_assignee'] = {'id': 4, 'name': 'John Smith'}
        self.assertIsInstance(project.default_assignee, resources.User)
        self.assertEqual(project.default_assignee.id, 4)

    def test_project_supports_close_reopen_archive_unarchive(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get(1)
        self.response.content = ''
        self.assertEqual(project.close(), True)
        self.assertEqual(project.reopen(), True)
        self.assertEqual(project.archive(), True)
        self.assertEqual(project.unarchive(), True)
        self.assertEqual(self.redmine.project.close(1), True)
        self.assertEqual(self.redmine.project.reopen(1), True)
        self.assertEqual(self.redmine.project.archive(1), True)
        self.assertEqual(self.redmine.project.unarchive(1), True)
        self.redmine.ver = (4, 1, 0)
        self.assertRaises(exceptions.VersionMismatchError, lambda: project.close())
        self.assertRaises(AttributeError, lambda: project.open())

    def test_issue_version(self):
        self.assertEqual(self.redmine.issue.resource_class.redmine_version, (1, 0, 0))

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
        issue = self.redmine.issue.create(project_id='bar', subject='Foo', version_id=1, checklists=[])
        self.assertEqual(issue.id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_issue_delete(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.response.content = ''
        self.assertEqual(issue.delete(), True)
        self.assertEqual(self.redmine.issue.delete(1), True)

    def test_issue_update(self):
        self.response.json.return_value = {
            'issue': {'name': 'Foo', 'id': 1, 'custom_fields': [{'id': 1, 'value': 'foo'}]}}
        issue = self.redmine.issue.get(1)
        issue.subject = 'Foo'
        issue.description = 'foobar'
        issue.custom_fields = [{'id': 1, 'value': 'bar'}]
        self.assertIsInstance(issue.save(), resources.Issue)
        self.assertEqual(issue.custom_fields[0].value, 'bar')

    def test_issue_relations(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        self.assertIsInstance(issue.relations, resultsets.ResourceSet)
        self.assertIsInstance(issue.time_entries, resultsets.ResourceSet)

    def test_issue_includes(self):
        response_includes = responses['issue']['get']
        self.response.json.return_value = response_includes
        issue = self.redmine.issue.get(1)
        response_includes['issue']['children'] = responses['issue']['all']['issues']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.children, resultsets.ResourceSet)
        response_includes['issue']['attachments'] = responses['attachment']['get']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.attachments, resultsets.ResourceSet)
        response_includes['issue']['relations'] = responses['issue_relation']['get']['relation']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.relations, resultsets.ResourceSet)
        response_includes['issue']['journals'] = [{'id': 1}, {'id': 2}]
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.journals, resultsets.ResourceSet)
        response_includes['issue']['watchers'] = responses['user']['all']['users']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.watchers, resultsets.ResourceSet)
        response_includes['issue']['allowed_statuses'] = responses['issue_status']['all']['issue_statuses']
        self.response.json.return_value = response_includes
        self.assertIsInstance(issue.allowed_statuses, resultsets.ResourceSet)

    def test_issue_add_watcher_raises_exception_if_wrong_version(self):
        self.response.json.return_value = responses['issue']['get']
        self.redmine.ver = (2, 2, 0)
        issue = self.redmine.issue.get(1)
        self.assertRaises(exceptions.ResourceVersionMismatchError, lambda: issue.watcher.add(1))

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
        self.assertEqual(repr(self.redmine.issue.get(1)), '<redminelib.resources.Issue #1 "Foo">')

    def test_issue_custom_repr_without_subject(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        del issue['_decoded_attrs']['subject']
        self.assertEqual(repr(issue), '<redminelib.resources.Issue #1>')

    def test_issue_custom_str(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(str(self.redmine.issue.get(1)), 'Foo')

    def test_issue_custom_str_without_subject(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        del issue['_decoded_attrs']['subject']
        self.assertEqual(str(issue), '1')

    def test_issue_journals(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['journals'] = [{'id': 1}]
        self.assertEqual(str(issue.journals[0]), '1')
        self.assertEqual(repr(issue.journals[0]), '<redminelib.resources.IssueJournal #1>')

    def test_issue_journals_url(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['journals'] = [{'id': 1}]
        self.assertEqual(issue.journals[0].url, None)

    def test_issue_journals_update(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['journals'] = [{'id': 1}]
        self.response.content = ''
        self.assertIsInstance(issue.journals[0].save(notes='new value'), resources.IssueJournal)
        self.assertEqual(self.redmine.issue_journal.update(1, notes='new value'), True)

    def test_issue_journals_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['journals'] = [{'id': 1, 'user': responses['user']['get']['user']}]
        self.assertIsInstance(issue.journals[0].user, resources.User)
        self.assertEqual(issue.journals[0].user.firstname, 'John')

    def test_issue_version_can_be_retrieved_via_version_attribute(self):
        self.response.json.return_value = {
            'issue': {'subject': 'Foo', 'id': 1, 'fixed_version': {'id': 1, 'name': 'Foo'}}}
        issue = self.redmine.issue.get(1)
        self.assertIsInstance(issue.version, resources.Version)

    def test_issue_version_can_be_set_via_version_attribute(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue.version_id = 1
        self.assertEqual(issue.fixed_version.id, 1)

    def test_issue_assigned_to_id_can_be_removed_via_none(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue.assigned_to_id = None
        self.assertEqual(issue.assigned_to_id, '')

    def test_issue_assigned_to_id_can_be_removed_via_zero(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue.assigned_to_id = 0
        self.assertEqual(issue.assigned_to_id, '')

    def test_issue_is_new(self):
        issue = self.redmine.issue.new()
        self.assertEqual(int(issue), 0)
        self.assertEqual(str(issue), '')
        self.assertEqual(repr(issue), '<redminelib.resources.Issue #0 "">')

    def test_issue_url(self):
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(self.redmine.issue.get(1).url, f'{self.url}/issues/1')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_issue_export(self):
        self.response.json.return_value = responses['issue']['all']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar'), '/foo/bar/issues.txt')
        self.response.json.return_value = responses['issue']['get']
        self.assertEqual(self.redmine.issue.get(1).export('txt', '/foo/bar'), '/foo/bar/1.txt')

    def test_issue_parent_converts_to_resource(self):
        self.response.json.return_value = {'issue': {'subject': 'Foo', 'id': 1, 'parent': {'id': 2}}}
        parent = self.redmine.issue.get(1).parent
        self.assertIsInstance(parent, resources.Issue)
        self.assertEqual(parent.id, 2)

    def test_issue_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['issue']['get']
        issue = self.redmine.issue.get(1)
        issue._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(issue.project, resources.Project)
        self.assertEqual(issue.project.identifier, 'foo')
        issue._decoded_attrs['tracker'] = responses['tracker']['all']['trackers'][0]
        self.assertIsInstance(issue.tracker, resources.Tracker)
        self.assertEqual(issue.tracker.id, 1)
        issue._decoded_attrs['status'] = responses['issue_status']['all']['issue_statuses'][0]
        self.assertIsInstance(issue.status, resources.IssueStatus)
        self.assertEqual(issue.status.id, 1)
        issue._decoded_attrs['priority'] = responses['enumeration']['filter']['time_entry_activities'][0]
        self.assertIsInstance(issue.priority, resources.Enumeration)
        self.assertEqual(issue.priority.id, 1)
        issue._decoded_attrs['author'] = responses['user']['get']['user']
        self.assertIsInstance(issue.author, resources.User)
        self.assertEqual(issue.author.firstname, 'John')
        issue._decoded_attrs['assigned_to'] = responses['user']['get']['user']
        self.assertIsInstance(issue.assigned_to, resources.User)
        self.assertEqual(issue.assigned_to.lastname, 'Smith')
        issue._decoded_attrs['category'] = responses['issue_category']['get']['issue_category']
        self.assertIsInstance(issue.category, resources.IssueCategory)
        self.assertEqual(issue.category.id, 1)
        issue._decoded_attrs['fixed_version'] = responses['version']['get']['version']
        self.assertIsInstance(issue.fixed_version, resources.Version)
        self.assertEqual(issue.fixed_version.id, 1)

    def test_time_entry_version(self):
        self.assertEqual(self.redmine.time_entry.resource_class.redmine_version, (1, 1, 0))

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
        self.response.json.return_value = responses['time_entry']['get']
        time_entry = self.redmine.time_entry.get(1)
        self.response.content = ''
        self.assertEqual(time_entry.delete(), True)
        self.assertEqual(self.redmine.time_entry.delete(1), True)

    def test_time_entry_update(self):
        self.response.json.return_value = {
            'time_entry': {'hours': 2, 'id': 1, 'issue': {'id': 1}, 'activity': {'id': 1}}}
        time_entry = self.redmine.time_entry.get(1)
        time_entry.hours = 3
        time_entry.issue_id = 2
        time_entry.activity_id = 2
        self.assertIsInstance(time_entry.save(), resources.TimeEntry)

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
        self.assertEqual(repr(self.redmine.time_entry.get(1)), '<redminelib.resources.TimeEntry #1>')

    def test_time_entry_is_new(self):
        time_entry = self.redmine.time_entry.new()
        self.assertEqual(int(time_entry), 0)
        self.assertEqual(str(time_entry), '0')
        self.assertEqual(repr(time_entry), '<redminelib.resources.TimeEntry #0>')

    def test_time_entry_url(self):
        self.response.json.return_value = responses['time_entry']['get']
        self.assertEqual(self.redmine.time_entry.get(1).url, f'{self.url}/time_entries/1')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_time_entry_export(self):
        self.response.json.return_value = responses['time_entry']['all']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.time_entry.all().export('txt', '/foo/bar'), '/foo/bar/time_entries.txt')

    def test_time_entry_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['time_entry']['get']
        time_entry = self.redmine.time_entry.get(1)
        time_entry._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(time_entry.project, resources.Project)
        self.assertEqual(time_entry.project.identifier, 'foo')
        time_entry._decoded_attrs['issue'] = responses['issue']['get']['issue']
        self.assertIsInstance(time_entry.issue, resources.Issue)
        self.assertEqual(time_entry.issue.id, 1)
        time_entry._decoded_attrs['user'] = responses['user']['get']['user']
        self.assertIsInstance(time_entry.user, resources.User)
        self.assertEqual(time_entry.user.firstname, 'John')
        time_entry._decoded_attrs['activity'] = responses['enumeration']['filter']['time_entry_activities'][0]
        self.assertIsInstance(time_entry.activity, resources.Enumeration)
        self.assertEqual(time_entry.activity.id, 1)

    def test_enumeration_version(self):
        self.assertEqual(self.redmine.enumeration.resource_class.redmine_version, (2, 2, 0))

    def test_enumeration_get(self):
        self.response.json.return_value = responses['enumeration']['filter']
        enumeration = self.redmine.enumeration.get(1, resource='time_entry_activities')
        self.assertEqual(enumeration.id, 1)
        self.assertEqual(enumeration.name, 'Foo')

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
            f'{self.url}/enumerations/1/edit'
        )

    def test_attachment_version(self):
        self.assertEqual(self.redmine.attachment.resource_class.redmine_version, (1, 3, 0))

    def test_attachment_get(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        self.assertEqual(attachment.id, 1)
        self.assertEqual(attachment.filename, 'foo.jpg')

    def test_attachment_update(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        attachment.filename = 'bar.jpg'
        self.assertIsInstance(attachment.save(), resources.Attachment)

    def test_attachment_delete(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        self.response.content = ''
        self.assertEqual(attachment.delete(), True)
        self.assertEqual(self.redmine.attachment.delete(1), True)

    def test_attachment_custom_str(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(str(self.redmine.attachment.get(1)), 'foo.jpg')

    def test_attachment_custom_str_without_filename(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        del attachment['_decoded_attrs']['filename']
        self.assertEqual(str(attachment), '1')

    def test_attachment_custom_repr(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(repr(self.redmine.attachment.get(1)), '<redminelib.resources.Attachment #1 "foo.jpg">')

    def test_attachment_custom_repr_without_subject(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        del attachment['_decoded_attrs']['filename']
        self.assertEqual(repr(attachment), '<redminelib.resources.Attachment #1>')

    def test_attachment_url(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(self.redmine.attachment.get(1).url, f'{self.url}/attachments/1')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_attachment_download(self):
        response = responses['attachment']['get']
        response['attachment']['content_url'] = 'http://foo/bar.txt'
        self.response.json.return_value = response
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.attachment.get(1).download('/some/path'), '/some/path/bar.txt')

    def test_attachment_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['attachment']['get']
        attachment = self.redmine.attachment.get(1)
        attachment._decoded_attrs['author'] = responses['user']['get']['user']
        self.assertIsInstance(attachment.author, resources.User)
        self.assertEqual(attachment.author.firstname, 'John')

    def test_file_version(self):
        self.assertEqual(self.redmine.file.resource_class.redmine_version, (3, 4, 0))

    def test_file_get(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        self.assertEqual(f.id, 1)
        self.assertEqual(f.filename, 'foo.jpg')

    def test_file_filter(self):
        self.response.json.return_value = responses['file']['filter']
        files = self.redmine.file.filter(project_id=1)
        self.assertEqual(files[0].id, 1)
        self.assertEqual(files[0].filename, 'foo.jpg')
        self.assertEqual(files[1].id, 2)
        self.assertEqual(files[1].filename, 'bar.jpg')

    @mock.patch('os.path.isfile', mock.Mock())
    @mock.patch('os.path.getsize', mock.Mock())
    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_file_create(self):
        self.set_patch_side_effect([
            mock.Mock(status_code=201, history=[], **{'json.return_value': {'upload': {'id': 1, 'token': '1.1234'}}}),
            mock.Mock(status_code=200, history=[], content='')
        ])
        f = self.redmine.file.create(project_id=1, filename='foo.jpg', path='foo', return_complete=False)
        self.assertEqual(f.id, 1)
        self.assertRaises(exceptions.ResourceAttrError, lambda: f.filename)

    def test_file_update(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        f.filename = 'bar.jpg'
        self.assertIsInstance(f.save(), resources.File)

    def test_file_delete(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        self.response.content = ''
        self.assertEqual(f.delete(), True)
        self.assertEqual(self.redmine.file.delete(1), True)

    def test_file_custom_str(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(str(self.redmine.file.get(1)), 'foo.jpg')

    def test_file_custom_str_without_filename(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        del f['_decoded_attrs']['filename']
        self.assertEqual(str(f), '1')

    def test_file_custom_repr(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(repr(self.redmine.file.get(1)), '<redminelib.resources.File #1 "foo.jpg">')

    def test_file_custom_repr_without_subject(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        del f['_decoded_attrs']['filename']
        self.assertEqual(repr(f), '<redminelib.resources.File #1>')

    def test_file_url(self):
        self.response.json.return_value = responses['attachment']['get']
        self.assertEqual(self.redmine.file.get(1).url, f'{self.url}/attachments/1')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_file_download(self):
        response = responses['attachment']['get']
        response['attachment']['content_url'] = 'http://foo/bar.txt'
        self.response.json.return_value = response
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.file.get(1).download('/some/path'), '/some/path/bar.txt')

    def test_file_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['attachment']['get']
        f = self.redmine.file.get(1)
        f._decoded_attrs['author'] = responses['user']['get']['user']
        self.assertIsInstance(f.author, resources.User)
        self.assertEqual(f.author.firstname, 'John')
        f._decoded_attrs['version'] = responses['version']['get']['version']
        self.assertIsInstance(f.version, resources.Version)
        self.assertEqual(f.version.id, 1)

    def test_wiki_page_version(self):
        self.assertEqual(self.redmine.wiki_page.resource_class.redmine_version, (2, 2, 0))

    def test_wiki_page_get(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.assertEqual(wiki_page.title, 'Foo')

    def test_wiki_page_get_special(self):
        """Test getting a wiki page with special char in title."""
        self.response.json.return_value = responses['wiki_page']['get_special']
        wiki_page = self.redmine.wiki_page.get('Foo%Bar', project_id=1)
        self.assertEqual(self.patch_requests.call_args[0][1], f'{self.url}/projects/1/wiki/Foo%25Bar.json')
        self.assertEqual(wiki_page.title, 'Foo%Bar')
        self.assertEqual(wiki_page.url, 'http://foo.bar/projects/1/wiki/Foo%25Bar')

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

    def test_wiki_page_create_special(self):
        """Test creating a wiki page with special char in title."""
        self.response.status_code = 201
        self.response.json.return_value = responses['wiki_page']['get_special']
        wiki_page = self.redmine.wiki_page.create(project_id='foo', title='Foo%Bar')
        self.assertEqual(self.patch_requests.call_args[0][1], f'{self.url}/projects/foo/wiki/Foo%25Bar.json')
        self.assertEqual(wiki_page.title, 'Foo%Bar')

    def test_wiki_page_delete(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.response.content = ''
        self.assertEqual(wiki_page.delete(), True)
        self.assertEqual(self.redmine.wiki_page.delete('Foo', project_id=1), True)

    def test_wiki_page_update(self):
        self.response.json.return_value = \
            {'wiki_page': {'title': 'Foo', 'version': 1, 'created_on': '2012-06-27T12:48:15Z'}}
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        wiki_page.text = 'Foo'
        self.assertIsInstance(wiki_page.save(), resources.WikiPage)
        self.assertEqual(wiki_page.version, 2)

    def test_wiki_page_refresh_by_title(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        self.assertEqual(wiki_page.title, 'Foo')
        self.response.json.return_value = {'wiki_page': {'title': 'Bar'}}
        wiki_page.refresh()
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
        self.assertEqual(repr(self.redmine.wiki_page.get('Foo', project_id=1)), '<redminelib.resources.WikiPage "Foo">')

    def test_wiki_page_includes(self):
        response_includes = responses['wiki_page']['get']
        self.response.json.return_value = response_includes
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        response_includes['wiki_page']['attachments'] = responses['attachment']['get']['attachment']
        self.response.json.return_value = response_includes
        self.assertIsInstance(wiki_page.attachments, resultsets.ResourceSet)

    def test_wiki_page_is_new(self):
        wiki_page = self.redmine.wiki_page.new()
        self.assertEqual(int(wiki_page), 0)
        self.assertEqual(str(wiki_page), '')
        self.assertEqual(repr(wiki_page), '<redminelib.resources.WikiPage "">')

    def test_wiki_page_url(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.assertEqual(self.redmine.wiki_page.get('Foo', project_id='Foo').url, f'{self.url}/projects/Foo/wiki/Foo')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_wiki_page_export(self):
        self.response.json.return_value = responses['wiki_page']['get']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.wiki_page.get('Foo', project_id='Foo').export('txt', '/foo'), '/foo/Foo.txt')

    def test_wiki_page_parent_converts_to_resource(self):
        self.response.json.return_value = {'wiki_page': {'title': 'Foo', 'project_id': 1, 'parent': {'title': 'Bar'}}}
        parent = self.redmine.wiki_page.get('Foo', project_id=1).parent
        self.assertIsInstance(parent, resources.WikiPage)
        self.assertEqual(parent.title, 'Bar')

    def test_wiki_page_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['wiki_page']['get']
        wiki_page = self.redmine.wiki_page.get('Foo', project_id=1)
        wiki_page._decoded_attrs['author'] = responses['user']['get']['user']
        self.assertIsInstance(wiki_page.author, resources.User)
        self.assertEqual(wiki_page.author.firstname, 'John')

    def test_project_membership_version(self):
        self.assertEqual(self.redmine.project_membership.resource_class.redmine_version, (1, 4, 0))

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
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        self.response.content = ''
        self.assertEqual(membership.delete(), True)
        self.assertEqual(self.redmine.project_membership.delete(1), True)

    def test_project_membership_update(self):
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        membership.role_ids = [1, 2]
        self.assertIsInstance(membership.save(), resources.ProjectMembership)
        self.assertEqual(membership.roles[0].id, 1)
        self.assertEqual(membership.roles[1].id, 2)

    def test_project_membership_custom_str(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(str(self.redmine.project_membership.get(1)), '1')

    def test_project_membership_custom_repr(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(repr(self.redmine.project_membership.get(1)), '<redminelib.resources.ProjectMembership #1>')

    def test_project_membership_is_new(self):
        membership = self.redmine.project_membership.new()
        self.assertEqual(int(membership), 0)
        self.assertEqual(str(membership), '0')
        self.assertEqual(repr(membership), '<redminelib.resources.ProjectMembership #0>')

    def test_project_membership_url(self):
        self.response.json.return_value = responses['project_membership']['get']
        self.assertEqual(self.redmine.project_membership.get(1).url, f'{self.url}/memberships/1')

    def test_project_membership_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['project_membership']['get']
        membership = self.redmine.project_membership.get(1)
        membership._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(membership.project, resources.Project)
        self.assertEqual(membership.project.identifier, 'foo')
        membership._decoded_attrs['user'] = responses['user']['get']['user']
        self.assertIsInstance(membership.user, resources.User)
        self.assertEqual(membership.user.firstname, 'John')
        membership._decoded_attrs['group'] = responses['group']['get']['group']
        self.assertIsInstance(membership.group, resources.Group)
        self.assertEqual(membership.group.id, 1)

    def test_issue_category_version(self):
        self.assertEqual(self.redmine.issue_category.resource_class.redmine_version, (1, 3, 0))

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
        self.response.json.return_value = responses['issue_category']['get']
        category = self.redmine.issue_category.get(1)
        self.response.content = ''
        self.assertEqual(category.delete(), True)
        self.assertEqual(self.redmine.issue_category.delete(1), True)

    def test_issue_category_update(self):
        self.response.json.return_value = responses['issue_category']['get']
        category = self.redmine.issue_category.get(1)
        category.name = 'Bar'
        self.assertIsInstance(category.save(), resources.IssueCategory)

    def test_issue_category_is_new(self):
        category = self.redmine.issue_category.new()
        self.assertEqual(int(category), 0)
        self.assertEqual(str(category), '')
        self.assertEqual(repr(category), '<redminelib.resources.IssueCategory #0 "">')

    def test_issue_category_url(self):
        self.response.json.return_value = responses['issue_category']['get']
        self.assertEqual(self.redmine.issue_category.get(1).url, f'{self.url}/issue_categories/1')

    def test_issue_category_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['issue_category']['get']
        category = self.redmine.issue_category.get(1)
        category._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(category.project, resources.Project)
        self.assertEqual(category.project.identifier, 'foo')
        category._decoded_attrs['assigned_to'] = responses['user']['get']['user']
        self.assertIsInstance(category.assigned_to, resources.User)
        self.assertEqual(category.assigned_to.firstname, 'John')

    def test_issue_relation_version(self):
        self.assertEqual(self.redmine.issue_relation.resource_class.redmine_version, (1, 3, 0))

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
        self.response.json.return_value = responses['issue_relation']['get']
        relation = self.redmine.issue_relation.get(1)
        self.response.content = ''
        self.assertEqual(relation.delete(), True)
        self.assertEqual(self.redmine.issue_relation.delete(1), True)

    def test_issue_relation_custom_str(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(str(self.redmine.issue_relation.get(1)), '1')

    def test_issue_relation_custom_repr(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(repr(self.redmine.issue_relation.get(1)), '<redminelib.resources.IssueRelation #1>')

    def test_issue_relation_is_new(self):
        relation = self.redmine.issue_relation.new()
        self.assertEqual(int(relation), 0)
        self.assertEqual(str(relation), '0')
        self.assertEqual(repr(relation), '<redminelib.resources.IssueRelation #0>')

    def test_issue_relation_url(self):
        self.response.json.return_value = responses['issue_relation']['get']
        self.assertEqual(self.redmine.issue_relation.get(1).url, f'{self.url}/relations/1')

    def test_version_version(self):
        self.assertEqual(self.redmine.version.resource_class.redmine_version, (1, 3, 0))

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
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        self.response.content = ''
        self.assertEqual(version.delete(), True)
        self.assertEqual(self.redmine.version.delete(1), True)

    def test_version_update(self):
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        version.name = 'Bar'
        self.assertIsInstance(version.save(), resources.Version)

    def test_version_returns_status_without_conversion(self):
        self.response.json.return_value = {'version': {'id': 1, 'name': 'Foo', 'status': 'foo'}}
        version = self.redmine.version.get(1)
        self.assertEqual(version.status, 'foo')

    def test_version_is_new(self):
        version = self.redmine.version.new()
        self.assertEqual(int(version), 0)
        self.assertEqual(str(version), '')
        self.assertEqual(repr(version), '<redminelib.resources.Version #0 "">')

    def test_version_url(self):
        self.response.json.return_value = responses['version']['get']
        self.assertEqual(self.redmine.version.get(1).url, f'{self.url}/versions/1')

    def test_version_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['version']['get']
        version = self.redmine.version.get(1)
        version._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(version.project, resources.Project)
        self.assertEqual(version.project.identifier, 'foo')

    def test_user_version(self):
        self.assertEqual(self.redmine.user.resource_class.redmine_version, (1, 1, 0))

    def test_user_get(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.assertEqual(user.id, 1)
        self.assertEqual(user.firstname, 'John')

    def test_user_get_account(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get('me')
        self.assertEqual(user.firstname, 'John')
        self.assertTrue(self.patch_requests.call_args[0][1].endswith('/my/account.json'))

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

    def test_user_create_with_send_information(self):
        import json
        self.response.status_code = 201
        self.response.json.return_value = responses['user']['get']
        self.redmine.user.create(firstname='John', lastname='Smith', send_information=True)
        self.assertEqual(json.loads(self.patch_requests.call_args[1]['data'])['send_information'], True)

    def test_user_delete(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.response.content = ''
        self.assertEqual(user.delete(), True)
        self.assertEqual(self.redmine.user.delete(1), True)

    def test_user_update(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        user.lastname = 'Foo'
        user.firstname = 'Bar'
        self.assertIsInstance(user.save(), resources.User)

    def test_user_update_account(self):
        self.redmine.user.update('me', lastname='Foo', firstname='Bar')
        self.assertTrue(self.patch_requests.call_args[0][1].endswith('/my/account.json'))

    def test_user_update_with_send_information(self):
        import json
        self.response.json.return_value = responses['user']['get']
        self.redmine.user.update(1, firstname='John', lastname='Smith', send_information=True)
        self.assertEqual(json.loads(self.patch_requests.call_args[1]['data'])['send_information'], True)

    def test_user_custom_str(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(str(self.redmine.user.get(1)), 'John Smith')

    def test_user_custom_repr(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(repr(self.redmine.user.get(1)), '<redminelib.resources.User #1 "John Smith">')

    def test_user_relations(self):
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.get(1)
        self.assertIsInstance(user.issues, resultsets.ResourceSet)
        self.assertIsInstance(user.time_entries, resultsets.ResourceSet)

    def test_user_includes(self):
        response_includes = responses['user']['get']
        self.response.json.return_value = response_includes
        user = self.redmine.user.get(1)
        response_includes['user']['memberships'] = responses['project_membership']['filter']['memberships']
        self.response.json.return_value = response_includes
        self.assertIsInstance(user.memberships, resultsets.ResourceSet)
        response_includes['user']['groups'] = responses['group']['all']['groups']
        self.response.json.return_value = response_includes
        self.assertIsInstance(user.groups, resultsets.ResourceSet)

    def test_user_returns_status_without_conversion(self):
        self.response.json.return_value = {'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1, 'status': 1}}
        user = self.redmine.user.get(1)
        self.assertEqual(user.status, 1)

    def test_user_is_new(self):
        user = self.redmine.user.new()
        self.assertEqual(int(user), 0)
        self.assertEqual(str(user), '')
        self.assertEqual(repr(user), '<redminelib.resources.User #0 "">')

    def test_user_url(self):
        self.response.json.return_value = responses['user']['get']
        self.assertEqual(self.redmine.user.get(1).url, f'{self.url}/users/1')

    def test_group_version(self):
        self.assertEqual(self.redmine.group.resource_class.redmine_version, (2, 1, 0))

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
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        self.response.content = ''
        self.assertEqual(group.delete(), True)
        self.assertEqual(self.redmine.group.delete(1), True)

    def test_group_update(self):
        self.response.json.return_value = responses['group']['get']
        group = self.redmine.group.get(1)
        group.name = 'Bar'
        self.assertIsInstance(group.save(), resources.Group)

    def test_group_includes(self):
        response_includes = responses['group']['get']
        self.response.json.return_value = response_includes
        group = self.redmine.group.get(1)
        response_includes['group']['memberships'] = responses['project_membership']['filter']['memberships']
        self.response.json.return_value = response_includes
        self.assertIsInstance(group.memberships, resultsets.ResourceSet)
        response_includes['group']['users'] = responses['user']['all']['users']
        self.response.json.return_value = response_includes
        self.assertIsInstance(group.users, resultsets.ResourceSet)

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
        self.assertEqual(repr(group), '<redminelib.resources.Group #0 "">')

    def test_group_url(self):
        self.response.json.return_value = responses['group']['get']
        self.assertEqual(self.redmine.group.get(1).url, f'{self.url}/groups/1')

    def test_role_version(self):
        self.assertEqual(self.redmine.role.resource_class.redmine_version, (1, 4, 0))

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
        self.assertEqual(self.redmine.role.get(1).url, f'{self.url}/roles/1')

    def test_news_version(self):
        self.assertEqual(self.redmine.news.resource_class.redmine_version, (1, 1, 0))

    def test_news_get(self):
        self.response.json.return_value = responses['news']['get']
        news = self.redmine.news.get(1)
        self.assertEqual(news.id, 1)
        self.assertEqual(news.title, 'Foo')

    def test_news_all(self):
        self.response.json.return_value = responses['news']['all']
        news = self.redmine.news.all()
        self.assertEqual(news[0].id, 2)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 1)
        self.assertEqual(news[1].title, 'Bar')

    def test_news_filter(self):
        self.response.json.return_value = responses['news']['filter']
        news = self.redmine.news.filter(project_id=1)
        self.assertEqual(news[0].id, 2)
        self.assertEqual(news[0].title, 'Foo')
        self.assertEqual(news[1].id, 1)
        self.assertEqual(news[1].title, 'Bar')

    def test_news_create(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['news']['get']
        news = self.redmine.news.create(project_id=1, title='Foo')
        self.assertEqual(news.title, 'Foo')

    def test_news_create_empty_response(self):
        self.set_patch_side_effect([
            mock.Mock(status_code=204, history=[], content=''),
            mock.Mock(status_code=201, history=[], **{'json.return_value': responses['news']['filter']})
        ])
        news = self.redmine.news.create(project_id=1, title='Foo')
        self.assertEqual(news.title, 'Foo')

    def test_news_delete(self):
        self.response.json.return_value = responses['news']['get']
        news = self.redmine.news.get(1)
        self.response.content = ''
        self.assertEqual(news.delete(), True)
        self.assertEqual(self.redmine.news.delete(1), True)

    def test_news_update(self):
        self.response.json.return_value = responses['news']['get']
        news = self.redmine.news.get(1)
        news.title = 'Bar'
        self.assertIsInstance(news.save(), resources.News)

    def test_news_url(self):
        self.response.json.return_value = responses['news']['filter']
        self.assertEqual(self.redmine.news.filter(project_id=1)[0].url, f'{self.url}/news/2')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_news_export(self):
        self.response.json.return_value = responses['news']['all']
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.news.all().export('txt', '/foo/bar'), '/foo/bar/news.txt')

    def test_news_str(self):
        self.response.json.return_value = responses['news']['filter']
        self.assertEqual(str(self.redmine.news.filter(project_id=1)[0]), 'Foo')

    def test_news_repr(self):
        self.response.json.return_value = responses['news']['filter']
        self.assertEqual(repr(self.redmine.news.filter(project_id=1)[0]), '<redminelib.resources.News #2 "Foo">')

    def test_news_resource_map_converts_to_resource(self):
        self.response.json.return_value = responses['news']['get']
        news = self.redmine.news.get(1)
        news._decoded_attrs['project'] = responses['project']['get']['project']
        self.assertIsInstance(news.project, resources.Project)
        self.assertEqual(news.project.identifier, 'foo')
        news._decoded_attrs['author'] = responses['user']['get']['user']
        self.assertIsInstance(news.author, resources.User)
        self.assertEqual(news.author.firstname, 'John')

    def test_news_includes(self):
        response_includes = responses['news']['get']
        self.response.json.return_value = response_includes
        news = self.redmine.news.get(1)
        response_includes['news'].update({'attachments': [responses['attachment']['get']['attachment']]})
        self.response.json.return_value = response_includes
        self.assertIsInstance(news.attachments, resultsets.ResourceSet)
        response_includes['news'].update({'comments': [{'id': 1, 'content': 'foobar'}]})
        self.response.json.return_value = response_includes
        self.assertIsInstance(news.comments, list)

    def test_issue_status_version(self):
        self.assertEqual(self.redmine.issue_status.resource_class.redmine_version, (1, 3, 0))

    def test_issue_status_get(self):
        self.response.json.return_value = responses['issue_status']['all']
        status = self.redmine.issue_status.get(1)
        self.assertEqual(status.id, 1)
        self.assertEqual(status.name, 'Foo')

    def test_issue_status_all(self):
        self.response.json.return_value = responses['issue_status']['all']
        statuses = self.redmine.issue_status.all()
        self.assertEqual(statuses[0].id, 1)
        self.assertEqual(statuses[0].name, 'Foo')
        self.assertEqual(statuses[1].id, 2)
        self.assertEqual(statuses[1].name, 'Bar')

    def test_issue_status_url(self):
        self.response.json.return_value = responses['issue_status']['all']
        self.assertEqual(self.redmine.issue_status.all()[0].url, f'{self.url}/issue_statuses/1/edit')

    def test_tracker_version(self):
        self.assertEqual(self.redmine.tracker.resource_class.redmine_version, (1, 3, 0))

    def test_tracker_get(self):
        self.response.json.return_value = responses['tracker']['all']
        tracker = self.redmine.tracker.get(1)
        self.assertEqual(tracker.id, 1)
        self.assertEqual(tracker.name, 'Foo')

    def test_tracker_all(self):
        self.response.json.return_value = responses['tracker']['all']
        trackers = self.redmine.tracker.all()
        self.assertEqual(trackers[0].id, 1)
        self.assertEqual(trackers[0].name, 'Foo')
        self.assertEqual(trackers[1].id, 2)
        self.assertEqual(trackers[1].name, 'Bar')

    def test_tracker_url(self):
        self.response.json.return_value = responses['tracker']['all']
        self.assertEqual(self.redmine.tracker.all()[0].url, f'{self.url}/trackers/1/edit')

    def test_query_version(self):
        self.assertEqual(self.redmine.query.resource_class.redmine_version, (1, 3, 0))

    def test_query_get(self):
        self.response.json.return_value = responses['query']['all']
        query = self.redmine.query.get(1)
        self.assertEqual(query.id, 1)
        self.assertEqual(query.name, 'Foo')

    def test_query_all(self):
        self.response.json.return_value = responses['query']['all']
        queries = self.redmine.query.all()
        self.assertEqual(queries[0].id, 1)
        self.assertEqual(queries[0].name, 'Foo')
        self.assertEqual(queries[1].id, 2)
        self.assertEqual(queries[1].name, 'Bar')

    def test_query_url(self):
        self.response.json.return_value = responses['query']['all']
        self.assertEqual(self.redmine.query.all()[0].url, f'{self.url}/projects/0/issues?query_id=1')

    def test_custom_field_version(self):
        self.assertEqual(self.redmine.custom_field.resource_class.redmine_version, (2, 4, 0))

    def test_custom_field_get(self):
        self.response.json.return_value = responses['custom_field']['all']
        field = self.redmine.custom_field.get(1)
        self.assertEqual(field.id, 1)
        self.assertEqual(field.name, 'Foo')

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
        self.assertEqual(self.redmine.custom_field.all()[0].url, f'{self.url}/custom_fields/1/edit')
