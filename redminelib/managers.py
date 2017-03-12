"""
Defines manager classes.
"""

import sys

from distutils.version import LooseVersion

from . import utilities, resultsets, exceptions


class ResourceManager(object):
    """
    Manages Redmine resource defined by the resource_name with the help of redmine object.
    """
    def __init__(self, redmine, resource_name, **params):
        """
        :param redmine.Redmine redmine: (required). Redmine object.
        :param string resource_name: (required). Resource name.
        :param dict params: (optional). Parameters used for resources retrieval.
        """
        resource_class = None
        resource_name = ''.join(word[0].upper() + word[1:] for word in str(resource_name).split('_'))
        resource_paths = tuple(redmine.resource_paths) + (sys.modules[self.__module__].__package__ + '.resources',)

        for path in resource_paths:
            try:
                resource_class = getattr(__import__(path, fromlist=[resource_name]), resource_name)
                break
            except (ImportError, AttributeError):
                continue

        if resource_class is None:
            raise exceptions.ResourceError

        if redmine.ver is not None and LooseVersion(str(redmine.ver)) < LooseVersion(resource_class.redmine_version):
            raise exceptions.ResourceVersionMismatchError

        self.url = ''
        self.container = None
        self.params = params
        self.redmine = redmine
        self.resource_class = resource_class

    def request(self, is_bulk, **params):
        """
        Makes request(s) and additionally checks for resource specific stuff.

        :param bool is_bulk: (required). Whether this is a bulk or single request.
        :param dict params: (optional). Parameters used for resource retrieval.
        """
        try:
            if not is_bulk:
                return self.redmine.engine.request('get', self.url, params=params)[self.container]
            else:
                return self.redmine.engine.bulk_request('get', self.url, self.container, **self.params)
        except exceptions.ResourceNotFoundError as e:
            # This is the only place we're checking for ResourceRequirementsError
            # because for some POST/PUT/DELETE requests Redmine may also return 404
            # status code instead of 405 which can lead us to improper decisions
            if self.resource_class.requirements:
                raise exceptions.ResourceRequirementsError(self.resource_class.requirements)
            raise e

    def to_resource(self, resource):
        """
        Converts resource data to Resource object.

        :param dict resource: (required). Resource data.
        """
        return self.resource_class(self, resource)

    def to_resource_set(self, resources):
        """
        Converts an iterable with resources data to ResourceSet object.

        :param resources: (required). Resource data.
        :type resources: list or tuple
        """
        return resultsets.ResourceSet(self, resources)

    def new(self):
        """
        Returns new empty Resource object.
        """
        return self.to_resource({})

    def new_manager(self, resource_name, **params):
        """
        Returns new ResourceManager object.

        :param string resource_name: (required). Resource name.
        :param dict params: (optional). Parameters used for resources retrieval.
        """
        return ResourceManager(self.redmine, resource_name, **params)

    def get(self, resource_id, **params):
        """
        Returns a Resource object from Redmine by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param dict params: (optional). Parameters used for resource retrieval.
        """
        if self.resource_class.query_one is None or self.resource_class.container_one is None:
            raise exceptions.ResourceBadMethodError

        try:
            self.url = self.redmine.url + self.resource_class.query_one.format(resource_id, **params)
        except KeyError as exception:
            raise exceptions.ValidationError('{0} argument is required'.format(exception))

        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_one
        return self.to_resource(self.request(False, **self.params))

    def all(self, **params):
        """
        Returns a ResourceSet object with all Resource objects.

        :param dict params: (optional). Parameters used for resources retrieval.
        """
        if self.resource_class.query_all is None or self.resource_class.container_many is None:
            raise exceptions.ResourceBadMethodError

        self.url = self.redmine.url + self.resource_class.query_all
        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_many
        return resultsets.ResourceSet(self)

    def filter(self, **filters):
        """
        Returns a ResourceSet object with Resource objects filtered by a dict of filters.

        :param dict filters: (optional). Filters used for resources retrieval.
        """
        if self.resource_class.query_filter is None or self.resource_class.container_many is None:
            raise exceptions.ResourceBadMethodError

        if not filters:
            raise exceptions.ResourceNoFiltersProvidedError

        try:
            self.url = self.redmine.url + self.resource_class.query_filter.format(**filters)
            self.container = self.resource_class.container_many.format(**filters)
        except KeyError:
            raise exceptions.ResourceFilterError

        self.params = self.resource_class.bulk_decode(filters, self)
        return resultsets.ResourceSet(self)

    def create(self, **fields):
        """
        Creates a new resource in Redmine and returns created Resource object on success.

        :param dict fields: (optional). Fields used for resource creation.
        """
        if self.resource_class.query_create is None or self.resource_class.container_one is None:
            raise exceptions.ResourceBadMethodError

        if not fields:
            raise exceptions.ResourceNoFieldsProvidedError

        formatter = utilities.MemorizeFormatter()

        try:
            url = self.redmine.url + formatter.format(self.resource_class.query_create, **fields)
        except KeyError as exception:
            raise exceptions.ValidationError('{0} field is required'.format(exception))

        self.container = self.resource_class.container_one
        data = {self.resource_class.container_one: self.resource_class.bulk_decode(formatter.unused_kwargs, self)}

        if 'uploads' in data[self.resource_class.container_one]:
            data['attachments'] = data[self.resource_class.container_one].pop('uploads')
            for index, attachment in enumerate(data['attachments']):
                data['attachments'][index]['token'] = self.redmine.upload(attachment.get('path', ''))

        response = self.redmine.engine.request(self.resource_class.http_method_create, url, data=data)
        resource = self.to_resource(response[self.container])

        self.params = formatter.used_kwargs
        self.url = self.redmine.url + self.resource_class.query_one.format(resource.internal_id, **fields)
        return resource

    def update(self, resource_id, **fields):
        """
        Updates a Resource object by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param dict fields: (optional). Fields which will be updated for the resource.
        """
        if self.resource_class.query_update is None or self.resource_class.container_one is None:
            raise exceptions.ResourceBadMethodError

        if not fields:
            raise exceptions.ResourceNoFieldsProvidedError

        formatter = utilities.MemorizeFormatter()

        try:
            query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
        except KeyError as exception:
            param = exception.args[0]

            if param in self.params:
                fields[param] = self.params[param]
                query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
            else:
                raise exceptions.ValidationError('{0} argument is required'.format(exception))

        url = self.redmine.url + query_update
        data = {self.resource_class.container_one: self.resource_class.bulk_decode(formatter.unused_kwargs, self)}

        if 'uploads' in data[self.resource_class.container_one]:
            data['attachments'] = data[self.resource_class.container_one].pop('uploads')
            for index, attachment in enumerate(data['attachments']):
                data['attachments'][index]['token'] = self.redmine.upload(attachment.get('path', ''))

        return self.redmine.engine.request(self.resource_class.http_method_update, url, data=data)

    def delete(self, resource_id, **params):
        """
        Deletes a Resource object by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param dict params: (optional). Parameters used for resource deletion.
        """
        if self.resource_class.query_delete is None:
            raise exceptions.ResourceBadMethodError

        try:
            url = self.redmine.url + self.resource_class.query_delete.format(resource_id, **params)
        except KeyError as exception:
            raise exceptions.ValidationError('{0} argument is required'.format(exception))

        return self.redmine.engine.request(
            self.resource_class.http_method_delete, url, params=self.resource_class.bulk_decode(params, self))

    def search(self, query, **options):
        """
        Searches for Resources using a query.

        :param string query: (required). What to search.
        :param dict options: (optional). Dictionary of search options.
        """
        if self.resource_class.search_hints is None or self.resource_class.container_many is None:
            raise exceptions.ResourceBadMethodError

        results = self.redmine.search(query, **dict(resources=[self.resource_class.container_many], **options))
        return results.get(self.resource_class.container_many) if results is not None else results

    def __repr__(self):
        """
        Official representation of a ResourceManager object.
        """
        return '<{0}.{1} object for {2} resource>'.format(
            self.__class__.__module__, self.__class__.__name__, self.resource_class.__name__)
