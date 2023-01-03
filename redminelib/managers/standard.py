"""
Defines standard Redmine resources managers.
"""

from . import ResourceManager
from .. import exceptions


class ProjectManager(ResourceManager):
    def __getattr__(self, attr):
        if attr in ('close', 'reopen', 'archive', 'unarchive'):
            if self.redmine.ver is not None and self.redmine.ver < (5, 0, 0):
                raise exceptions.VersionMismatchError(f'Project {attr}')

            return lambda resource_id: self.redmine.engine.request(
                'put', f'{self.redmine.url}{self.resource_class.query_one.format(resource_id)[:-5]}/{attr}.json')

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{attr}'")


class FileManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            response = {self.container: {'id': int(request[self.container]['token'].split('.')[0])}}

        return super()._process_create_response(request, response)


class WikiPageManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            raise exceptions.ValidationError('Resource already exists')  # issue #182

        return super()._process_create_response(request, response)


class UserManager(ResourceManager):
    @staticmethod
    def _check_custom_url(path):
        if path.endswith('/me.json'):
            path = '/my/account.json'

        return path

    def _construct_get_url(self, path):
        return super()._construct_get_url(self._check_custom_url(path))

    def _prepare_create_request(self, request):
        request = super()._prepare_create_request(request)
        request['send_information'] = request[self.container].pop('send_information', False)
        return request

    def _construct_update_url(self, path):
        return super()._construct_update_url(self._check_custom_url(path))

    def _prepare_update_request(self, request):
        request = super()._prepare_update_request(request)
        request['send_information'] = request[self.resource_class.container_update].pop('send_information', False)
        return request


class NewsManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            response = {self.container: self.redmine.news.filter(**self.params)[0].raw()}

        return super()._process_create_response(request, response)
