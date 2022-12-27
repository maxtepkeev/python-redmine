from . import mock, BaseRedmineTestCase

from redminelib import exceptions

response = {
    'issues': [
        {'subject': 'Foo', 'id': 1, 'tracker_id': 1},
        {'subject': 'Bar', 'id': 2, 'tracker_id': 2},
        {'subject': 'Baz', 'id': 3, 'tracker_id': 3},
    ]
}


class ResultSetTestCase(BaseRedmineTestCase):
    def setUp(self):
        super().setUp()
        self.response.json = mock.Mock(return_value=response)

    def test_has_custom_repr(self):
        self.assertEqual(repr(self.redmine.issue.all()),
                         '<redminelib.resultsets.ResourceSet object with Issue resources>')

    def test_offset_limit_all(self):
        self.response.json.return_value = dict(total_count=3, limit=0, offset=0, **response)
        issues = self.redmine.issue.all()
        self.assertEqual(issues.limit, 0)
        self.assertEqual(issues.offset, 0)
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[1].id, 2)
        self.assertEqual(issues[2].id, 3)

    def test_offset_limit(self):
        self.response.json.return_value = {
            'total_count': 2, 'limit': 300, 'offset': 1, 'issues': response['issues'][1:3]}
        issues = self.redmine.issue.all()[1:300]
        self.assertEqual(issues.limit, 300)
        self.assertEqual(issues.offset, 1)
        self.assertEqual(issues[0].id, 2)
        self.assertEqual(issues[1].id, 3)
        self.assertEqual(issues[:1][0].id, 2)
        self.assertEqual(issues[1:][0].id, 3)
        self.assertEqual(issues[1:1][0].id, 3)

    def test_offset_limit_mimic(self):
        issues = self.redmine.issue.all()[1:3]
        self.assertEqual(issues.limit, 3)
        self.assertEqual(issues.offset, 1)
        self.assertEqual(issues[0].id, 2)
        self.assertEqual(issues[1].id, 3)

    def test_total_count(self):
        self.response.json.return_value = dict(total_count=3, limit=0, offset=0, **response)
        issues = self.redmine.issue.all()
        len(issues)
        self.assertEqual(issues.total_count, 3)

    def test_total_count_mimic(self):
        response_with_cf = {'issue': dict(custom_fields=[{'id': 1, 'value': 0}], **response['issues'][0])}
        self.response.json.return_value = response_with_cf
        issue = self.redmine.issue.get(1)
        self.assertEqual(issue.custom_fields.total_count, 1)

    def test_total_count_raise_exception_if_not_evaluated(self):
        self.assertRaises(exceptions.ResultSetTotalCountError, lambda: self.redmine.issue.all().total_count)

    def test_resultset_is_empty(self):
        self.response.json.return_value = {'limit': 100, 'issues': [], 'total_count': 0, 'offset': 0}
        issues = self.redmine.issue.all()
        self.assertEqual(len(issues), 0)
        self.assertEqual(list(issues), [])

    def test_sliced_resultset_is_empty(self):
        self.response.json.return_value = {'limit': 100, 'issues': [], 'total_count': 0, 'offset': 0}
        issues = self.redmine.issue.all()[:200]
        self.assertEqual(len(issues), 0)
        self.assertEqual(list(issues), [])

    def test_supports_iteration(self):
        issues = list(self.redmine.issue.all())
        self.assertEqual(issues[0].subject, 'Foo')
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[1].subject, 'Bar')
        self.assertEqual(issues[1].id, 2)

    def test_supports_len(self):
        self.assertEqual(len(self.redmine.issue.all()), 3)

    def test_get_method_resource_found(self):
        issues = self.redmine.issue.all().get(2)
        self.assertEqual(issues.id, 2)

    def test_get_method_resource_not_found(self):
        issues = self.redmine.issue.all().get(6)
        self.assertEqual(issues, None)

    def test_filter_method_nonexistant_attributes(self):
        issues = self.redmine.issue.all().filter(id=1, foo__exact=1)
        self.assertEqual(len(issues), 0)

    def test_filter_exact_lookup(self):
        issues = self.redmine.issue.all().filter(id=1, tracker_id__exact=1)
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(len(issues), 1)

    def test_filter_in_lookup(self):
        issues = self.redmine.issue.all().filter(id__in=(1, 3))
        self.assertEqual(issues[0].id, 1)
        self.assertEqual(issues[1].id, 3)
        self.assertEqual(len(issues), 2)

    def test_update_method(self):
        issues = self.redmine.issue.all().update(subject='FooBar')
        self.assertEqual(issues[0].subject, 'FooBar')
        self.assertEqual(issues[1].subject, 'FooBar')
        self.assertEqual(issues[2].subject, 'FooBar')

    def test_delete_method(self):
        self.assertEqual(self.redmine.issue.all().delete(), True)

    def test_resourceset_is_picklable(self):
        import pickle
        issues = self.redmine.issue.all()
        unpickled_issues = pickle.loads(pickle.dumps(issues))
        self.assertEqual(issues[0]['subject'], unpickled_issues[0]['subject'])
        self.assertEqual(issues[1]['subject'], unpickled_issues[1]['subject'])
        self.assertEqual(issues[2]['subject'], unpickled_issues[2]['subject'])

    def test_values_method(self):
        issues = list(self.redmine.issue.all().values())
        self.assertEqual(issues[0]['subject'], 'Foo')
        self.assertEqual(issues[0]['id'], 1)
        self.assertEqual(issues[1]['subject'], 'Bar')
        self.assertEqual(issues[1]['id'], 2)
        self.assertEqual(issues[2]['subject'], 'Baz')
        self.assertEqual(issues[2]['id'], 3)

    def test_values_method_with_fields(self):
        issues = list(self.redmine.issue.all().values('subject', 'id'))
        self.assertEqual(len(issues[0]), 2)
        self.assertEqual(issues[0]['subject'], 'Foo')
        self.assertEqual(issues[0]['id'], 1)
        self.assertEqual(len(issues[1]), 2)
        self.assertEqual(issues[1]['subject'], 'Bar')
        self.assertEqual(issues[1]['id'], 2)
        self.assertEqual(len(issues[2]), 2)
        self.assertEqual(issues[2]['subject'], 'Baz')
        self.assertEqual(issues[2]['id'], 3)

    def test_values_list_method(self):
        issues = list(self.redmine.issue.all().values_list())
        self.assertIn('Foo', issues[0])
        self.assertIn(1, issues[0])
        self.assertIn('Bar', issues[1])
        self.assertIn(2, issues[1])
        self.assertIn('Baz', issues[2])
        self.assertIn(3, issues[2])

    def test_values_list_method_with_fields(self):
        issues = list(self.redmine.issue.all().values_list('id', 'subject'))
        self.assertEqual(len(issues[0]), 2)
        self.assertEqual(issues[0][0], 1)
        self.assertEqual(issues[0][1], 'Foo')
        self.assertEqual(len(issues[1]), 2)
        self.assertEqual(issues[1][0], 2)
        self.assertEqual(issues[1][1], 'Bar')
        self.assertEqual(len(issues[2]), 2)
        self.assertEqual(issues[2][0], 3)
        self.assertEqual(issues[2][1], 'Baz')

    def test_values_list_method_flattened(self):
        issues = list(self.redmine.issue.all().values_list('id', flat=True))
        self.assertEqual(issues[0], 1)
        self.assertEqual(issues[1], 2)
        self.assertEqual(issues[2], 3)

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar'), '/foo/bar/issues.txt')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export_with_all_columns(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns='all'), '/foo/bar/issues.txt')
        self.redmine.ver = '3.3.0'
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns='all'), '/foo/bar/issues.txt')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export_with_all_gui_columns(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns='all_gui'), '/foo/bar/issues.txt')
        self.redmine.ver = '3.3.0'
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns='all_gui'), '/foo/bar/issues.txt')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export_with_all_gui_extra_columns(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns=['all_gui']), '/foo/bar/issues.txt')
        self.redmine.ver = '3.3.0'
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns=['all_gui']), '/foo/bar/issues.txt')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_export_with_custom_columns(self):
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.issue.all().export('txt', '/foo/bar', columns=['status']), '/foo/bar/issues.txt')

    def test_export_not_supported_exception(self):
        self.assertRaises(exceptions.ExportNotSupported, lambda: self.redmine.custom_field.all().export('pdf'))

    def test_export_format_not_supported_exception(self):
        self.response.status_code = 406
        self.assertRaises(exceptions.ExportFormatNotSupportedError, lambda: self.redmine.issue.all().export('foo'))

    def test_export_reraises_unknown_error(self):
        self.response.status_code = 999
        self.assertRaises(exceptions.UnknownError, lambda: self.redmine.issue.all().export('foo'))

    def test_filter_no_filters_exception(self):
        self.assertRaises(exceptions.ResourceNoFiltersProvidedError, lambda: self.redmine.issue.all().filter())

    def test_filter_lookup_exception(self):
        self.assertRaises(exceptions.ResourceSetFilterLookupError, lambda: self.redmine.issue.all().filter(id__bar=1))

    def test_filter_bad_lookup_class_definition(self):
        from redminelib import lookups
        type('Foo', (lookups.Lookup,), {'lookup_name': 'foo'})
        self.assertRaises(NotImplementedError, lambda: self.redmine.issue.all().filter(id__foo=1))
        del lookups.registry['foo']

    def test_index_error_exception(self):
        self.assertRaises(exceptions.ResourceSetIndexError, lambda: self.redmine.issue.all()[6])
