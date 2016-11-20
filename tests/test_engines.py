from . import mock, BaseRedmineTestCase, Redmine

from redminelib import engines, exceptions


class BaseEngineTestCase(BaseRedmineTestCase):
    def test_engine_init(self):
        redmine = Redmine(self.url, key='123', impersonate='jsmith', requests={'foo': 'bar'})
        self.assertEqual(redmine.engine.requests['params']['key'], '123')
        self.assertEqual(redmine.engine.requests['headers']['X-Redmine-Switch-User'], 'jsmith')
        self.assertEqual(redmine.engine.requests['foo'], 'bar')
        redmine = Redmine(self.url, username='john', password='qwerty')
        self.assertEqual(redmine.engine.requests['auth'], ('john', 'qwerty'))

    def test_successful_response_via_username_password(self):
        self.redmine.engine.requests['auth'] = ('john', 'qwerty')
        self.response.status_code = 200
        self.response.json.return_value = {'success': True}
        self.assertEqual(self.redmine.engine.request('get', self.url)['success'], True)

    def test_successful_response_via_api_key(self):
        self.redmine.engine.requests['params']['key'] = '123'
        self.response.status_code = 200
        self.response.json.return_value = {'success': True}
        self.assertEqual(self.redmine.engine.request('get', self.url)['success'], True)

    def test_successful_response_via_put_method(self):
        self.response.status_code = 200
        self.response.content = ''
        self.assertEqual(self.redmine.engine.request('put', self.url), True)

    def test_session_not_implemented_exception(self):
        self.assertRaises(NotImplementedError, lambda: engines.BaseEngine())

    def test_process_bulk_request_not_implemented_exception(self):
        self.redmine.engine = type('FooEngine', (engines.BaseEngine,), {'create_session': lambda obj, **kwargs: None})()
        self.assertRaises(NotImplementedError, lambda: self.redmine.engine.process_bulk_request(
            'get', '/foo', 'bar', {}))

    def test_conflict_error_exception(self):
        self.response.status_code = 409
        self.assertRaises(exceptions.ConflictError, lambda: self.redmine.engine.request('put', self.url))

    def test_json_decode_error_exception(self):
        self.response.status_code = 200
        self.response.json = mock.Mock(side_effect=ValueError)
        self.assertRaises(exceptions.JSONDecodeError, lambda: self.redmine.engine.request('get', self.url))

    def test_auth_error_exception(self):
        self.response.status_code = 401
        self.assertRaises(exceptions.AuthError, lambda: self.redmine.engine.request('get', self.url))

    def test_forbidden_error_exception(self):
        self.response.status_code = 403
        self.assertRaises(exceptions.ForbiddenError, lambda: self.redmine.engine.request('get', self.url))

    def test_impersonate_error_exception(self):
        self.response.status_code = 412
        self.assertRaises(exceptions.ImpersonateError, lambda: self.redmine.engine.request('get', self.url))

    def test_server_error_exception(self):
        self.response.status_code = 500
        self.assertRaises(exceptions.ServerError, lambda: self.redmine.engine.request('post', self.url))

    def test_request_entity_too_large_error_exception(self):
        self.response.status_code = 413
        self.assertRaises(exceptions.RequestEntityTooLargeError, lambda: self.redmine.engine.request('post', self.url))

    def test_validation_error_exception(self):
        self.response.status_code = 422
        self.response.json.return_value = {'errors': ['foo', 'bar', ['foo', 'bar']]}
        self.assertRaises(exceptions.ValidationError, lambda: self.redmine.engine.request('post', self.url))

    def test_not_found_error_exception(self):
        self.response.status_code = 404
        self.assertRaises(exceptions.ResourceNotFoundError, lambda: self.redmine.engine.request('get', self.url))

    def test_unknown_error_exception(self):
        self.response.status_code = 888
        self.assertRaises(exceptions.UnknownError, lambda: self.redmine.engine.request('get', self.url))

    def test_http_protocol_exception(self):
        self.response.history = [mock.Mock()]
        self.redmine.url = 'http://foo.bar'
        self.assertRaises(exceptions.HTTPProtocolError, lambda: self.redmine.engine.request('get', self.url))

    def test_engine_is_picklable(self):
        import pickle
        self.redmine.engine.requests['params']['key'] = '123'
        self.redmine.engine.requests['headers']['X-Redmine-Switch-User'] = 'jsmith'
        redmine = pickle.loads(pickle.dumps(self.redmine))
        self.assertEqual(redmine.engine.requests['params']['key'], '123')
        self.assertEqual(redmine.engine.requests['headers']['X-Redmine-Switch-User'], 'jsmith')
