from tests import unittest, mock, Redmine, URL


class TestRedmine(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.redmine = Redmine(self.url)

    def test_default_attributes(self):
        self.assertEqual(self.redmine.url, self.url)
        self.assertEqual(self.redmine.key, None)
        self.assertEqual(self.redmine.ver, None)
        self.assertEqual(self.redmine.username, None)
        self.assertEqual(self.redmine.password, None)
        self.assertEqual(self.redmine.impersonate, None)
        self.assertEqual(self.redmine.date_format, '%Y-%m-%d')
        self.assertEqual(self.redmine.datetime_format, '%Y-%m-%dT%H:%M:%SZ')

    def test_set_attributes_through_kwargs(self):
        self.redmine = Redmine(
            self.url,
            key='123',
            version='1.0',
            username='john',
            password='qwerty',
            impersonate='jsmith',
            date_format='format',
            datetime_format='format'
        )
        self.assertEqual(self.redmine.url, self.url)
        self.assertEqual(self.redmine.key, '123')
        self.assertEqual(self.redmine.ver, '1.0')
        self.assertEqual(self.redmine.username, 'john')
        self.assertEqual(self.redmine.password, 'qwerty')
        self.assertEqual(self.redmine.impersonate, 'jsmith')
        self.assertEqual(self.redmine.date_format, 'format')
        self.assertEqual(self.redmine.datetime_format, 'format')


class TestRedmineRequest(unittest.TestCase):
    def setUp(self):
        self.url = URL
        self.redmine = Redmine(self.url)
        self.response = mock.Mock()
        patcher = mock.patch('requests.get', return_value=self.response)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_successful_response(self):
        self.response.status_code = 200
        self.response.json.return_value = {'success': True}
        self.assertEqual(self.redmine.request('get', self.url)['success'], True)

    def test_auth_error_exception(self):
        from redmine.exceptions import AuthError
        self.response.status_code = 401
        self.assertRaises(AuthError, lambda: self.redmine.request('get', self.url))

    def test_impersonate_error_exception(self):
        from redmine.exceptions import ImpersonateError
        self.redmine.impersonate = 'not_exists'
        self.response.status_code = 412
        self.assertRaises(ImpersonateError, lambda: self.redmine.request('get', self.url))

    def test_none_response(self):
        self.assertEqual(self.redmine.request('get', self.url), None)
