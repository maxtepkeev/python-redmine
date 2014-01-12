from distutils.version import LooseVersion
from redmine.resultsets import ResourceSet
from redmine.exceptions import (
    ResourceError,
    ResourceBadMethodError,
    ResourceFilterError,
    ResourceNoFiltersProvidedError,
    ResourceNoFieldsProvidedError,
    ResourceVersionMismatchError
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

        if redmine.ver is not None and LooseVersion(str(redmine.ver)) < LooseVersion(resource_class.version):
            raise ResourceVersionMismatchError()

        self.redmine = redmine
        self.resource_class = resource_class

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

                    results.extend(response[self.container])
                    self.params['limit'] -= 100
                    self.params['offset'] += 100

            return results

        return self.redmine.request('get', self.url, params=self.params)[self.container]

    def to_resource(self, resource):
        """Converts a single resource dict from Redmine result set to resource object"""
        return self.resource_class(self, resource)

    def to_resource_set(self, resources):
        """Converts an iterable with resource dicts from Redmine result set to ResourceSet object"""
        return ResourceSet(self, resources)

    def get(self, resource_id, **params):
        """Returns a Resource object directly by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_one is None or self.resource_class.container_one is None:
            raise ResourceBadMethodError()

        self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_one.format(resource_id, **params))
        self.params = params
        self.container = self.resource_class.container_one

        try:
            return self.resource_class(self, self.retrieve())
        except TypeError:
            return None

    def all(self, **params):
        """Returns a ResourceSet object with all Resource objects"""
        if self.resource_class.query_all is None or self.resource_class.container_all is None:
            raise ResourceBadMethodError()

        self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_all)
        self.params = params
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
            if self.resource_class.query_all is not None and self.resource_class.container_all is not None:
                self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_all)
                self.container = self.resource_class.container_all
            else:
                raise ResourceFilterError()

        self.params = filters
        return ResourceSet(self)

    def create(self, **fields):
        """Creates a new resource in Redmine database and returns resource object on success"""
        if self.resource_class.query_create is None or self.resource_class.container_create is None:
            raise ResourceBadMethodError()

        if not fields:
            raise ResourceNoFieldsProvidedError

        self.container = self.resource_class.container_one
        url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_create)
        container = self.resource_class.container_create
        resource = self.redmine.request('post', url, data={container: fields})[self.container]
        self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_one.format(resource['id']))
        return self.resource_class(self, resource)
