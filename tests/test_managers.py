import warnings

from . import mock, BaseRedmineTestCase
from .responses import responses

from redminelib import managers, resources, resultsets, exceptions


class FooResource(resources.Project):
    pass


class ResourceManagerTestCase(BaseRedmineTestCase):
    def test_has_custom_repr(self):
        self.assertEqual(repr(self.redmine.issue), '<redminelib.managers.ResourceManager object for Issue resource>')

    def test_supports_additional_resources(self):
        self.assertIsInstance(self.redmine.foo_resource, managers.ResourceManager)

    def test_not_supported_resource_exception(self):
        self.assertRaises(exceptions.ResourceError, lambda: self.redmine.foobar)

    def test_not_supported_version_exception(self):
        self.redmine.ver = '0.0.1'
        self.assertRaises(exceptions.ResourceVersionMismatchError, lambda: self.redmine.project)

    def test_convert_dict_to_resource_object(self):
        project = self.redmine.project.to_resource(responses['project']['get']['project'])
        self.assertIsInstance(project, resources.Project)
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.identifier, 'foo')
        self.assertEqual(project.id, 1)

    def test_convert_dicts_to_resource_set_object(self):
        resourceset = self.redmine.project.to_resource_set([
            {'name': 'Foo', 'identifier': 'foo', 'id': 1},
            {'name': 'Bar', 'identifier': 'bar', 'id': 2}
        ])
        self.assertIsInstance(resourceset, resultsets.ResourceSet)
        self.assertEqual(resourceset[0].name, 'Foo')
        self.assertEqual(resourceset[0].identifier, 'foo')
        self.assertEqual(resourceset[0].id, 1)
        self.assertEqual(resourceset[1].name, 'Bar')
        self.assertEqual(resourceset[1].identifier, 'bar')
        self.assertEqual(resourceset[1].id, 2)

    def test_get_single_resource(self):
        self.response.json.return_value = responses['project']['get']
        project = self.redmine.project.get('foo')
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.identifier, 'foo')
        self.assertEqual(project.id, 1)

    def test_get_single_resource_via_all(self):
        self.response.json.return_value = responses['tracker']['all']
        tracker = self.redmine.tracker.get(1)
        self.assertEqual(tracker.id, 1)
        self.assertEqual(tracker.name, 'Foo')

    def test_get_single_resource_via_filter(self):
        self.response.json.return_value = responses['enumeration']['filter']
        enumeration = self.redmine.enumeration.get(1, resource='time_entry_activities')
        self.assertEqual(enumeration.id, 1)
        self.assertEqual(enumeration.name, 'Foo')

    def test_get_unicode_resource(self):
        unicode_name = b'\xcf\x86oo'.decode('utf-8')
        self.response.json.return_value = {'project': {'name': unicode_name, 'identifier': unicode_name, 'id': 1}}
        project = self.redmine.project.get(unicode_name)
        self.assertEqual(project.name, unicode_name)
        self.assertEqual(project.identifier, unicode_name)
        self.assertEqual(project.id, 1)

    def test_get_all_resources(self):
        self.assertIsInstance(self.redmine.project.all(), resultsets.ResourceSet)

    def test_get_filtered_resources(self):
        self.assertIsInstance(self.redmine.issue.filter(project_id='foo'), resultsets.ResourceSet)

    def test_decode_params(self):
        from datetime import date, datetime
        time_entries = self.redmine.time_entry.filter(from_date=date(2014, 3, 9), to_date=date(2014, 3, 10))
        self.assertEqual(time_entries.manager.params['from'], '2014-03-09')
        self.assertEqual(time_entries.manager.params['to'], '2014-03-10')
        time_entries = self.redmine.time_entry.filter(from_date=datetime(2014, 3, 9), to_date=datetime(2014, 3, 10))
        self.assertEqual(time_entries.manager.params['from'], '2014-03-09T00:00:00Z')
        self.assertEqual(time_entries.manager.params['to'], '2014-03-10T00:00:00Z')

    def test_create_resource(self):
        self.response.status_code = 201
        self.response.json.return_value = responses['user']['get']
        user = self.redmine.user.create(firstname='John', lastname='Smith')
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.lastname, 'Smith')

    def test_create_unicode_resource(self):
        unicode_name = b'\xcf\x86oo'.decode('utf-8')
        self.response.status_code = 201
        self.response.json.return_value = {'wiki_page': {'title': unicode_name, 'project_id': 1}}
        wiki_page = self.redmine.wiki_page.create(title=unicode_name, project_id=1)
        self.assertEqual(wiki_page.title, unicode_name)
        self.assertEqual(wiki_page.project_id, 1)

    @mock.patch('os.path.isfile', mock.Mock())
    @mock.patch('os.path.getsize', mock.Mock())
    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_create_resource_with_uploads(self):
        self.response.status_code = 201
        self.response.json.return_value = {
            'upload': {'id': 1, 'token': '123456'},
            'issue': {'subject': 'Foo', 'project_id': 1, 'id': 1}
        }
        issue = self.redmine.issue.create(project_id=1, subject='Foo', uploads=[{'path': 'foo'}])
        self.assertEqual(issue.project_id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_create_resource_with_stream_uploads(self):
        from io import StringIO
        self.response.status_code = 201
        self.response.json.return_value = {
            'upload': {'id': 1, 'token': '123456'},
            'issue': {'subject': 'Foo', 'project_id': 1, 'id': 1}
        }
        stream = StringIO(b'\xcf\x86oo'.decode('utf-8'))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            issue = self.redmine.issue.create(project_id=1, subject='Foo', uploads=[{'path': stream}])
            self.assertEquals(len(w), 1)
            self.assertIs(w[0].category, exceptions.PerformanceWarning)
        self.assertEqual(issue.project_id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_create_empty_resource(self):
        project = self.redmine.project.new()
        defaults = dict.fromkeys(project._includes + project._relations)
        self.assertEqual(project._decoded_attrs, defaults)
        self.assertEqual(repr(project), '<redminelib.resources.Project #0 "">')

    def test_create_resource_returns_none(self):
        with self.redmine.session(return_response=False):
            self.assertEqual(self.redmine.user.create(firstname='John', lastname='Smith'), None)

    def test_update_resource(self):
        self.response.content = ''
        manager = self.redmine.wiki_page
        manager.params['project_id'] = 1
        self.assertEqual(manager.update(b'\xcf\x86oo'.decode('utf-8'), title='Bar'), True)

    @mock.patch('os.path.isfile', mock.Mock())
    @mock.patch('os.path.getsize', mock.Mock())
    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_update_resource_with_uploads(self):
        self.set_patch_side_effect([
            mock.Mock(status_code=201, history=[], **{'json.return_value': {'upload': {'id': 1, 'token': '123456'}}}),
            mock.Mock(status_code=200, history=[], content='')
        ])
        self.assertEqual(self.redmine.issue.update(1, subject='Bar', uploads=[{'path': 'foo'}]), True)

    def test_update_resource_with_stream_uploads(self):
        from io import StringIO
        self.set_patch_side_effect([
            mock.Mock(status_code=201, history=[], **{'json.return_value': {'upload': {'id': 1, 'token': '123456'}}}),
            mock.Mock(status_code=200, history=[], content='')
        ])
        stream = StringIO(b'\xcf\x86oo'.decode('utf-8'))
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always')
            self.assertEqual(self.redmine.issue.update(1, subject='Bar', uploads=[{'path': stream}]), True)
            self.assertEquals(len(w), 1)
            self.assertIs(w[0].category, exceptions.PerformanceWarning)

    def test_update_resource_returns_none(self):
        with self.redmine.session(return_response=False):
            self.assertEqual(self.redmine.issue.update(1, subject='Bar'), None)

    def test_delete_resource(self):
        self.response.content = ''
        self.assertEqual(self.redmine.wiki_page.delete(b'\xcf\x86oo'.decode('utf-8'), project_id=1), True)

    def test_delete_resource_returns_204(self):
        self.response.status_code = 204
        self.response.content = ''
        self.assertEqual(self.redmine.wiki_page.delete(b'\xcf\x86oo'.decode('utf-8'), project_id=1), True)

    def test_delete_resource_returns_none(self):
        with self.redmine.session(return_response=False):
            self.assertEqual(self.redmine.user.delete(1), None)

    def test_resource_get_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.issue_journal.get(1))

    def test_resource_all_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.attachment.all())

    def test_resource_filter_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.project.filter())

    def test_resource_create_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.query.create())

    def test_resource_update_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.query.update(1))

    def test_resource_delete_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.query.delete(1))

    def test_resource_search_method_unsupported_exception(self):
        self.assertRaises(exceptions.ResourceBadMethodError, lambda: self.redmine.query.search('foo'))

    def test_filter_no_filters_exception(self):
        self.assertRaises(exceptions.ResourceNoFiltersProvidedError, lambda: self.redmine.issue.filter())

    def test_filter_unknown_filters_exception(self):
        self.assertRaises(exceptions.ResourceFilterError, lambda: self.redmine.version.filter(foo='bar'))

    def test_create_no_fields_exception(self):
        self.assertRaises(exceptions.ResourceNoFieldsProvidedError, lambda: self.redmine.user.create())

    def test_update_no_fields_exception(self):
        self.assertRaises(exceptions.ResourceNoFieldsProvidedError, lambda: self.redmine.project.update(1))

    def test_get_validation_exception(self):
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.wiki_page.get('foo'))

    def test_get_notfound_exception(self):
        self.response.json.return_value = responses['tracker']['all']
        self.assertRaises(exceptions.ResourceNotFoundError, lambda: self.redmine.tracker.get(999))

    def test_create_validation_exception(self):
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.issue_category.create(foo='bar'))

    def test_update_validation_exception(self):
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.wiki_page.update('Foo', title='Bar'))

    def test_delete_validation_exception(self):
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.wiki_page.delete('Foo'))

    def test_manager_is_picklable(self):
        import pickle
        project = self.redmine.project
        project.url = 'foo'
        project.params = {'foo': 'bar'}
        unpickled_project = pickle.loads(pickle.dumps(project))
        self.assertEqual(project.url, unpickled_project.url)
        self.assertEqual(project.params['foo'], unpickled_project.params['foo'])

    def test_create_validation_exception_via_put(self):
        self.response.content = ''
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.wiki_page.create(project_id=1, title='Foo'))

    def test_reraises_not_found_exception(self):
        self.response.status_code = 404
        self.assertRaises(exceptions.ResourceNotFoundError, lambda: self.redmine.project.get('non-existent-project'))
        self.assertRaises(exceptions.ResourceNotFoundError, lambda: list(self.redmine.project.all()))

    def test_resource_requirements_exception(self):
        FooResource.requirements = ('foo plugin', ('bar plugin', '1.2.3'),)
        self.response.status_code = 404
        self.assertRaises(exceptions.ResourceRequirementsError, lambda: self.redmine.foo_resource.get(1))
        self.assertRaises(exceptions.ResourceRequirementsError, lambda: list(self.redmine.foo_resource.all()))

    def test_search(self):
        self.response.json.return_value = {'total_count': 1, 'offset': 0, 'limit': 0, 'results': [
            {'id': 1, 'title': 'Foo', 'type': 'issue'}]}
        results = self.redmine.issue.search('foo')
        self.assertIsInstance(results['issues'], resultsets.ResourceSet)
        self.assertEqual(len(results['issues']), 1)

    def test_search_returns_none_if_nothing_found(self):
        self.response.json.return_value = {'total_count': 0, 'offset': 0, 'limit': 0, 'results': []}
        self.assertIsNone(self.redmine.issue.search('foo'))
