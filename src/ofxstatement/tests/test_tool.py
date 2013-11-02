import os
import unittest
from unittest import mock
import tempfile
import shutil

from ofxstatement import tool, statement


class ToolTests(unittest.TestCase):
    def test_convert_configured(self):
        args = mock.Mock(type="test",
                         input=os.path.join(self.tmpdir, "input"),
                         output=os.path.join(self.tmpdir, "output"))

        config = {"test": {"plugin": "sample"}}

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)
        uipatch = mock.patch("ofxstatement.ui.UI")

        with configpatch, pluginpatch, uipatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)

    def test_convert_noconf(self):

        args = mock.Mock(type="test",
                         input=os.path.join(self.tmpdir, "input"),
                         output=os.path.join(self.tmpdir, "output"))

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        noconfigpatch = mock.patch("ofxstatement.configuration.read",
                                   return_value=None)
        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)
        uipatch = mock.patch("ofxstatement.ui.UI")

        with noconfigpatch, pluginpatch, uipatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(suffix='ofxstatement')

    def tearDown(self):
        shutil.rmtree(self.tmpdir)
