"""
Defines lookup classes to be used in ResultSet's filter method.
"""

registry = {}


class Lookup:
    lookup_name = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        registry[cls.lookup_name] = cls()

    def __call__(self, resource_value, requested_value):
        raise NotImplementedError


class Exact(Lookup):
    lookup_name = 'exact'

    def __call__(self, resource_value, requested_value):
        return resource_value == requested_value


class In(Lookup):
    lookup_name = 'in'

    def __call__(self, resource_value, requested_values):
        return resource_value in requested_values
