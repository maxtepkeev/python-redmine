"""
Provides public API.
"""

import os
import inspect
import contextlib

from distutils.version import LooseVersion

from . import managers, exceptions, engines, utilities, resources
from .version import __version__


class Redmine(object):
    """
    Entry point for all requests.
    """
    def __init__(self, url, **kwargs):
        """
        :param string url: (required). Redmine location.
        :param string key: (optional). API key used for authentication.
        :param string version: (optional). Redmine version.
        :param string username: (optional). Username used for authentication.
        :param string password: (optional). Password used for authentication.
        :param dict requests: (optional). Connection options.
        :param string impersonate: (optional). Username to impersonate.
        :param string date_format: (optional). Formatting directives for date format.
        :param string datetime_format: (optional). Formatting directives for datetime format.
        :param raise_attr_exception: (optional). Control over resource attribute access exception raising.
        :type raise_attr_exception: bool or tuple
        :param resource_paths: (optional). Paths to modules which contain additional resources.
        :type resource_paths: list or tuple
        :param cls engine: (optional). Engine that will be used to make requests to Redmine.
        """
        self.url = url.rstrip('/')
        self.ver = kwargs.get('version', None)
        self.date_format = kwargs.get('date_format', '%Y-%m-%d')
        self.datetime_format = kwargs.get('datetime_format', '%Y-%m-%dT%H:%M:%SZ')
        self.raise_attr_exception = kwargs.get('raise_attr_exception', True)
        self.resource_paths = kwargs.get('resource_paths', ())

        engine = kwargs.get('engine', engines.DefaultEngine)

        if not inspect.isclass(engine) or not issubclass(engine, engines.BaseEngine):
            raise exceptions.EngineClassError

        self.engine = engine(**kwargs)

    def __getattr__(self, resource_name):
        """
        Returns either ResourceSet or Resource object depending on the method used on the ResourceManager.

        :param string resource_name: (required). Resource name.
        """
        if resource_name.startswith('_'):
            raise AttributeError

        return managers.ResourceManager(self, resource_name)

    @contextlib.contextmanager
    def session(self, **options):
        """
        Initiates a temporary session with a copy of the current engine but with new options.

        :param dict options: (optional). Engine's options for a session.
        """
        engine = self.engine
        self.engine = engine.__class__(
            requests=utilities.merge_dicts(engine.requests, options.pop('requests', {})), **options)
        yield self
        self.engine = engine

    def upload(self, filepath):
        """
        Uploads file from filepath to Redmine and returns an assigned token.

        :param string filepath: (required). Path to the file that will be uploaded.
        """
        if self.ver is not None and LooseVersion(str(self.ver)) < LooseVersion('1.4.0'):
            raise exceptions.VersionMismatchError('File uploading')

        if not os.path.isfile(filepath) or os.path.getsize(filepath) == 0:
            raise exceptions.NoFileError

        with open(filepath, 'rb') as stream:
            url = '{0}/uploads.json'.format(self.url)
            headers = {'Content-Type': 'application/octet-stream'}
            response = self.engine.request('post', url, data=stream, headers=headers)

        return response['upload']['token']

    def download(self, url, savepath=None, filename=None, params=None):
        """
        Downloads file from Redmine and saves it to savepath or returns a response directly
        for maximum control over file processing.

        :param string url: (required). URL of the file that will be downloaded.
        :param string savepath: (optional). Path where to save the file.
        :param string filename: (optional). Name that will be used for the file.
        :param dict params: (optional). Params to send in the query string.
        """
        response = self.engine.request('get', url, params=dict(params or {}, **{'stream': True}), return_raw=True)

        # If a savepath wasn't provided we return a response directly
        # so a user can have maximum control over response data
        if savepath is None:
            return response

        try:
            from urlparse import urlsplit
        except ImportError:
            from urllib.parse import urlsplit

        if filename is None:
            filename = urlsplit(url)[2].split('/')[-1]

            if not filename:
                raise exceptions.FileUrlError

        savepath = os.path.join(savepath, filename)

        with open(savepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)

        return savepath

    def auth(self):
        """
        Shortcut for the case if we just want to check if user provided valid auth credentials.
        """
        return self.user.get('current')

    def search(self, query, **options):
        """
        Interface to Redmine Search API

        :param string query: (required). What to search.
        :param dict options: (optional). Dictionary of search options.
        """
        if self.ver is not None and LooseVersion(str(self.ver)) < LooseVersion('3.0.0'):
            raise exceptions.VersionMismatchError('Search functionality')

        container_map, manager_map, results = {}, {}, {'unknown': {}}

        for resource in options.pop('resources', []):
            options[resource] = True

        options['q'] = query

        for name, details in resources.registry.items():
            if details['class'].search_hints is not None:
                for hint in details['class'].search_hints:
                    container_map[hint] = details['class'].container_many

                manager_map[details['class'].container_many] = getattr(self, name)

        raw_resources, _ = self.engine.bulk_request('get', '{0}/search.json'.format(self.url), 'results', **options)

        for resource in raw_resources:
            if resource['type'] in container_map:
                container = container_map[resource['type']]

                if container not in results:
                    results[container] = []

                results[container].append(resource)
            else:
                if resource['type'] not in results['unknown']:
                    results['unknown'][resource['type']] = []

                results['unknown'][resource['type']].append(resource)

            del resource['type']  # all resources are already sorted by type so we don't need it

        if not results['unknown']:
            del results['unknown']

        for container in results:
            if container in manager_map:
                results[container] = manager_map[container].to_resource_set(results[container])

        return results or None
