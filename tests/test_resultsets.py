from tests import unittest, mock, Redmine, URL

response = {
    'projects': [
        {'name': 'Foo', 'identifier': 'foo', 'id': 1},
        {'name': 'Bar', 'identifier': 'bar', 'id': 2},
        {'name': 'Baz', 'identifier': 'baz', 'id': 3},
    ]
}


class TestResultSet(unittest.TestCase):
    def setUp(self):
        self.redmine = Redmine(URL)
        self.response = mock.Mock(status_code=200, json=mock.Mock(return_value=response))
        patcher_get = mock.patch('redmine.requests.get', return_value=self.response)
        patcher_put = mock.patch('redmine.requests.put', return_value=self.response)
        patcher_delete = mock.patch('redmine.requests.delete', return_value=self.response)
        patcher_get.start()
        patcher_put.start()
        patcher_delete.start()
        self.addCleanup(patcher_get.stop)
        self.addCleanup(patcher_put.stop)
        self.addCleanup(patcher_delete.stop)

    def test_has_custom_repr(self):
        self.assertEqual(repr(self.redmine.project.all()),
                         '<redmine.resultsets.ResourceSet object with Project resources>')

    def test_offset_limit_all(self):
        self.response.json.return_value = dict(response, total_count=3, limit=0, offset=0)
        projects = self.redmine.project.all()
        self.assertEqual(projects.limit, 0)
        self.assertEqual(projects.offset, 0)
        self.assertEqual(projects[0].id, 1)
        self.assertEqual(projects[1].id, 2)
        self.assertEqual(projects[2].id, 3)

    def test_offset_limit(self):
        response_with_limit_offset = {'total_count': 2, 'limit': 3, 'offset': 1, 'projects': response['projects'][1:3]}
        self.response.json.return_value = response_with_limit_offset
        projects = self.redmine.project.all()[1:3]
        self.assertEqual(projects.limit, 3)
        self.assertEqual(projects.offset, 1)
        self.assertEqual(projects[0].id, 2)
        self.assertEqual(projects[1].id, 3)
        self.assertEqual(projects[:1][0].id, 2)
        self.assertEqual(projects[1:][0].id, 3)
        self.assertEqual(projects[1:1][0].id, 3)

    def test_offset_limit_mimic(self):
        projects = self.redmine.project.all()[1:3]
        self.assertEqual(projects.limit, 3)
        self.assertEqual(projects.offset, 1)
        self.assertEqual(projects[0].id, 2)
        self.assertEqual(projects[1].id, 3)

    def test_total_count(self):
        self.response.json.return_value = dict(response, total_count=3, limit=0, offset=0)
        projects = self.redmine.project.all()
        len(projects)
        self.assertEqual(projects.total_count, 3)

    def test_total_count_mimic(self):
        response_with_custom_fields = {'project': dict(response['projects'][0], custom_fields=[{'id': 1, 'value': 0}])}
        self.response.json.return_value = response_with_custom_fields
        project = self.redmine.project.get('foo')
        self.assertEqual(project.custom_fields.total_count, 1)

    def test_total_count_raise_exception_if_not_evaluated(self):
        from redmine.exceptions import ResultSetTotalCountError
        self.assertRaises(ResultSetTotalCountError, lambda: self.redmine.project.all().total_count)

    def test_resultset_is_empty(self):
        self.response.json.return_value = {'limit': 100, 'projects': [], 'total_count': 0, 'offset': 0}
        projects = self.redmine.project.all()
        self.assertEqual(len(projects), 0)
        self.assertEqual(list(projects), [])

    def test_sliced_resultset_is_empty(self):
        self.response.json.return_value = {'limit': 100, 'projects': [], 'total_count': 0, 'offset': 0}
        projects = self.redmine.project.all()[:200]
        self.assertEqual(len(projects), 0)
        self.assertEqual(list(projects), [])

    def test_supports_iteration(self):
        projects = list(self.redmine.project.all())
        self.assertEqual(projects[0].name, 'Foo')
        self.assertEqual(projects[0].identifier, 'foo')
        self.assertEqual(projects[0].id, 1)
        self.assertEqual(projects[1].name, 'Bar')
        self.assertEqual(projects[1].identifier, 'bar')
        self.assertEqual(projects[1].id, 2)

    def test_supports_len(self):
        self.assertEqual(len(self.redmine.project.all()), 3)

    def test_get_method_resource_found(self):
        projects = self.redmine.project.all().get(2)
        self.assertEqual(projects.id, 2)

    def test_get_method_resource_not_found(self):
        projects = self.redmine.project.all().get(6)
        self.assertEqual(projects, None)

    def test_filter_method(self):
        projects = self.redmine.project.all().filter((1, 3))
        self.assertEqual(projects[0].id, 1)
        self.assertEqual(projects[1].id, 3)

    def test_update_method(self):
        projects = self.redmine.project.all().update(name='FooBar')
        self.assertEqual(projects[0].name, 'FooBar')
        self.assertEqual(projects[1].name, 'FooBar')
        self.assertEqual(projects[2].name, 'FooBar')

    def test_delete_method(self):
        self.assertEqual(self.redmine.project.all().delete(), True)

    def test_resourceset_is_picklable(self):
        import pickle
        projects = self.redmine.project.all()
        unpickled_projects = pickle.loads(pickle.dumps(projects))
        self.assertEqual(projects[0]['name'], unpickled_projects[0]['name'])
        self.assertEqual(projects[1]['name'], unpickled_projects[1]['name'])
        self.assertEqual(projects[2]['name'], unpickled_projects[2]['name'])

    def test_values_method(self):
        projects = list(self.redmine.project.all().values())
        self.assertEqual(projects[0]['name'], 'Foo')
        self.assertEqual(projects[0]['identifier'], 'foo')
        self.assertEqual(projects[0]['id'], 1)
        self.assertEqual(projects[1]['name'], 'Bar')
        self.assertEqual(projects[1]['identifier'], 'bar')
        self.assertEqual(projects[1]['id'], 2)
        self.assertEqual(projects[2]['name'], 'Baz')
        self.assertEqual(projects[2]['identifier'], 'baz')
        self.assertEqual(projects[2]['id'], 3)

    def test_values_method_with_fields(self):
        projects = list(self.redmine.project.all().values('name', 'id'))
        self.assertEqual(len(projects[0]), 2)
        self.assertEqual(projects[0]['name'], 'Foo')
        self.assertEqual(projects[0]['id'], 1)
        self.assertEqual(len(projects[1]), 2)
        self.assertEqual(projects[1]['name'], 'Bar')
        self.assertEqual(projects[1]['id'], 2)
        self.assertEqual(len(projects[2]), 2)
        self.assertEqual(projects[2]['name'], 'Baz')
        self.assertEqual(projects[2]['id'], 3)

    def test_values_list_method(self):
        projects = list(self.redmine.project.all().values_list())
        self.assertIn('Foo', projects[0])
        self.assertIn('foo', projects[0])
        self.assertIn(1, projects[0])
        self.assertIn('Bar', projects[1])
        self.assertIn('bar', projects[1])
        self.assertIn(2, projects[1])
        self.assertIn('Baz', projects[2])
        self.assertIn('baz', projects[2])
        self.assertIn(3, projects[2])

    def test_values_list_method_with_fields(self):
        projects = list(self.redmine.project.all().values_list('id', 'name'))
        self.assertEqual(len(projects[0]), 2)
        self.assertEqual(projects[0][0], 1)
        self.assertEqual(projects[0][1], 'Foo')
        self.assertEqual(len(projects[1]), 2)
        self.assertEqual(projects[1][0], 2)
        self.assertEqual(projects[1][1], 'Bar')
        self.assertEqual(len(projects[2]), 2)
        self.assertEqual(projects[2][0], 3)
        self.assertEqual(projects[2][1], 'Baz')

    def test_values_list_method_flattened(self):
        projects = list(self.redmine.project.all().values_list('id', flat=True))
        self.assertEqual(projects[0], 1)
        self.assertEqual(projects[1], 2)
        self.assertEqual(projects[2], 3)

    @mock.patch('redmine.open', mock.mock_open(), create=True)
    def test_export(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar'), '/foo/bar/issues.txt')

    def test_export_not_supported_exception(self):
        from redmine.exceptions import ExportNotSupported
        self.assertRaises(ExportNotSupported, lambda: self.redmine.custom_field.all().export('pdf'))

    def test_export_format_not_supported_exception(self):
        from redmine.exceptions import ExportFormatNotSupportedError
        self.response.status_code = 406
        self.assertRaises(ExportFormatNotSupportedError, lambda: self.redmine.issue.all().export('foo'))

    def test_export_reraises_unknown_error(self):
        from redmine.exceptions import UnknownError
        self.response.status_code = 999
        self.assertRaises(UnknownError, lambda: self.redmine.issue.all().export('foo'))

    def test_filter_param_exception(self):
        from redmine.exceptions import ResourceSetFilterParamError
        self.assertRaises(ResourceSetFilterParamError, lambda: self.redmine.project.all().filter(1))

    def test_index_error_exception(self):
        from redmine.exceptions import ResourceSetIndexError
        self.assertRaises(ResourceSetIndexError, lambda: self.redmine.project.all()[6])
