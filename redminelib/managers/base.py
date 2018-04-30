"""
Defines base Redmine resource manager class and it's infrastructure.
"""

from .. import utilities, resultsets, exceptions


class ResourceManager(object):
    """
    Manages given Redmine resource class with the help of redmine object.
    """
    def __init__(self, redmine, resource_class):
        """
        :param redmine.Redmine redmine: (required). Redmine object.
        :param resources.BaseResource resource_class: (required). Resource class.
        """
        self.url = ''
        self.params = {}
        self.container = None
        self.redmine = redmine
        self.resource_class = resource_class

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
        manager = getattr(self.redmine, resource_name)
        manager.params = params
        return manager

    def get(self, resource_id, **params):
        """
        Returns a Resource object from Redmine by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param dict params: (optional). Parameters used for resource retrieval.
        """
        if self.resource_class.query_one is None or self.resource_class.container_one is None:
            operation = self.all if self.resource_class.query_all else self.filter
            resource = operation(**params).get(resource_id, None)

            if resource is None:
                raise exceptions.ResourceNotFoundError

            return resource

        try:
            self.url = self.redmine.url + self.resource_class.query_one.format(resource_id, **params)
        except KeyError as exception:
            raise exceptions.ValidationError('{0} argument is required'.format(exception))

        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_one

        try:
            return self.to_resource(self.redmine.engine.request('get', self.url, params=self.params)[self.container])
        except exceptions.ResourceNotFoundError as e:
            if self.resource_class.requirements:
                raise exceptions.ResourceRequirementsError(self.resource_class.requirements)
            raise e

    def all(self, **params):
        """
        Returns a ResourceSet object with all Resource objects.

        :param dict params: (optional). Parameters used for resources retrieval.
        """
        if self.resource_class.query_all is None or self.resource_class.container_all is None:
            raise exceptions.ResourceBadMethodError

        self.url = self.redmine.url + self.resource_class.query_all
        self.params = self.resource_class.bulk_decode(params, self)
        self.container = self.resource_class.container_all
        return resultsets.ResourceSet(self)

    def filter(self, **filters):
        """
        Returns a ResourceSet object with Resource objects filtered by a dict of filters.

        :param dict filters: (optional). Filters used for resources retrieval.
        """
        if self.resource_class.query_filter is None or self.resource_class.container_filter is None:
            raise exceptions.ResourceBadMethodError

        if not filters:
            raise exceptions.ResourceNoFiltersProvidedError

        try:
            self.url = self.redmine.url + self.resource_class.query_filter.format(**filters)
            self.container = self.resource_class.container_filter.format(**filters)
        except KeyError:
            raise exceptions.ResourceFilterError

        self.params = self.resource_class.bulk_decode(filters, self)
        return resultsets.ResourceSet(self)

    def _construct_create_url(self, path):
        """
        Constructs URL for create method.

        :param string path: absolute URL path.
        """
        return self.redmine.url + path

    def _prepare_create_request(self, request):
        """
        Makes the necessary preparations for create request data.

        :param dict request: Request data.
        """
        return {self.container: self.resource_class.bulk_decode(request, self)}

    def create(self, **fields):
        """
        Creates a new resource in Redmine and returns created Resource object on success.

        :param dict fields: (optional). Fields used for resource creation.
        """
        if self.resource_class.query_create is None or self.resource_class.container_create is None:
            raise exceptions.ResourceBadMethodError

        if not fields:
            raise exceptions.ResourceNoFieldsProvidedError

        formatter = utilities.MemorizeFormatter()

        try:
            url = self._construct_create_url(formatter.format(self.resource_class.query_create, **fields))
        except KeyError as e:
            raise exceptions.ValidationError('{0} field is required'.format(e))

        self.params = formatter.used_kwargs
        self.container = self.resource_class.container_create
        request = self._prepare_create_request(formatter.unused_kwargs)
        response = self.redmine.engine.request(self.resource_class.http_method_create, url, data=request)
        resource = self._process_create_response(request, response)
        self.url = self.redmine.url + self.resource_class.query_one.format(resource.internal_id, **fields)
        return resource

    def _process_create_response(self, request, response):
        """
        Processes create response and constructs resource object.

        :param dict request: Original request data.
        :param any response: Response received from Redmine for this request data.
        """
        return self.to_resource(response[self.container])

    def _construct_update_url(self, path):
        """
        Constructs URL for update method.

        :param string path: absolute URL path.
        """
        return self.redmine.url + path

    def _prepare_update_request(self, request):
        """
        Makes the necessary preparations for update request data.

        :param dict request: Request data.
        """
        return {self.resource_class.container_update: self.resource_class.bulk_decode(request, self)}

    def update(self, resource_id, **fields):
        """
        Updates a Resource object by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param dict fields: (optional). Fields that will be updated for the resource.
        """
        if self.resource_class.query_update is None or self.resource_class.container_update is None:
            raise exceptions.ResourceBadMethodError

        if not fields:
            raise exceptions.ResourceNoFieldsProvidedError

        formatter = utilities.MemorizeFormatter()

        try:
            query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
        except KeyError as e:
            param = e.args[0]

            if param in self.params:
                fields[param] = self.params[param]
                query_update = formatter.format(self.resource_class.query_update, resource_id, **fields)
            else:
                raise exceptions.ValidationError('{0} argument is required'.format(e))

        url = self._construct_update_url(query_update)
        request = self._prepare_update_request(formatter.unused_kwargs)
        response = self.redmine.engine.request(self.resource_class.http_method_update, url, data=request)
        return self._process_update_response(request, response)

    def _process_update_response(self, request, response):
        """
        Processes update response.

        :param dict request: Original request data.
        :param any response: Response received from Redmine for this request data.
        """
        return response

    def _construct_delete_url(self, path):
        """
        Constructs URL for delete method.

        :param string path: absolute URL path.
        """
        return self.redmine.url + path

    def _prepare_delete_request(self, request):
        """
        Makes the necessary preparations for delete request data.

        :param dict request: Request data.
        """
        return self.resource_class.bulk_decode(request, self)

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
            url = self._construct_delete_url(self.resource_class.query_delete.format(resource_id, **params))
        except KeyError as e:
            raise exceptions.ValidationError('{0} argument is required'.format(e))

        request = self._prepare_delete_request(params)
        response = self.redmine.engine.request(self.resource_class.http_method_delete, url, params=request)
        return self._process_delete_response(request, response)

    def _process_delete_response(self, request, response):
        """
        Processes delete response.

        :param dict request: Original request data.
        :param any response: Response received from Redmine for this request data.
        """
        return response

    def search(self, query, **options):
        """
        Searches for Resources using a query.

        :param string query: (required). What to search.
        :param dict options: (optional). Dictionary of search options.
        """
        if self.resource_class.search_hints is None:
            raise exceptions.ResourceBadMethodError

        container = self.resource_class.container_all or self.resource_class.container_filter
        results = self.redmine.search(query, **dict(resources=[container], **options))
        return results.get(container) if results is not None else results

    def __repr__(self):
        """
        Official representation of a ResourceManager object.
        """
        return '<redminelib.managers.{0} object for {1} resource>'.format(
            self.__class__.__name__, self.resource_class.__name__)
