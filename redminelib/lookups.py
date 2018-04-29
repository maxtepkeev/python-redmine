"""
Defines lookup classes to be used in ResultSet's filter method.
"""

from . import utilities


registry = {}


class Registrar(type):
    """
    A lookup class that implements this metaclass, i.e. all lookup classes that inherit from
    Lookup, will be added to a lookup registry to be used in ResultSet's filter method. Lookup
    class, at minimum, should define a lookup_name attribute and implement a __call__ method,
    otherwise it will be considered a base class and won't be added to the registry.
    """
    def __new__(mcs, name, bases, attrs):
        cls = super(Registrar, mcs).__new__(mcs, name, bases, attrs)

        if attrs['lookup_name'] is None:  # base classes shouldn't be added to the registry
            return cls

        registry[attrs['lookup_name']] = cls()
        return cls


class Lookup(utilities.with_metaclass(Registrar)):
    lookup_name = None

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
