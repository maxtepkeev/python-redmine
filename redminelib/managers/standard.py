"""
Defines standard Redmine resources managers.
"""

from . import ResourceManager
from .. import exceptions


class WikiPageManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            raise exceptions.ValidationError('Resource already exists')  # issue #182

        return super(WikiPageManager, self)._process_create_response(request, response)


class FileManager(ResourceManager):
    def _process_create_response(self, request, response):
        if response is True:
            response = {self.container: {'id': int(request[self.container]['token'].split('.')[0])}}

        return super(FileManager, self)._process_create_response(request, response)
