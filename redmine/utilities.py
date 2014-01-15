import sys
from string import Formatter


def to_string(string):
    """Converts unicode to utf-8 if on Python 2, leaves as it is if on Python 3"""
    return string.encode('utf-8') if sys.version_info[0] < 3 else string


class MemorizeFormatter(Formatter):
    """Memorizes all arguments, used during string formatting"""
    def __init__(self):
        self.used_kwargs = {}
        self.unused_kwargs = {}

    def check_unused_args(self, used_args, args, kwargs):
        for item in used_args:
            self.used_kwargs[item] = kwargs[item]
            del kwargs[item]

        self.unused_kwargs = kwargs
