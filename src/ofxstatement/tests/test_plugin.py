import unittest

import mock

from ofxstatement import plugin


class PluginTest(unittest.TestCase):
    def test_get_plugin(self) -> None:
        class SamplePlugin(plugin.Plugin):
            def get_parser(self):
                return mock.Mock()

        ep = mock.Mock()
        ep.load.return_value = SamplePlugin

        ep_patch = mock.patch("pkg_resources.iter_entry_points", return_value=[ep])

        with ep_patch:
            p = plugin.get_plugin("sample", mock.Mock("UI"), mock.Mock("Settings"))
            self.assertIsInstance(p, SamplePlugin)

    def test_get_plugin_conflict(self) -> None:
        ep = mock.Mock()

        ep_patch = mock.patch("pkg_resources.iter_entry_points", return_value=[ep, ep])
        with ep_patch:
            with self.assertRaises(plugin.PluginNameConflict):
                plugin.get_plugin("conflicting", mock.Mock("UI"), mock.Mock("Settings"))

    def test_get_plugin_not_found(self) -> None:
        with self.assertRaises(plugin.PluginNotRegistered):
            plugin.get_plugin("not_existing", mock.Mock("UI"), mock.Mock("Settings"))
