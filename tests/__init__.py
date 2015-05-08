try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from redmine import Redmine
from distutils.version import LooseVersion
from redmine.packages.requests import __version__ as requests_version

URL = 'http://foo.bar'


def json_response(json_):
    """Requests had json as a property until 1.0.0 and as a method afterwards"""
    return mock.Mock(return_value=json_) if LooseVersion(requests_version) >= LooseVersion('1.0.0') else json_
