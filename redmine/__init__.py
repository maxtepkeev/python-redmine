import requests
from redmine.managers import ResourceManager
from redmine.exceptions import AuthError, ImpersonateError


class Redmine(object):
    """An entry point for all requests"""
    def __init__(self, url, **kwargs):
        self.url = url
        self.key = kwargs.get('key', None)
        self.ver = kwargs.get('version', None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.impersonate = kwargs.get('impersonate', None)
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.datetime_format = kwargs.get('datetime_format', '%Y-%m-%dT%H:%M:%SZ')

    def __getattr__(self, resource):
        """Returns either ResourceSet or Resource object depending on the method used on the ResourceManager"""
        return ResourceManager(self, resource)

    def request(self, method, url, **params):
        """Makes requests to Redmine and returns result in json format"""
        kwargs = {
            'headers': {},
            'params': params,
        }

        if self.impersonate is not None:
            kwargs['headers']['X-Redmine-Switch-User'] = self.impersonate

        # We would like to be authenticated by API key by default
        if 'key' not in kwargs['params'] and self.key is not None:
            kwargs['params']['key'] = self.key
        else:
            kwargs['auth'] = (self.username, self.password)

        response = getattr(requests, method)(url, **kwargs)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            raise AuthError()
        elif response.status_code == 412 and self.impersonate is not None:
            raise ImpersonateError()

        return None
