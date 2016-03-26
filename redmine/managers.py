import datetime

from distutils.version import LooseVersion

from .resultsets import ResourceSet
from .utilities import MemorizeFormatter, is_unicode, to_string
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
    """Manages the behaviour of Redmine resources"""
    url = ''
    params = {}
    container = None

    def __init__(self, redmine, resource_name):
        """Accepts redmine instance object and tries to import the needed resource by resource name"""
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

    def retrieve(self, **params):
        """A proxy for Redmine object request which does some extra work for resource retrieval"""
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
            raise ResourceBadMethodError

        if is_unicode(resource_id):
            resource_id = to_string(resource_id)

        try:
            self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_one.format(resource_id, **params))
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        self.params = self.prepare_params(params)
        self.container = self.resource_class.container_one
        return self.resource_class(self, self.retrieve()[0])

    def all(self, **params):
        """Returns a ResourceSet object with all Resource objects"""
        if self.resource_class.query_all is None or self.resource_class.container_all is None:
            raise ResourceBadMethodError

        self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_all)
        self.params = self.prepare_params(params)
        self.container = self.resource_class.container_all
        return ResourceSet(self)

    def filter(self, **filters):
        """Returns a ResourceSet object with Resource objects filtered by a dict of filters"""
        if self.resource_class.query_filter is None or self.resource_class.container_filter is None:
            raise ResourceBadMethodError

        if not filters:
            raise ResourceNoFiltersProvidedError

        try:
            self.url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_filter.format(**filters))
            self.container = self.resource_class.container_filter.format(**filters)
        except KeyError:
            raise ResourceFilterError

        self.params = self.prepare_params(filters)
        return ResourceSet(self)

    def create(self, **fields):
        """Creates a new resource in Redmine database and returns resource object on success"""
        if self.resource_class.query_create is None or self.resource_class.container_create is None:
            raise ResourceBadMethodError

        if not fields:
            raise ResourceNoFieldsProvidedError

        formatter = MemorizeFormatter()

        title = fields.get('title')
        if title is not None and is_unicode(title):
            fields['title'] = to_string(title)

        try:
            url = '{0}{1}'.format(self.redmine.url, formatter.format(self.resource_class.query_create, **fields))
        except KeyError as exception:
            raise ValidationError('{0} field is required'.format(exception))

        self.container = self.resource_class.container_one
        data = {self.resource_class.container_create: self.prepare_params(formatter.unused_kwargs)}

        if 'uploads' in data[self.resource_class.container_create]:
            data['attachments'] = data[self.resource_class.container_create].pop('uploads')
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
        self.url = '{0}{1}'.format(
            self.redmine.url,
            self.resource_class.query_one.format(resource.internal_id, **fields)
        )
        return resource

    def update(self, resource_id, **fields):
        """Updates a Resource object by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_update is None or self.resource_class.container_update is None:
            raise ResourceBadMethodError

        if not fields:
            raise ResourceNoFieldsProvidedError

        formatter = MemorizeFormatter()

        if is_unicode(resource_id):
            resource_id = to_string(resource_id)

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
        data = {self.resource_class.container_update: self.prepare_params(formatter.unused_kwargs)}

        if 'uploads' in data[self.resource_class.container_update]:
            data['attachments'] = data[self.resource_class.container_update].pop('uploads')
            for index, attachment in enumerate(data['attachments']):
                data['attachments'][index]['token'] = self.redmine.upload(attachment.get('path', ''))

        return self.redmine.request('put', url, data=data)

    def delete(self, resource_id, **params):
        """Deletes a Resource object by resource id (can be either integer id or string identifier)"""
        if self.resource_class.query_delete is None:
            raise ResourceBadMethodError

        if is_unicode(resource_id):
            resource_id = to_string(resource_id)

        try:
            url = '{0}{1}'.format(self.redmine.url, self.resource_class.query_delete.format(resource_id, **params))
        except KeyError as exception:
            raise ValidationError('{0} argument is required'.format(exception))

        return self.redmine.request('delete', url, params=self.prepare_params(params))

    def prepare_params(self, params):
        """Prepares params so Redmine could understand them correctly"""
        for name, value in params.items():
            type_ = type(value)

            if type_ is datetime.date:
                params[name] = value.strftime(self.redmine.date_format)
            elif type_ is datetime.datetime:
                params[name] = value.strftime(self.redmine.datetime_format)

        return self.resource_class.translate_params(params)
