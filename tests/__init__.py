import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from redmine import Redmine

URL = 'http://foo.bar'
