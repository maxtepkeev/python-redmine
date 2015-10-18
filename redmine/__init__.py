import os
import json

from distutils.version import LooseVersion

from .packages import requests
from .version import __version__
from .managers import ResourceManager
from .utilities import is_string, to_string
from .exceptions import (
    AuthError,
    ConflictError,
    ImpersonateError,
    ServerError,
    ValidationError,
    NoFileError,
    FileUrlError,
    VersionMismatchError,
    ResourceNotFoundError,
    RequestEntityTooLargeError,
    UnknownError,
    ForbiddenError,
    JSONDecodeError
)


class Redmine(object):
    """An entry point for all requests"""
    def __init__(self, url, **kwargs):
        self.url = url.rstrip('/')
        self.key = kwargs.get('key', None)
        self.ver = kwargs.get('version', None)
        self.username = kwargs.get('username', None)
        self.password = kwargs.get('password', None)
        self.requests = kwargs.get('requests', {})
        self.impersonate = kwargs.get('impersonate', None)
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.datetime_format = kwargs.get('datetime_format', '%Y-%m-%dT%H:%M:%SZ')
        self.raise_attr_exception = kwargs.get('raise_attr_exception', True)
        self.custom_resource_paths = kwargs.get('custom_resource_paths', None)

    def __getattr__(self, resource):
        """Returns either ResourceSet or Resource object depending on the method used on the ResourceManager"""
        if resource.startswith('_'):
            raise AttributeError

        return ResourceManager(self, resource)

    def upload(self, filepath):
        """Uploads file from filepath to Redmine and returns an assigned token"""
        if self.ver is not None and LooseVersion(str(self.ver)) < LooseVersion('1.4.0'):
            raise VersionMismatchError('File upload')

        try:
            with open(filepath, 'rb') as stream:
                url = '{0}{1}'.format(self.url, '/uploads.json')
                response = self.request('post', url, data=stream, headers={'Content-Type': 'application/octet-stream'})
        except IOError:
            raise NoFileError

        return response['upload']['token']

    def download(self, url, savepath=None, filename=None):
        """Downloads file from Redmine and saves it to savepath or returns it as bytes"""
        self.requests['stream'] = True   # We don't want to load the entire file into memory
        response = self.request('get', url, raw_response=True)
        self.requests['stream'] = False  # Return back this setting for all usual requests

        # If a savepath wasn't provided we return an iter_content method
        # so a user can call it with the desired parameters for maximum
        # control and iterate over the response data
        if savepath is None:
            return response.iter_content

        try:
            from urlparse import urlsplit
        except ImportError:
            from urllib.parse import urlsplit

        if filename is None:
            filename = urlsplit(url)[2].split('/')[-1]

            if not filename:
                raise FileUrlError

        savepath = os.path.join(savepath, filename)

        with open(savepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return savepath

    def auth(self):
        """Shortcut for the case if we just want to check if user provided valid auth credentials"""
        return self.user.get('current')

    def request(self, method, url, headers=None, params=None, data=None, raw_response=False):
        """Makes requests to Redmine and returns result in json format"""
        kwargs = dict(self.requests, **{
            'headers': headers or {},
            'params': params or {},
            'data': data or {},
        })

        if 'Content-Type' not in kwargs['headers'] and method in ('post', 'put'):
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
            if raw_response:
                return response
            elif not response.content.strip():
                return True
            else:
                try:
                    return response.json()
                except (ValueError, TypeError):
                    raise JSONDecodeError(response)
        elif response.status_code == 401:
            raise AuthError
        elif response.status_code == 403:
            raise ForbiddenError
        elif response.status_code == 404:
            raise ResourceNotFoundError
        elif response.status_code == 409:
            raise ConflictError
        elif response.status_code == 412 and self.impersonate is not None:
            raise ImpersonateError
        elif response.status_code == 413:
            raise RequestEntityTooLargeError
        elif response.status_code == 422:
            errors = response.json()['errors']
            raise ValidationError(to_string(', '.join(e if is_string(e) else ': '.join(e) for e in errors)))
        elif response.status_code == 500:
            raise ServerError

        raise UnknownError(response.status_code)
