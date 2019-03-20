"""
Provides helper utilities.
"""

import sys
import copy
import string
import functools
try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


def fix_unicode(cls):
    """
    A class decorator that defines __unicode__, makes __str__ and __repr__
    return a utf-8 encoded string and encodes unicode exception messages
    to utf-8 encoded strings under Python 2. Does nothing under Python 3.

    :param class cls: (required). A class where unicode should be fixed.
    """
    if sys.version_info[0] >= 3:
        return cls

    def decorator(fn):
        @functools.wraps(fn, assigned=('__name__', '__doc__'))
        def wrapper(self, *args, **kwargs):
            if fn.__name__ == '__init__':
                return fn(self, *[arg.encode('utf-8') if isinstance(arg, unicode) else arg for arg in args], **kwargs)
            return fn(self).encode('utf-8')
        return wrapper

    if issubclass(cls, Exception):
        cls.__init__ = decorator(cls.__init__)
        return cls

    cls.__unicode__ = cls.__str__
    cls.__str__ = decorator(cls.__unicode__)
    cls.__repr__ = decorator(cls.__repr__)
    return cls


def with_metaclass(meta, *bases):
    """
    Create a base class with a metaclass.
    """
    class MetaClass(meta):
        def __new__(cls, name, this_bases, dct):
            return meta(name, bases, dct)
    return type.__new__(MetaClass, 'temporary_class', (), {})


def merge_dicts(a, b):
    """
    Merges dicts a and b recursively into a new dict.

    :param dict a: (required).
    :param dict b: (required).
    """
    result = copy.deepcopy(a)

    for key, value in b.items():
        if isinstance(value, dict):
            result[key] = merge_dicts(value, a.get(key, {}))
        else:
            result[key] = value

    return result


class URIFormatter(string.Formatter):
    """
    Passes all arguments through urllib.parse.quote.
    """
    def format_field(self, value, format_spec):
        retval = super(URIFormatter, self).format_field(value, format_spec)
        return quote(retval.encode('utf-8'))


class MemorizeURIFormatter(URIFormatter):
    """
    Memorizes all arguments, used during string formatting.
    """
    def __init__(self):
        self.used_kwargs = {}
        self.unused_kwargs = {}

    def check_unused_args(self, used_args, args, kwargs):
        for item in used_args:
            if item in kwargs:
                self.used_kwargs[item] = kwargs.pop(item)

        self.unused_kwargs = kwargs


class URITemplate(str):
    formatter = URIFormatter()

    def format(self, *args, **kwargs):
        return URIFormatter().format(self, *args, **kwargs)
