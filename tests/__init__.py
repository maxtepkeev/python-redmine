try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from redminelib import Redmine


class BaseRedmineTestCase(unittest.TestCase):
    url = 'http://foo.bar'
    patch_prefix = 'patch'
    patch_targets = {'requests': 'redminelib.engines.sync.requests.Session.request'}

    def setUp(self):
        self.redmine = Redmine(self.url)
        self.response = mock.Mock(status_code=200, history=[])

        for target, path in self.patch_targets.items():
            setattr(self, '{0}_{1}'.format(self.patch_prefix, target),
                    mock.patch(path, return_value=self.response).start())

        self.addCleanup(mock.patch.stopall)

    def set_patch_side_effect(self, side_effect):
        for target in self.patch_targets:
            getattr(self, '{0}_{1}'.format(self.patch_prefix, target)).side_effect = side_effect
