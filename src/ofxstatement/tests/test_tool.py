import os
import unittest
import tempfile
import io
import logging
import logging.handlers
import shutil

import mock

from ofxstatement import tool, statement, configuration, parser, exceptions


class ToolTests(unittest.TestCase):
    def test_convert_configured(self):
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", input=inputfname, output=outputfname)

        config = {"test": {"plugin": "sample"}}

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with configpatch, pluginpatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % inputfname])

    def test_convert_noconf(self):
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", input=inputfname, output=outputfname)

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        noconfigpatch = mock.patch("ofxstatement.configuration.read",
                                   return_value=None)
        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with noconfigpatch, pluginpatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)

        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % inputfname])

    def test_convert_parseerror(self):
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")

        class FailingParser(parser.StatementParser):
            def parse(self):
                raise exceptions.ParseError(23, "Catastrophic error")

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = FailingParser()

        noconfigpatch = mock.patch("ofxstatement.configuration.read",
                                   return_value=None)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with noconfigpatch, pluginpatch:
            ret = tool.run(['convert', '-t test', inputfname, outputfname])

        self.assertEqual(ret, 2)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ['ERROR: Parse error on line 23: Catastrophic error'])
    
    def test_download_date_wrong(self):
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", date_from="01/13/2019", 
                            date_to="01/02/2019", output=outputfname)

        config = {"test": {"plugin": "sample"}}

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with configpatch, pluginpatch:
            ret = tool.download(args)

        self.assertEqual(ret, 1)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["ERROR: Wrong date format: %s" % "01/13/2019"])

    def test_download_date_consistency(self):
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", date_from="02/01/2019", 
                            date_to="01/01/2019", output=outputfname)

        config = {"test": {"plugin": "sample"}}

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with configpatch, pluginpatch:
            ret = tool.download(args)

        self.assertEqual(ret, 1)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["ERROR: End date before start date"])

    def test_download_configured(self):
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", date_from="01/01/2019", date_to="01/02/2019", output=outputfname)

        config = {"test": {"plugin": "sample"}}

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with configpatch, pluginpatch:
            ret = tool.download(args)

        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: [%s] Download started" % "test",
            "INFO: Download completed: %s" % outputfname])

    def test_download_noconf(self):
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", date_from="01/01/2019", date_to="01/02/2019", output=outputfname)

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        noconfigpatch = mock.patch("ofxstatement.configuration.read",
                                   return_value=None)
        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with noconfigpatch, pluginpatch:
            ret = tool.download(args)

        self.assertEqual(ret, 0)

        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: [%s] Download started" % "test",
            "INFO: Download completed: %s" % outputfname])

    def test_download_no_download(self):
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", date_from="01/01/2019", date_to="01/02/2019", output=outputfname)

        config = {"test": {"plugin": "sample"}}

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser
        sample_plugin.get_downloader.side_effect = NotImplementedError

        configpatch = mock.patch("ofxstatement.configuration.read",
                                 return_value=config)

        pluginpatch = mock.patch("ofxstatement.plugin.get_plugin",
                                 return_value=sample_plugin)

        with configpatch, pluginpatch:
            ret = tool.download(args)

        self.assertEqual(ret, 1)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["ERROR: Plugin '%s' has no download capability" % "sample"])

    def test_list_plugins_plugins(self):
        pl1 = mock.Mock(__doc__="Plugin one")
        pl2 = mock.Mock()
        plugins = [("pl1", pl1), ("pl2", pl2)]

        pluginpatch = mock.patch("ofxstatement.plugin.list_plugins",
                                 return_value=plugins)
        outpatch = mock.patch("sys.stdout", self.log)

        with pluginpatch, outpatch:
            tool.run(['list-plugins'])

        self.assertEqual(
            self.log.getvalue().splitlines(),
            ['The following plugins are available: ',
             '',
             '  pl1              Plugin one',
             '  pl2              '])

    def test_list_plugins_noplugins(self):
        pluginpatch = mock.patch("ofxstatement.plugin.list_plugins",
                                 return_value=[])
        outpatch = mock.patch("sys.stdout", self.log)
        with pluginpatch, outpatch:
            tool.run(['list-plugins'])

        self.assertEqual(
            self.log.getvalue().splitlines(),
            ['No plugins available. Install plugin eggs or create your own.',
             'See https://github.com/kedder/ofxstatement for more info.'])

    def test_editconfig_noconfdir(self):
        # config directory does not exist yet
        confdir = os.path.join(self.tmpdir, "config")
        confpath = os.path.join(confdir, "config.ini")
        locpatch = mock.patch.object(configuration, "get_default_location",
                                     return_value=confpath)

        call = mock.Mock()
        makedirs = mock.Mock()
        mkdirspatch = mock.patch("os.makedirs", makedirs)
        subprocesspatch = mock.patch("subprocess.call", call)
        envpatch = mock.patch("os.environ", {"EDITOR": "notepad.exe"})

        with locpatch, envpatch, mkdirspatch, subprocesspatch:
            tool.run(['edit-config'])

        makedirs.assert_called_once_with(confdir, mode=0o700)
        call.assert_called_once_with(["notepad.exe", confpath])

    def test_editconfig_existing(self):
        # config directory already exists
        confpath = os.path.join(self.tmpdir, "config.ini")
        locpatch = mock.patch.object(configuration, "get_default_location",
                                     return_value=confpath)
        makedirs = mock.Mock()
        mkdirspatch = mock.patch("os.makedirs", makedirs)

        call = mock.Mock()
        subprocesspatch = mock.patch("subprocess.call", call)

        envpatch = mock.patch("os.environ", {})

        with locpatch, envpatch, mkdirspatch, subprocesspatch:
            tool.run(['edit-config'])

        self.assertEqual(makedirs.mock_calls, [])
        call.assert_called_once_with(["vim", confpath])

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp(suffix='ofxstatement')
        self.setUpLogging()

    def tearDown(self):
        self.tearDownLogging()
        shutil.rmtree(self.tmpdir)

    def setUpLogging(self):
        self.log = io.StringIO()
        fmt = logging.Formatter("%(levelname)s: %(message)s")
        self.loghandler = logging.StreamHandler(self.log)
        self.loghandler.setFormatter(fmt)
        logging.root.addHandler(self.loghandler)
        logging.root.setLevel(logging.INFO)

    def tearDownLogging(self):
        logging.root.removeHandler(self.loghandler)
