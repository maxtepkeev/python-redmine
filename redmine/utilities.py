import sys
from string import Formatter


def is_string(string):
    """Python 2 and 3 friendly function to check if a string is really a string"""
    return isinstance(string, basestring if sys.version_info[0] < 3 else str)


def to_string(string):
    """Converts unicode to utf-8 if on Python 2, leaves as is if on Python 3"""
    return string.encode('utf-8') if sys.version_info[0] < 3 else string


class MemorizeFormatter(Formatter):
    """Memorizes all arguments, used during string formatting"""
    def __init__(self):
        self.used_kwargs = {}
        self.unused_kwargs = {}

    def check_unused_args(self, used_args, args, kwargs):
        for item in used_args:
            if item in kwargs:
                self.used_kwargs[item] = kwargs.pop(item)

        self.unused_kwargs = kwargs
