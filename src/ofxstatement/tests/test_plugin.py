import unittest

import mock

from ofxstatement import plugin


class PluginTest(unittest.TestCase):

    def test_get_plugin(self):
        class SamplePlugin(plugin.Plugin):
            def get_parser(self):
                return mock.Mock()

        ep = mock.Mock()
        ep.load.return_value = SamplePlugin

        ep_patch = mock.patch("pkg_resources.iter_entry_points",
                              return_value=[ep])

        with ep_patch:
            p = plugin.get_plugin("sample", None, None)
            self.assertIsInstance(p, SamplePlugin)

    def test_get_plugin_conflict(self):
        ep = mock.Mock()

        ep_patch = mock.patch("pkg_resources.iter_entry_points",
                              return_value=[ep, ep])
        with ep_patch:
            with self.assertRaises(plugin.PluginNameConflict):
                plugin.get_plugin("conflicting", None, None)

    def test_get_plugin_not_found(self):
        with self.assertRaises(plugin.PluginNotRegistered):
            plugin.get_plugin("not_existing", None, None)
