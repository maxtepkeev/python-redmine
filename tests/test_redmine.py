from . import mock, BaseRedmineTestCase, Redmine

from redminelib import engines, resultsets, exceptions


class RedmineTestCase(BaseRedmineTestCase):
    def test_default_attributes(self):
        self.assertEqual(self.redmine.url, self.url)
        self.assertEqual(self.redmine.ver, None)
        self.assertEqual(self.redmine.date_format, '%Y-%m-%d')
        self.assertEqual(self.redmine.datetime_format, '%Y-%m-%dT%H:%M:%SZ')
        self.assertEqual(self.redmine.raise_attr_exception, True)
        self.assertEqual(self.redmine.resource_paths, ())
        self.assertEqual(self.redmine.engine.__class__, engines.DefaultEngine)

    def test_set_attributes_through_kwargs(self):
        FooEngine = type('FooEngine', (engines.BaseEngine,), {'create_session': lambda obj, **kwargs: None})
        redmine = Redmine(self.url, version='1.0', date_format='format', datetime_format='format',
                          raise_attr_exception=False, resource_paths='foo.bar.baz', engine=FooEngine)
        self.assertEqual(redmine.url, self.url)
        self.assertEqual(redmine.ver, '1.0')
        self.assertEqual(redmine.date_format, 'format')
        self.assertEqual(redmine.datetime_format, 'format')
        self.assertEqual(redmine.raise_attr_exception, False)
        self.assertEqual(redmine.resource_paths, 'foo.bar.baz')
        self.assertEqual(redmine.engine.__class__, FooEngine)

    def test_engine_class_exception(self):
        self.assertRaises(exceptions.EngineClassError, lambda: Redmine(self.url, engine=type('Foo', (object,), {})))

    def test_session_impersonate(self):
        with self.redmine.session(impersonate='jsmith'):
            self.assertEqual(self.redmine.engine.requests['headers']['X-Redmine-Switch-User'], 'jsmith')
        self.assertRaises(KeyError, lambda: self.redmine.engine.requests['headers']['X-Redmine-Switch-User'])

    def test_session_key(self):
        with self.redmine.session(key='opa'):
            self.assertEqual(self.redmine.engine.requests['params']['key'], 'opa')
        self.assertRaises(KeyError, lambda: self.redmine.engine.requests['params']['key'])

    def test_session_username_password(self):
        with self.redmine.session(username='john', password='smith'):
            self.assertEqual(self.redmine.engine.requests['auth'], ('john', 'smith'))
        self.assertRaises(KeyError, lambda: self.redmine.engine.requests['auth'])

    def test_session_requests(self):
        self.redmine.engine.requests['cert'] = ('bar', 'baz')
        requests = {'verify': False, 'timeout': 2, 'cert': ('foo', 'bar'), 'params': {'foo': 'bar'}}
        with self.redmine.session(key='secret', requests=requests):
            self.assertEqual(self.redmine.engine.requests['params'], dict(key='secret', **requests['params']))
            self.assertEqual(self.redmine.engine.requests['verify'], requests['verify'])
            self.assertEqual(self.redmine.engine.requests['timeout'], requests['timeout'])
            self.assertEqual(self.redmine.engine.requests['cert'], requests['cert'])
        self.assertEqual(self.redmine.engine.requests['params'], {})
        self.assertEqual(self.redmine.engine.requests['cert'], ('bar', 'baz'))
        self.assertRaises(KeyError, lambda: self.redmine.engine.requests['verify'])
        self.assertRaises(KeyError, lambda: self.redmine.engine.requests['timeout'])

    @mock.patch('os.path.isfile', mock.Mock())
    @mock.patch('os.path.getsize', mock.Mock())
    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_successful_file_upload(self):
        self.response.status_code = 201
        self.response.json.return_value = {'upload': {'token': '123456'}}
        self.assertEqual(self.redmine.upload('foo'), '123456')

    @mock.patch('redminelib.open', mock.mock_open(), create=True)
    def test_successful_file_download(self):
        self.response.status_code = 200
        self.response.iter_content = lambda chunk_size: (str(num) for num in range(0, 5))
        self.assertEqual(self.redmine.download('http://foo/bar.txt', '/some/path'), '/some/path/bar.txt')

    def test_successful_in_memory_file_download(self):
        self.response.status_code = 200
        self.response.iter_content = lambda: (str(num) for num in range(0, 5))
        self.assertEqual(''.join(self.redmine.download('http://foo/bar.txt').iter_content()), '01234')

    def test_file_url_exception(self):
        self.response.status_code = 200
        self.assertRaises(exceptions.FileUrlError, lambda: self.redmine.download('http://bad_url', '/some/path'))

    def test_file_upload_no_file_exception(self):
        self.assertRaises(exceptions.NoFileError, lambda: self.redmine.upload('foo',))

    def test_file_upload_not_supported_exception(self):
        self.redmine.ver = '1.0.0'
        self.assertRaises(exceptions.VersionMismatchError, lambda: self.redmine.upload('foo',))

    def test_auth(self):
        self.redmine.username = 'john'
        self.redmine.password = 'qwerty'
        self.response.status_code = 200
        self.response.json.return_value = {'user': {'firstname': 'John', 'lastname': 'Smith', 'id': 1}}
        self.assertEqual(self.redmine.auth().firstname, 'John')

    def test_search(self):
        self.response.json.return_value = {'total_count': 6, 'offset': 0, 'limit': 0, 'results': [
            {'id': 1, 'title': 'Foo', 'type': 'issue'},
            {'id': 2, 'title': 'Bar', 'type': 'issue closed'},
            {'id': 3, 'title': 'Foo', 'type': 'project'},
            {'id': 4, 'title': 'Foo', 'type': 'news'},
            {'id': 5, 'title': 'Foo', 'type': 'wiki-page'},
            {'id': 6, 'title': 'Foo', 'type': 'document'},
        ]}
        results = self.redmine.search('foo')
        self.assertIsInstance(results['issues'], resultsets.ResourceSet)
        self.assertEqual(len(results['issues']), 2)
        self.assertIsInstance(results['projects'], resultsets.ResourceSet)
        self.assertEqual(len(results['projects']), 1)
        self.assertIsInstance(results['news'], resultsets.ResourceSet)
        self.assertEqual(len(results['news']), 1)
        self.assertIsInstance(results['wiki_pages'], resultsets.ResourceSet)
        self.assertEqual(len(results['wiki_pages']), 1)
        self.assertIsInstance(results['unknown'], dict)
        self.assertEqual(len(results['unknown']['document']), 1)

    def test_search_without_unknown(self):
        self.response.json.return_value = {'total_count': 1, 'offset': 0, 'limit': 0, 'results': [
            {'id': 1, 'title': 'Foo', 'type': 'issue'}]}
        results = self.redmine.search('foo')
        self.assertIsInstance(results['issues'], resultsets.ResourceSet)
        self.assertEqual(len(results['issues']), 1)

    def test_search_not_supported_exception(self):
        self.redmine.ver = '1.0.0'
        self.assertRaises(exceptions.VersionMismatchError, lambda: self.redmine.search('foo'))

    def test_redmine_is_picklable(self):
        import pickle
        redmine = pickle.loads(pickle.dumps(self.redmine))
        self.assertEqual(redmine.url, self.redmine.url)
        self.assertEqual(redmine.ver, self.redmine.ver)
        self.assertEqual(redmine.date_format, self.redmine.date_format)
        self.assertEqual(redmine.datetime_format, self.redmine.datetime_format)
        self.assertEqual(redmine.raise_attr_exception, self.redmine.raise_attr_exception)
        self.assertEqual(redmine.resource_paths, self.redmine.resource_paths)
