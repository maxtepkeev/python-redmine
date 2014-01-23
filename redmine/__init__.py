import json
import requests
from distutils.version import LooseVersion
from redmine.managers import ResourceManager
from redmine.utilities import to_string
from redmine.exceptions import (
    AuthError,
    ConflictError,
    ImpersonateError,
    ServerError,
    ValidationError,
    NoFileError,
    VersionMismatchError,
    ResourceNotFoundError
)


class Redmine(object):
    """An entry point for all requests"""
    def __init__(self, url, **kwargs):
        self.url = url
        self.key = kwargs.get('key', None)
        self.ver = kwargs.get('version', None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.requests = kwargs.get('requests', {})
        self.impersonate = kwargs.get('impersonate', None)
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.datetime_format = kwargs.get('datetime_format', '%Y-%m-%dT%H:%M:%SZ')

    def __getattr__(self, resource):
        """Returns either ResourceSet or Resource object depending on the method used on the ResourceManager"""
        return ResourceManager(self, resource)

    def upload(self, filepath):
        """Uploads file from filepath to Redmine and returns an assigned token"""
        if self.ver is not None and LooseVersion(str(self.ver)) < LooseVersion('1.4.0'):
            raise VersionMismatchError('File upload')

        try:
            with open(filepath) as stream:
                url = '{0}{1}'.format(self.url, '/uploads.json')
                response = self.request('post', url, data=stream, headers={'Content-Type': 'application/octet-stream'})
        except IOError:
            raise NoFileError()

        return response['upload']['token']

    def request(self, method, url, headers=None, params=None, data=None):
        """Makes requests to Redmine and returns result in json format"""
        kwargs = dict(self.requests, **{
            'headers': headers or {},
            'params': params or {},
            'data': data or {},
        })

        if not 'Content-Type' in kwargs['headers'] and method in ('post', 'put'):
            kwargs['data'] = json.dumps(data)
            kwargs['headers']['Content-Type'] = 'application/json'

        if self.impersonate is not None:
            kwargs['headers']['X-Redmine-Switch-User'] = self.impersonate

        # We would like to be authenticated by API key by default
        if 'key' not in kwargs['params'] and self.key is not None:
            kwargs['params']['key'] = self.key
        else:
            kwargs['auth'] = (self.username, self.password)

        response = getattr(requests, method)(url, **kwargs)

        if response.status_code in (200, 201):
            if response.status_code == 200 and method in ('put', 'delete'):
                return True
            return response.json()
        elif response.status_code == 401:
            raise AuthError()
        elif response.status_code == 404:
            raise ResourceNotFoundError
        elif response.status_code == 409:
            raise ConflictError
        elif response.status_code == 412 and self.impersonate is not None:
            raise ImpersonateError()
        elif response.status_code == 422:
            raise ValidationError(to_string(', '.join(response.json()['errors'])))
        elif response.status_code == 500:
            raise ServerError()

        return None
