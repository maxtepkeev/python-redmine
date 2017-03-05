"""
Defines ResourceSet objects that can be used to represent a set of resources.
"""

import itertools

from . import utilities, exceptions


class BaseResourceSet(object):
    """
    Defines basic functionality for a ResourceSet object.
    """
    def __init__(self, manager, resources=None, limit=0, offset=0, total_count=None):
        """
        :param managers.ResourceManager manager: (required). ResourceManager object.
        :param resources: (optional). Iterable of resources.
        :type resources: list or tuple
        :param int limit: (optional). Resource limit.
        :param int offset: (optional). Resource offset.
        :param int total_count: (optional). How many resources are there available in Redmine.
        """
        self.manager = manager
        self.limit = limit
        self.offset = offset
        self.resource_id_key = manager.resource_class.internal_id_key
        self._resources = resources
        self._total_count = total_count
        self._is_sliced = False

    @property
    def total_count(self):
        """
        Returns total count of available resources in Redmine, this is known only after ResourceSet evaluation.
        """
        if self._total_count is None:
            if self._resources is None:
                raise exceptions.ResultSetTotalCountError
            else:
                self._total_count = len(self)

        return self._total_count

    def export(self, fmt, savepath=None, filename=None):
        """
        Exports all resources from resource set to requested format if Resource supports that.

        :param string fmt: (required). Format to use for export, e.g. atom, csv, txt, pdf, html etc.
        :param string savepath: (optional). Path where to save the file.
        :param string filename: (optional). Name that will be used for the file.
        """
        if self.manager.resource_class.query_all_export is None:
            raise exceptions.ExportNotSupported

        formatter = utilities.MemorizeFormatter()

        url = self.manager.redmine.url + formatter.format(
            self.manager.resource_class.query_all_export, format=fmt, **self.manager.params)

        try:
            return self.manager.redmine.download(url, savepath, filename, params=formatter.unused_kwargs)
        except exceptions.UnknownError as e:
            if e.status_code == 406:
                raise exceptions.ExportFormatNotSupportedError
            raise e

    def _resource_cls(self, cls, resources, **kwargs):
        """
        Returns a new resource set class instance defined by cls, filled with resources and loaded with kwargs.

        :param any cls: (required). Resource set class.
        :param resources: (required). Iterable of resources.
        :type resources: list or tuple
        :param dict kwargs: (optional). Additional keyword arguments if any.
        """
        return cls(self.manager, resources=resources, limit=self.limit, offset=self.offset,
                   total_count=self._total_count, **kwargs)

    def __getitem__(self, item):
        """
        Sets limit and offset or returns a Resource by requested index.
        """
        if isinstance(item, slice):
            self.limit = item.stop
            self.offset = item.start
            self._is_sliced = True
        elif isinstance(item, int):
            try:
                return next(itertools.islice(self, item, item + 1))
            except StopIteration:
                raise exceptions.ResourceSetIndexError

        if self._resources is not None and self._is_sliced:
            return self._resource_cls(self.__class__, [resource for resource in BaseResourceSet.__iter__(self)])

        return self

    def __iter__(self):
        """
        Returns requested resources in a lazy fashion.
        """
        # If this is the first time we are evaluating the ResourceSet
        # all the hard part will be done by the active Engine object
        if self._resources is None:
            self.manager.params.setdefault('limit', self.limit)
            self.manager.params.setdefault('offset', self.offset)
            self._resources, self._total_count = self.manager.request(True)
            resources = self._resources
        # Otherwise ResourceSet object should handle slicing by itself
        elif self._is_sliced:
            offset = self.offset or None

            if not self.limit:
                limit = None
            elif self.limit and not self.offset:
                limit = self.limit
            else:
                limit = self.limit + self.offset

            resources = self._resources[offset:limit]
        else:
            resources = self._resources

        self._is_sliced = False
        return (resource for resource in resources)

    def __len__(self):
        """
        Allows len() to be called on a ResourceSet object.
        """
        return sum(1 for _ in self)

    def __repr__(self):
        """
        Official representation of a ResourceSet object.
        """
        return '<{0}.{1} object with {2} resources>'.format(
            self.__class__.__module__, self.__class__.__name__, self.manager.resource_class.__name__)


class ResourceSet(BaseResourceSet):
    """
    Represents a set of Redmine resources as objects.
    """
    def get(self, resource_id, default=None):
        """
        Returns a single Resource from a ResourceSet by resource id.

        :param resource_id: (required). Resource id.
        :type resource_id: int or string
        :param none default: (optional). What to return if Resource wasn't found.
        """
        for resource in super(ResourceSet, self).__iter__():
            if resource_id == resource[self.resource_id_key]:
                return self.manager.to_resource(resource)

        return default

    def filter(self, resource_ids):
        """
        Returns a ResourceSet with requested resource ids.

        :param resource_ids: (required). Resource ids.
        :type resource_ids: list or tuple
        """
        if not isinstance(resource_ids, (tuple, list)):
            raise exceptions.ResourceSetFilterParamError

        return self._resource_cls(ResourceSet, [resource for resource in super(
            ResourceSet, self).__iter__() if resource[self.resource_id_key] in resource_ids])

    def update(self, **fields):
        """
        Updates fields of all resources in a ResourceSet with the given values.

        :param dict fields: (optional). Fields in resources that will be updated.
        """
        resources = []

        for resource in self:
            for field in fields:
                setattr(resource, field, fields[field])

            resource.save()
            resources.append(resource.raw())

        return self._resource_cls(ResourceSet, resources)

    def delete(self):
        """
        Deletes all resources in a ResourceSet.
        """
        for resource in self:
            resource.delete()

        self._resources = None
        return True

    def values(self, *fields):
        """
        Returns ResourceSet as an iterable of dictionaries.

        :param fields: (optional). Iterable which sets field names each resource will contain.
        :type fields: list or tuple
        """
        if fields:
            for resource in super(ResourceSet, self).__iter__():
                yield dict((field, resource[field]) for field in fields if field in resource)
        else:
            for resource in super(ResourceSet, self).__iter__():
                yield resource

    def values_list(self, *fields, **kwargs):
        """
        Returns ResourceSet as an iterable of tuples with Resource values or single values if flattened.

        :param fields: (optional). Iterable which sets field names each resource will contain.
        :type fields: list or tuple
        :param dict kwargs: (optional). If fields contain single field, setting flat=True will flatten the result.
        """
        flat = kwargs.pop('flat', False)

        if fields:
            if flat and len(fields) == 1:
                for resource in super(ResourceSet, self).__iter__():
                    yield resource.get(fields[0])
            else:
                for resource in super(ResourceSet, self).__iter__():
                    yield tuple(resource[field] for field in fields if field in resource)
        else:
            for resource in super(ResourceSet, self).__iter__():
                yield tuple(resource.values())

    def __iter__(self):
        """
        Returns requested resources in a lazy fashion.
        """
        return (self.manager.to_resource(resource) for resource in super(ResourceSet, self).__iter__())
