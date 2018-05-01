"""
Base engine that defines common behaviour and settings for all engines.
"""

import json

from .. import exceptions


class BaseEngine(object):
    chunk = 100

    def __init__(self, **options):
        """
        :param string key: (optional). API key used for authentication.
        :param string username: (optional). Username used for authentication.
        :param string password: (optional). Password used for authentication.
        :param dict requests: (optional). Connection options.
        :param string impersonate: (optional). Username to impersonate.
        :param bool return_raw_response (optional). Whether to return raw or json encoded responses.
        """
        self.return_raw_response = options.pop('return_raw_response', False)
        self.requests = dict(dict(headers={}, params={}, data={}), **options.get('requests', {}))

        if options.get('impersonate') is not None:
            self.requests['headers']['X-Redmine-Switch-User'] = options['impersonate']

        # We would like to be authenticated by API key by default
        if options.get('key') is not None:
            self.requests['params']['key'] = options['key']
        elif options.get('username') is not None and options.get('password') is not None:
            self.requests['auth'] = (options['username'], options['password'])

        self.session = self.create_session(**self.requests)

    @staticmethod
    def create_session(**params):
        """
        Creates a session object that will be used to make requests to Redmine.

        :param dict params: (optional). Session params.
        """
        raise NotImplementedError

    @staticmethod
    def construct_request_kwargs(method, headers, params, data):
        """
        Constructs kwargs that will be used in all requests to Redmine.

        :param string method: (required). HTTP verb to use for the request.
        :param dict headers: (required). HTTP headers to send with the request.
        :param dict params: (required). Params to send in the query string.
        :param data: (required). Data to send in the body of the request.
        :type data: dict, bytes or file-like object
        """
        kwargs = {'data': data or {}, 'params': params or {}, 'headers': headers or {}}

        if method in ('post', 'put', 'patch') and 'Content-Type' not in kwargs['headers']:
            kwargs['data'] = json.dumps(data)
            kwargs['headers']['Content-Type'] = 'application/json'

        return kwargs

    def request(self, method, url, headers=None, params=None, data=None):
        """
        Makes a single request to Redmine and returns processed response.

        :param string method: (required). HTTP verb to use for the request.
        :param string url: (required). URL of the request.
        :param dict headers: (optional). HTTP headers to send with the request.
        :param dict params: (optional). Params to send in the query string.
        :param data: (optional). Data to send in the body of the request.
        :type data: dict, bytes or file-like object
        """
        kwargs = self.construct_request_kwargs(method, headers, params, data)
        return self.process_response(self.session.request(method, url, **kwargs))

    def bulk_request(self, method, url, container, **params):
        """
        Makes needed preparations before launching the active engine's request process.

        :param string method: (required). HTTP verb to use for the request.
        :param string url: (required). URL of the request.
        :param string container: (required). Key in the response that should be used to access retrieved resources.
        :param dict params: (optional). Params that should be used for resource retrieval.
        """
        limit = params.get('limit') or 0
        offset = params.get('offset') or 0
        response = self.request(method, url, params=dict(params, limit=limit or self.chunk, offset=offset))

        # Resource supports limit/offset on Redmine level
        if all(response.get(param) is not None for param in ('total_count', 'limit', 'offset')):
            total_count = response['total_count']
            results = response[container]
            limit = limit or total_count

            if limit > self.chunk:
                bulk_params = []

                for num in range(limit - self.chunk, 0, -self.chunk):
                    offset += self.chunk
                    limit -= self.chunk
                    bulk_params.append(dict(params, offset=offset, limit=limit))

                # If we need to make just one more request, there's no point in async
                if len(bulk_params) == 1:
                    results.extend(self.request(method, url, params=bulk_params[0])[container])
                else:
                    results.extend(self.process_bulk_request(method, url, container, bulk_params))
        # We have to mimic limit/offset if a resource
        # doesn't support this feature on Redmine level
        else:
            total_count = len(response[container])
            results = response[container][offset:None if limit == 0 else limit + offset]

        return results, total_count

    def process_bulk_request(self, method, url, container, bulk_params):
        """
        Makes several requests in blocking or non-blocking fashion depending on the engine.

        :param string method: (required). HTTP verb to use for the request.
        :param string url: (required). URL of the request.
        :param string container: (required). Key in the response that should be used to access retrieved resources.
        :param list bulk_params: (required). Params that should be used for resource retrieval.
        """
        raise NotImplementedError

    def process_response(self, response):
        """
        Processes response received from Redmine.

        :param obj response: (required). Response object with response details.
        """
        if response.history:
            r = response.history[0]
            if r.is_redirect and r.request.url.startswith('http://') and response.request.url.startswith('https://'):
                raise exceptions.HTTPProtocolError

        status_code = response.status_code

        if status_code in (200, 201, 204):
            if self.return_raw_response:
                return response
            elif not response.content.strip():
                return True
            else:
                try:
                    return response.json()
                except (ValueError, TypeError):
                    raise exceptions.JSONDecodeError(response)
        elif status_code == 401:
            raise exceptions.AuthError
        elif status_code == 403:
            raise exceptions.ForbiddenError
        elif status_code == 404:
            raise exceptions.ResourceNotFoundError
        elif status_code == 409:
            raise exceptions.ConflictError
        elif status_code == 412:
            raise exceptions.ImpersonateError
        elif status_code == 413:
            raise exceptions.RequestEntityTooLargeError
        elif status_code == 422:
            errors = response.json()['errors']
            raise exceptions.ValidationError(', '.join(': '.join(e) if isinstance(e, list) else e for e in errors))
        elif status_code == 500:
            raise exceptions.ServerError

        raise exceptions.UnknownError(status_code)
