from distutils.version import LooseVersion

from .resultsets import ResourceSet
from .utilities import MemorizeFormatter
from .exceptions import (
    ResourceError,
    ResourceBadMethodError,
    ResourceFilterError,
    ResourceNoFiltersProvidedError,
    ResourceNoFieldsProvidedError,
    ResourceVersionMismatchError,
    ResourceNotFoundError,
    ValidationError,
    ResourceRequirementsError
)


class ResourceManager(object):
    """
    Manages Redmine resource defined by the resource_name with the help of redmine instance object.
    """
    url = ''
    params = {}
    container = None

    def __init__(self, redmine, resource_name, **params):
        """
        :param redmine.Redmine redmine: (required). Redmine instance object.
        :param str resource_name: (required). Resource name.
        :param dict params: (optional). Parameters used for resources retrieval.
        """
        resource_class = None
        resource_name = ''.join(word[0].upper() + word[1:] for word in resource_name.split('_'))
        resource_paths = tuple((redmine.custom_resource_paths or ())) + ('redmine.resources',)

        for path in resource_paths:
            try:
                resource_class = getattr(__import__(path, fromlist=[resource_name]), resource_name)
                break
            except (ImportError, AttributeError):
                continue

        if resource_class is None:
            raise ResourceError

        if redmine.ver is not None and LooseVersion(str(redmine.ver)) < LooseVersion(resource_class.redmine_version):
            raise ResourceVersionMismatchError

        self.redmine = redmine
        self.resource_class = resource_class
        self.params = params

    def retrieve(self, **params):
        """
        A proxy for redmine.Redmine.request() which does some extra work for resource retrieval.

        :param dict params: (optional). Parameters used for resource retrieval.
        """
        self.params.update(**params)

        results = []
        total_count = 0
        limit = self.params.get('limit', 0)
        offset = self.params.get('offset', 0)

        if limit == 0:
            limit = 100

        while True:
            try:
                response = self.redmine.request('get', self.url, params=dict(self.params, limit=limit, offset=offset))
            except ResourceNotFoundError:
                # This is the only place we're checking for ResourceRequirementsError
                # because for some POST/PUT/DELETE requests Redmine may also return 404
                # status code instead of 405 which can lead us to improper decisions
                if self.resource_class.requirements:
                    raise ResourceRequirementsError(self.resource_class.requirements)

                raise ResourceNotFoundError

            # A single resource was requested via get()
            if isinstance(response[self.container], dict):
                results = response[self.container]
                total_count = 1
                break

            # Resource supports limit/offset on Redmine level
            if all(response.get(param) is not None for param in ('total_count', 'limit', 'offset')):
                total_count = response['total_count']
                results.extend(response[self.container])

                # We want to get all resources
                if self.params.get('limit', 0) == 0:
                    offset += limit

                    if total_count <= offset:
                        break
                # We want to get only some resources
                else:
                    limit -= 100
                    offset += 100

                    if limit <= 0:
                        break
            # We have to mimic limit/offset if a resource
            # doesn't support this feature on Redmine level
            else:
                total_count = len(response[self.container])
                results = response[self.container][offset:None if self.params.get('limit', 0) == 0 else limit + offset]
                break

        return results, total_count

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
        return ResourceSet(self, resources)

    def new(self):
        """
        Returns new empty Resource object.
        """
        return self.to_resource({})

    def new_manager(self, resource_name, **params):
        """
        Returns new ResourceManager instance object.

        :param str resource_name: (required). Resource name.
        :param dict params: (optional). Parameters used for resources retrieval.
        """
        return ResourceManager(self.redmine, resource_name, **params)

    def get(self, resource_id, **params):
        """
        Returns a Resource object from Redmine by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or str
        :param dict params: (optional). Parameters used for resource retrieval.
        """
        if self.resource_class.query_one is None or self.resource_class.container_one is None:
            raise ResourceBadMethodError

        try:
            self.url = self.redmine.url + self.resource_class.query_one.format(resource_id, **params)
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_one
        return self.resource_class(self, self.retrieve()[0])

    def all(self, **params):
        """
        Returns a ResourceSet object with all Resource objects.

        :param dict params: (optional). Parameters used for resources retrieval.
        """
        if self.resource_class.query_all is None or self.resource_class.container_many is None:
            raise ResourceBadMethodError

        self.url = self.redmine.url + self.resource_class.query_all
        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_many
        return ResourceSet(self)

    def filter(self, **filters):
        """
        Returns a ResourceSet object with Resource objects filtered by a dict of filters.

        :param dict filters: (optional). Filters used for resources retrieval.
        """
        if self.resource_class.query_filter is None or self.resource_class.container_many is None:
            raise ResourceBadMethodError

        if not filters:
            raise ResourceNoFiltersProvidedError

        try:
            self.url = self.redmine.url + self.resource_class.query_filter.format(**filters)
            self.container = self.resource_class.container_many.format(**filters)
        except KeyError:
            raise ResourceFilterError

        self.params = self.resource_class.bulk_decode(filters, self)
        return ResourceSet(self)

    def create(self, **fields):
        """
        Creates a new resource in Redmine and returns created Resource object on success.

        :param dict fields: (optional). Fields used for resource creation.
        """
        if self.resource_class.query_create is None or self.resource_class.container_one is None:
            raise ResourceBadMethodError

        if not fields:
            raise ResourceNoFieldsProvidedError

        formatter = MemorizeFormatter()

        try:
            url = self.redmine.url + formatter.format(self.resource_class.query_create, **fields)
        except KeyError as exception:
            raise ValidationError('{0} field is required'.format(exception))

        self.container = self.resource_class.container_one
        data = {self.resource_class.container_one: self.resource_class.bulk_decode(formatter.unused_kwargs, self)}

        if 'uploads' in data[self.resource_class.container_one]:
            data['attachments'] = data[self.resource_class.container_one].pop('uploads')
            for index, attachment in enumerate(data['attachments']):
                data['attachments'][index]['token'] = self.redmine.upload(attachment.get('path', ''))

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
        self.url = self.redmine.url + self.resource_class.query_one.format(resource.internal_id, **fields)
        return resource

    def update(self, resource_id, **fields):
        """
        Updates a Resource object by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or str
        :param dict fields: (optional). Fields which will be updated for the resource.
        """
        if self.resource_class.query_update is None or self.resource_class.container_one is None:
            raise ResourceBadMethodError

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

        url = self.redmine.url + query_update
        data = {self.resource_class.container_one: self.resource_class.bulk_decode(formatter.unused_kwargs, self)}

        if 'uploads' in data[self.resource_class.container_one]:
            data['attachments'] = data[self.resource_class.container_one].pop('uploads')
            for index, attachment in enumerate(data['attachments']):
                data['attachments'][index]['token'] = self.redmine.upload(attachment.get('path', ''))

        return self.redmine.request('put', url, data=data)

    def delete(self, resource_id, **params):
        """
        Deletes a Resource object by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or str
        :param dict params: (optional). Parameters used for resource deletion.
        """
        if self.resource_class.query_delete is None:
            raise ResourceBadMethodError

        try:
            url = self.redmine.url + self.resource_class.query_delete.format(resource_id, **params)
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        return self.redmine.request('delete', url, params=self.resource_class.bulk_decode(params, self))
