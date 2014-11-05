from tests import unittest, mock, json_response, Redmine, URL
from redmine.managers import ResourceManager
from redmine.resources import Project
from redmine.resultsets import ResourceSet
from redmine.exceptions import ResourceBadMethodError, ValidationError


class FooResource(Project):
    pass


class TestResourceManager(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.redmine = Redmine(self.url)

    def test_supports_project_resource(self):
        self.assertIsInstance(self.redmine.project, ResourceManager)

    def test_supports_issue_resource(self):
        self.assertIsInstance(self.redmine.issue, ResourceManager)

    def test_supports_time_entry_resource(self):
        self.assertIsInstance(self.redmine.time_entry, ResourceManager)

    def test_supports_enumeration_resource(self):
        self.assertIsInstance(self.redmine.enumeration, ResourceManager)

    def test_supports_attachment_resource(self):
        self.assertIsInstance(self.redmine.attachment, ResourceManager)

    def test_supports_issue_journal_resource(self):
        self.assertIsInstance(self.redmine.issue_journal, ResourceManager)

    def test_supports_wiki_page_resource(self):
        self.assertIsInstance(self.redmine.wiki_page, ResourceManager)

    def test_supports_project_membership_resource(self):
        self.assertIsInstance(self.redmine.project_membership, ResourceManager)

    def test_supports_issue_category_resource(self):
        self.assertIsInstance(self.redmine.issue_category, ResourceManager)

    def test_supports_issue_relation_resource(self):
        self.assertIsInstance(self.redmine.issue_relation, ResourceManager)

    def test_supports_version_resource(self):
        self.assertIsInstance(self.redmine.version, ResourceManager)

    def test_supports_user_resource(self):
        self.assertIsInstance(self.redmine.user, ResourceManager)

    def test_supports_group_resource(self):
        self.assertIsInstance(self.redmine.group, ResourceManager)

    def test_supports_role_resource(self):
        self.assertIsInstance(self.redmine.role, ResourceManager)

    def test_supports_news_resource(self):
        self.assertIsInstance(self.redmine.news, ResourceManager)

    def test_supports_issue_status_resource(self):
        self.assertIsInstance(self.redmine.issue_status, ResourceManager)

    def test_supports_tracker_resource(self):
        self.assertIsInstance(self.redmine.tracker, ResourceManager)

    def test_supports_query_resource(self):
        self.assertIsInstance(self.redmine.query, ResourceManager)

    def test_supports_custom_field_resource(self):
        self.assertIsInstance(self.redmine.custom_field, ResourceManager)

    def test_supports_custom_resources(self):
        self.redmine.custom_resource_paths = (__name__,)
        self.assertIsInstance(self.redmine.foo_resource, ResourceManager)

    def test_not_supported_resource_exception(self):
        from redmine.exceptions import ResourceError
        self.assertRaises(ResourceError, lambda: self.redmine.foobar)

    def test_not_supported_version_exception(self):
        from redmine.exceptions import ResourceVersionMismatchError
        self.redmine.ver = '0.0.1'
        self.assertRaises(ResourceVersionMismatchError, lambda: self.redmine.project)

    def test_convert_dict_to_resource_object(self):
        from redmine.resources import Project
        project = self.redmine.project.to_resource({'name': 'Foo', 'identifier': 'foo', 'id': 1})
        self.assertIsInstance(project, Project)
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.identifier, 'foo')
        self.assertEqual(project.id, 1)

    def test_convert_dicts_to_resource_set_object(self):
        resourceset = self.redmine.project.to_resource_set([
            {'name': 'Foo', 'identifier': 'foo', 'id': 1},
            {'name': 'Bar', 'identifier': 'bar', 'id': 2}
        ])
        self.assertIsInstance(resourceset, ResourceSet)
        self.assertEqual(resourceset[0].name, 'Foo')
        self.assertEqual(resourceset[0].identifier, 'foo')
        self.assertEqual(resourceset[0].id, 1)
        self.assertEqual(resourceset[1].name, 'Bar')
        self.assertEqual(resourceset[1].identifier, 'bar')
        self.assertEqual(resourceset[1].id, 2)

    @mock.patch('requests.get')
    def test_get_single_resource(self, mock_get):
        mock_get.return_value = response = mock.Mock(status_code=200)
        response.json = json_response({'project': {'name': 'Foo', 'identifier': 'foo', 'id': 1}})
        project = self.redmine.project.get('foo')
        self.assertEqual(project.name, 'Foo')
        self.assertEqual(project.identifier, 'foo')
        self.assertEqual(project.id, 1)

    def test_get_all_resources(self):
        self.assertIsInstance(self.redmine.project.all(), ResourceSet)

    def test_get_filtered_resources(self):
        self.assertIsInstance(self.redmine.issue.filter(project_id='foo'), ResourceSet)

    def test_prepare_params(self):
        from datetime import date, datetime
        time_entries = self.redmine.time_entry.filter(from_date=date(2014, 3, 9), to_date=date(2014, 3, 10))
        self.assertEqual(time_entries.manager.params['from'], '2014-03-09')
        self.assertEqual(time_entries.manager.params['to'], '2014-03-10')
        time_entries = self.redmine.time_entry.filter(from_date=datetime(2014, 3, 9), to_date=datetime(2014, 3, 10))
        self.assertEqual(time_entries.manager.params['from'], '2014-03-09T00:00:00Z')
        self.assertEqual(time_entries.manager.params['to'], '2014-03-10T00:00:00Z')

    @mock.patch('requests.post')
    def test_create_resource(self, mock_post):
        mock_post.return_value = response = mock.Mock(status_code=201)
        response.json = json_response({'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1}})
        user = self.redmine.user.create(firstname='John', lastname='Smith')
        self.assertEqual(user.firstname, 'John')
        self.assertEqual(user.lastname, 'Smith')

    @mock.patch('redmine.open', mock.mock_open(), create=True)
    @mock.patch('requests.post')
    def test_create_resource_with_uploads(self, mock_post):
        mock_post.return_value = response = mock.Mock(status_code=201)
        response.json = json_response({
            'upload': {'token': '123456'},
            'issue': {'subject': 'Foo', 'project_id': 1, 'id': 1}
        })
        issue = self.redmine.issue.create(project_id=1, subject='Foo', uploads=[{'path': 'foo'}])
        self.assertEqual(issue.project_id, 1)
        self.assertEqual(issue.subject, 'Foo')

    def test_create_empty_resource(self):
        project = self.redmine.project.new()
        defaults = dict((include, None) for include in project._includes)
        defaults.update(dict((relation, None) for relation in project._relations))
        self.assertEqual(project._attributes, defaults)

    @mock.patch('requests.put')
    def test_update_resource(self, mock_put):
        mock_put.return_value = mock.Mock(status_code=200, content='')
        manager = self.redmine.wiki_page
        manager.params['project_id'] = 1
        self.assertEqual(manager.update('Foo', title='Bar'), True)
        del manager.params['project_id']

    @mock.patch('redmine.open', mock.mock_open(), create=True)
    @mock.patch('requests.put')
    @mock.patch('requests.post')
    def test_update_resource_with_uploads(self, mock_post, mock_put):
        mock_put.return_value = mock.Mock(status_code=200, content='')
        mock_post.return_value = response = mock.Mock(status_code=201)
        response.json = json_response({'upload': {'token': '123456'}})
        manager = self.redmine.issue
        manager.params['subject'] = 'Foo'
        self.assertEqual(manager.update(1, subject='Bar', uploads=[{'path': 'foo'}]), True)
        del manager.params['subject']

    @mock.patch('requests.delete')
    def test_delete_resource(self, mock_delete):
        mock_delete.return_value = mock.Mock(status_code=200, content='')
        self.assertEqual(self.redmine.group.delete(1), True)

    def test_resource_get_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.enumeration.get('foo'))

    def test_resource_all_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.attachment.all())

    def test_resource_filter_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.project.filter())

    def test_resource_create_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.query.create())

    def test_resource_update_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.query.update(1))

    def test_resource_delete_method_unsupported_exception(self):
        self.assertRaises(ResourceBadMethodError, lambda: self.redmine.query.delete(1))

    def test_filter_no_filters_exception(self):
        from redmine.exceptions import ResourceNoFiltersProvidedError
        self.assertRaises(ResourceNoFiltersProvidedError, lambda: self.redmine.issue.filter())

    def test_filter_unknown_filters_exception(self):
        from redmine.exceptions import ResourceFilterError
        self.assertRaises(ResourceFilterError, lambda: self.redmine.version.filter(foo='bar'))

    def test_create_no_fields_exception(self):
        from redmine.exceptions import ResourceNoFieldsProvidedError
        self.assertRaises(ResourceNoFieldsProvidedError, lambda: self.redmine.user.create())

    def test_update_no_fields_exception(self):
        from redmine.exceptions import ResourceNoFieldsProvidedError
        self.assertRaises(ResourceNoFieldsProvidedError, lambda: self.redmine.project.update(1))

    def test_get_validation_exception(self):
        self.assertRaises(ValidationError, lambda: self.redmine.wiki_page.get('foo'))

    def test_create_validation_exception(self):
        self.assertRaises(ValidationError, lambda: self.redmine.issue_category.create(foo='bar'))

    def test_update_validation_exception(self):
        self.assertRaises(ValidationError, lambda: self.redmine.wiki_page.update('Foo', title='Bar'))

    def test_delete_validation_exception(self):
        self.assertRaises(ValidationError, lambda: self.redmine.wiki_page.delete('Foo'))

    def test_manager_is_picklable(self):
        import pickle
        project = self.redmine.project
        project.url = 'foo'
        project.params = {'foo': 'bar'}
        unpickled_project = pickle.loads(pickle.dumps(project))
        self.assertEqual(project.url, unpickled_project.url)
        self.assertEqual(project.params['foo'], unpickled_project.params['foo'])

    @mock.patch('requests.put')
    @mock.patch('requests.post')
    def test_create_validation_exception_via_put(self, mock_post, mock_put):
        mock_post.return_value = mock.Mock(status_code=404)
        mock_put.return_value = mock.Mock(status_code=200)
        self.assertRaises(ValidationError, lambda: self.redmine.user.create(firstname='John', lastname='Smith'))

    @mock.patch('requests.get')
    def test_reraises_not_found_exception(self, mock_get):
        from redmine.exceptions import ResourceNotFoundError
        mock_get.return_value = mock.Mock(status_code=404)
        self.assertRaises(ResourceNotFoundError, lambda: self.redmine.project.get('non-existent-project'))

    @mock.patch('requests.get')
    def test_resource_requirements_exception(self, mock_get):
        from redmine.exceptions import ResourceRequirementsError
        FooResource.requirements = ('foo plugin', ('bar plugin', '1.2.3'),)
        mock_get.return_value = mock.Mock(status_code=404)
        self.redmine.custom_resource_paths = (__name__,)
        self.assertRaises(ResourceRequirementsError, lambda: self.redmine.foo_resource.get(1))
