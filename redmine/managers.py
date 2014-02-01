from distutils.version import LooseVersion
from redmine.resultsets import ResourceSet
from redmine.utilities import MemorizeFormatter
from redmine.exceptions import (
    ResourceError,
    ResourceBadMethodError,
    ResourceFilterError,
    ResourceNoFiltersProvidedError,
    ResourceNoFieldsProvidedError,
    ResourceVersionMismatchError,
    ResourceNotFoundError,
    ValidationError
)


class ResourceManager(object):
    """Manages the behaviour of Redmine resources"""
    url = ''
    params = {}
    container = None

    def __init__(self, redmine, resource_name):
        """Accepts redmine instance object and tries to import the needed resource by resource name"""
        resource_name = ''.join(word[0].upper() + word[1:] for word in resource_name.split('_'))

        try:
            resource_class = getattr(__import__('redmine.resources', fromlist=[resource_name]), resource_name)
        except AttributeError:
            raise ResourceError()

        if redmine.ver is not None and LooseVersion(str(redmine.ver)) < LooseVersion(resource_class.redmine_version):
            raise ResourceVersionMismatchError()

        self.redmine = redmine
        self.resource_class = resource_class
        self.total_count = 0

    def retrieve(self, **params):
        """A proxy for Redmine object request which does some extra work for resource retrieval"""
        self.params.update(**params)

        # Redmine allows us to only return 100 resources per request, so if
        # we want to get all or > 100 resources we need to do some extra work
        if 'limit' in self.params and not 0 < self.params['limit'] <= 100:
            results = []
            self.params['offset'] = self.params.get('offset', 0)

            # we want to get all resources
            if self.params['limit'] == 0:
                self.params['limit'] = 100

                while True:
                    response = self.redmine.request('get', self.url, params=self.params)
                    
                    if response is None:
                        break
                    
                    self.total_count = response.get('total_count', 0)

                    results.extend(response[self.container])
                    self.params['offset'] += self.params['limit']

                    if response.get('total_count', 0) <= self.params['offset']:
                        break
            # we want to get > 100 resources
            else:
                while self.params['limit'] > 0:
                    response = self.redmine.request('get', self.url, params=self.params)
                    
                    if response is None:
                        break
                    
                    self.total_count = response.get('total_count', 0)

                    results.extend(response[self.container])
                    self.params['limit'] -= 100
                    self.params['offset'] += 100

            return results

        data = self.redmine.request('get', self.url, params=self.params)[self.container]
        self.total_count = data.get('total_count', 0)
        return data

    def to_resource(self, resource):
        """Converts a single resource dict from Redmine result set to resource object"""
        return self.resource_class(self, resource)

    def to_resource_set(self, resources):
        """Converts an iterable with resource dicts from Redmine result set to ResourceSet object"""
        return ResourceSet(self, resources)

    def new(self):
        """Returns new empty resource"""
        return self.to_resource({})

    def get(self, resource_id, **params):
        """Returns a Resource object directly by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_one is None or self.resource_class.container_one is None:
            raise ResourceBadMethodError()

        try:
            self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_one.format(resource_id, **params))
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        self.params = self.resource_class.translate_params(params)
        self.container = self.resource_class.container_one
        return self.resource_class(self, self.retrieve())

    def all(self, **params):
        """Returns a ResourceSet object with all Resource objects"""
        if self.resource_class.query_all is None or self.resource_class.container_all is None:
            raise ResourceBadMethodError()

        self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_all)
        self.params = self.resource_class.translate_params(params)
        self.container = self.resource_class.container_all
        return ResourceSet(self)

    def filter(self, **filters):
        """Returns a ResourceSet object with Resource objects filtered by a dict of filters"""
        if self.resource_class.query_filter is None or self.resource_class.container_filter is None:
            raise ResourceBadMethodError()

        if not filters:
            raise ResourceNoFiltersProvidedError()

        try:
            self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_filter.format(**filters))
            self.container = self.resource_class.container_filter.format(**filters)
        except KeyError:
            raise ResourceFilterError()

        self.params = self.resource_class.translate_params(filters)
        return ResourceSet(self)

    def create(self, **fields):
        """Creates a new resource in Redmine database and returns resource object on success"""
        if self.resource_class.query_create is None or self.resource_class.container_create is None:
            raise ResourceBadMethodError()

        if not fields:
            raise ResourceNoFieldsProvidedError

        if 'uploads' in fields:
            for index, upload in enumerate(fields['uploads']):
                fields['uploads'][index]['token'] = self.redmine.upload(upload.get('path', ''))

        formatter = MemorizeFormatter()

        try:
            url = '{0}{1}'.format(self.redmine.url, formatter.format(self.resource_class.query_create, **fields))
        except KeyError as exception:
            raise ValidationError('{0} field is required'.format(exception))

        self.container = self.resource_class.container_one
        data = {self.resource_class.container_create: formatter.unused_kwargs}

        # Almost all resources are created via POST method, but some
        # resources are created via PUT, so we should check for this
        try:
            response = self.redmine.request('post', url, data=data)
        except ResourceNotFoundError:
            response = self.redmine.request('put', url, data=data)

        try:
            resource = self.to_resource(response[self.container])
        except TypeError:
            raise ValidationError('Resource already exists')  # fix for repeated PUT requests

        self.params = formatter.used_kwargs
        self.url = '{0}{1}'.format(
            self.redmine.url,
            self.resource_class.query_one.format(resource.internal_id, **fields)
        )
        return resource

    def update(self, resource_id, **fields):
        """Updates a Resource object by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_update is None or self.resource_class.container_update is None:
            raise ResourceBadMethodError()

        if not fields:
            raise ResourceNoFieldsProvidedError

        formatter = MemorizeFormatter()

        try:
            query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
        except KeyError as exception:
            param = str(exception).replace("'", "")

            if param in self.params:
                fields[param] = self.params[param]
                query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
            else:
                raise ValidationError('{0} argument is required'.format(exception))

        url = '{0}{1}'.format(self.redmine.url, query_update)
        data = {self.resource_class.container_update: formatter.unused_kwargs}
        return self.redmine.request('put', url, data=data)

    def delete(self, resource_id, **params):
        """Deletes a Resource object by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_delete is None:
            raise ResourceBadMethodError()

        try:
            url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_delete.format(resource_id, **params))
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        return self.redmine.request('delete', url, params=params)
