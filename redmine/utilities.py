import sys
import string


def to_string(unistr):
    """
    Encodes unicode string to utf-8 if on Python 2, leaves as is if on Python 3.

    :param str unistr: (required). Unicode string.
    """
    return unistr.encode('utf-8') if sys.version_info[0] < 3 else unistr


class MemorizeFormatter(string.Formatter):
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
