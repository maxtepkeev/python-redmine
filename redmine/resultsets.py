import itertools
from redmine.exceptions import (
    ResourceSetIndexError,
    ResourceSetFilterParamError,
    ResultSetTotalCountError
)


class ResourceSet(object):
    """Represents a set of Redmine resources as objects"""
    limit = 0
    offset = 0
    _total_count = -1

    def __init__(self, manager, resources=None):
        """Accepts manager instance object, optionally can be prefilled with an iterable of resources"""
        self.manager = manager
        self.resources = resources

    def get(self, resource_id, default=None):
        """Returns a single item from a ResourceSet by resource id"""
        for resource in self:
            if resource_id == resource.internal_id:
                return resource

        return default

    def filter(self, resource_ids):
        """Returns a ResourceSet with requested resource ids"""
        if not isinstance(resource_ids, (tuple, list)):
            raise ResourceSetFilterParamError

        resources = []

        for resource in self:
            if resource.internal_id in resource_ids:
                resources.append(resource)

        return ResourceSet(self.manager, resources)

    def update(self, **fields):
        """Updates fields of all resources in a ResourceSet with the given values"""
        resources = []

        for resource in self:
            for field in fields:
                setattr(resource, field, fields[field])

            resource.save()
            resources.append(resource)

        return ResourceSet(self.manager, resources)

    def delete(self):
        """Deletes all resources in a ResourceSet"""
        for resource in self:
            self.manager.delete(resource.internal_id)

        return True

    def values(self, *fields):
        """Returns ValuesResourceSet object which represents Resource as a dictionary"""
        return ValuesResourceSet(self.manager, resources=self.resources, fields=fields)

    @property
    def total_count(self):
        """Returns total count of available resources, this is known only after ResourceSet evaluation"""
        if self._total_count == -1:
            if self.resources is None:
                raise ResultSetTotalCountError
            else:
                self._total_count = len(self)

        return self._total_count

    def _evaluate(self):
        """Evaluates current ResourceSet object"""
        self.resources, self._total_count = self.manager.retrieve(
            limit=self.manager.params.get('limit', self.limit),
            offset=self.manager.params.get('offset', self.offset)
        )

    def __getitem__(self, item):
        """Sets limit and offset or returns a resource by requested index"""
        if isinstance(item, slice):
            if item.stop is not None:
                self.limit = item.stop
            if item.start is not None:
                self.offset = item.start
        elif isinstance(item, int):
            try:
                return next(itertools.islice(self, item, item + 1))
            except StopIteration:
                raise ResourceSetIndexError

        return self

    def __iter__(self):
        """Returns requested resources in a lazy fashion"""
        if self.resources is None:
            self._evaluate()

        return (self.manager.to_resource(resource) for resource in self.resources)

    def __len__(self):
        """Allows len() to be called on an instance object"""
        return sum(1 for _ in self)

    def __repr__(self):
        """Official representation of ResourceSet object"""
        return '<{0}.{1} object with {2} resources>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.manager.resource_class.__name__
        )


class ValuesResourceSet(ResourceSet):
    """Represents a set of Redmine resources as dictionaries"""
    def __init__(self, manager, resources=None, fields=()):
        """Accepts optional fields iterable which sets field names each resource will contain"""
        super(ValuesResourceSet, self).__init__(manager, resources)
        self.fields = fields
        self.resource_internal_id = 'title' if self.manager.resource_class.__name__ == 'WikiPage' else 'id'

    def get(self, resource_id, default=None):
        """Returns a single item from a ValuesResourceSet by resource id"""
        for resource in self:
            if int(resource_id) == resource[self.resource_internal_id]:
                return resource

        return default

    def filter(self, resource_ids):
        """Returns a ValuesResourceSet with requested resource ids"""
        if not isinstance(resource_ids, (tuple, list)):
            raise ResourceSetFilterParamError

        resources = []

        for resource in self:
            if resource[self.resource_internal_id] in resource_ids:
                resources.append(resource)

        return ValuesResourceSet(self.manager, resources=resources, fields=self.fields)

    def update(self, **fields):
        """Updates fields of all resources in a ValuesResourceSet with the given values"""
        resources = []

        for resource in self:
            for field in fields:
                resource[field] = fields[field]

            self.manager.update(resource[self.resource_internal_id], **fields)
            resources.append(resource)

        return ValuesResourceSet(self.manager, resources=resources, fields=self.fields)

    def delete(self):
        """Deletes all resources in a ValuesResourceSet"""
        for resource in self:
            self.manager.delete(resource[self.resource_internal_id])

        return True

    def __iter__(self):
        """Returns requested resources in a lazy fashion"""
        if self.resources is None:
            self._evaluate()

        for resource in self.resources:
            if not self.fields:
                yield resource
            else:
                fields = {}

                for field in resource:
                    if field in self.fields:
                        fields.update({field: resource[field]})

                yield fields
