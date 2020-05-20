"""
Defines standard Redmine resources managers.
"""

from . import ResourceManager
from .. import exceptions


class FileManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            response = {self.container: {'id': int(request[self.container]['token'].split('.')[0])}}

        return super(FileManager, self)._process_create_response(request, response)


class WikiPageManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            raise exceptions.ValidationError('Resource already exists')  # issue #182

        return super(WikiPageManager, self)._process_create_response(request, response)


class UserManager(ResourceManager):
    def _prepare_create_request(self, request):
        request = super(UserManager, self)._prepare_create_request(request)
        request['send_information'] = request[self.container].pop('send_information', False)
        return request

    def _prepare_update_request(self, request):
        request = super(UserManager, self)._prepare_update_request(request)
        request['send_information'] = request[self.resource_class.container_update].pop('send_information', False)
        return request


class NewsManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            response = {self.container: self.redmine.news.filter(**self.params)[0].raw()}

        return super(NewsManager, self)._process_create_response(request, response)
