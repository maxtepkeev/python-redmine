"""
Provides helper utilities.
"""

import copy
import string
import urllib.parse

from . import exceptions


def versiontuple(version):
    """
    Converts numeric SemVer version string to tuple.

    :param string version: (required). Version string to convert.
    """
    parts = str(version).split('.')

    if len(parts) != 3 or not all(part.isnumeric() for part in parts):
        raise exceptions.VersionFormatError(version)

    return tuple(int(part) for part in parts)


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


class ResourceQueryFormatter(string.Formatter):
    """
    Quotes query and memorizes all arguments, used during string formatting.
    """
    def __init__(self):
        self.used_kwargs = {}
        self.unused_kwargs = {}

    def check_unused_args(self, used_args, args, kwargs):
        for item in used_args:
            if item in kwargs:
                self.used_kwargs[item] = kwargs.pop(item)

        self.unused_kwargs = kwargs

    def format_field(self, value, format_spec):
        return urllib.parse.quote(super().format_field(value, format_spec).encode('utf-8'))


class ResourceQueryStr(str):
    """
    Extends default string with additional formatting capabilities.
    """
    formatter = ResourceQueryFormatter()

    def format(self, *args, **kwargs):
        return self.formatter.format(self, *args, **kwargs)
