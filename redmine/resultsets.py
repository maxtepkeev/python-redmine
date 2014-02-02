import itertools
from redmine.exceptions import ResourceSetIndexError, ResourceSetFilterParamError, ResultSetNotEvaluatedError


class ResourceSet(object):
    """Represents a set of Redmine resources"""
    limit = 0
    offset = 0

    def __init__(self, manager, resources=None):
        """Accepts manager instance object, optionally can be prefilled with an iterable of resources"""
        self.manager = manager
        self.resources = resources

    def get(self, resource_id):
        """Returns a single item from a ResourceSet by resource id"""
        for resource in self:
            if int(resource_id) == resource.id:
                return resource

        return None

    def filter(self, resource_ids):
        """Returns a ResourceSet with requested resource ids"""
        if not isinstance(resource_ids, (tuple, list)):
            raise ResourceSetFilterParamError()

        resources = []

        for resource in self:
            if resource.id in resource_ids:
                resources.append(resource)

        return ResourceSet(self.manager, resources)

    @property
    def total_count(self):
        """ Raises an exception if the count is not set (count is only set at set evaluation time """
        if self.manager.total_count == -1:
            raise ResultSetNotEvaluatedError()
        return self.manager.total_count

    def __getitem__(self, item):
        """Sets limit and offset or returns a resource by requested index"""
        if isinstance(item, slice):
            if item.stop is not None:
                self.limit = item.stop
            if item.start is not None:
                self.offset = item.start
        elif isinstance(item, int):
            try:
                return next(itertools.islice(self.__iter__(), item, item + 1))
            except StopIteration:
                raise ResourceSetIndexError()

        return self

    def __iter__(self):
        """Returns requested resources in a lazy fashion"""
        if self.resources is None:
            self.resources = self.manager.retrieve(
                limit=self.manager.params.get('limit', self.limit),
                offset=self.manager.params.get('offset', self.offset)
            )

        return iter(self.manager.to_resource(resource) for resource in self.resources)

    def __len__(self):
        """Allows len() to be called on an instance object"""
        return sum(1 for _ in self.__iter__())

    def __repr__(self):
        """Official representation of ResourceSet object"""
        return '<{0}.{1} object with {2} resources>'.format(
            self.__class__.__module__,
            self.__class__.__name__,
            self.manager.resource_class.__name__
        )
