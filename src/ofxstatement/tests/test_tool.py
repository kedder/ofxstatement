import os
import platform
import unittest
import tempfile
import io
import logging
import logging.handlers
import shutil

import mock

from ofxstatement import tool, statement, configuration, parser, exceptions


class ToolTests(unittest.TestCase):
    def test_convert_configured(self) -> None:
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", input=inputfname, output=outputfname)

        config = {"test": {"plugin": "sample"}}

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        configpatch = mock.patch("ofxstatement.configuration.read", return_value=config)

        pluginpatch = mock.patch(
            "ofxstatement.plugin.get_plugin", return_value=sample_plugin
        )

        with configpatch, pluginpatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % inputfname],
        )

    def test_convert_noconf(self) -> None:
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")
        args = mock.Mock(type="test", input=inputfname, output=outputfname)

        parser = mock.Mock()
        parser.parse.return_value = statement.Statement()

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = parser

        noconfigpatch = mock.patch("ofxstatement.configuration.read", return_value=None)
        pluginpatch = mock.patch(
            "ofxstatement.plugin.get_plugin", return_value=sample_plugin
        )

        with noconfigpatch, pluginpatch:
            ret = tool.convert(args)

        self.assertEqual(ret, 0)

        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["INFO: Conversion completed: %s" % inputfname],
        )

    def test_convert_parseerror(self) -> None:
        inputfname = os.path.join(self.tmpdir, "input")
        outputfname = os.path.join(self.tmpdir, "output")

        class FailingParser(parser.StatementParser):
            def parse(self):
                raise exceptions.ParseError(23, "Catastrophic error")

        sample_plugin = mock.Mock()
        sample_plugin.get_parser.return_value = FailingParser()

        noconfigpatch = mock.patch("ofxstatement.configuration.read", return_value=None)

        pluginpatch = mock.patch(
            "ofxstatement.plugin.get_plugin", return_value=sample_plugin
        )

        with noconfigpatch, pluginpatch:
            ret = tool.run(["convert", "-t test", inputfname, outputfname])

        self.assertEqual(ret, 2)
        self.assertEqual(
            self.log.getvalue().splitlines(),
            ["ERROR: Parse error on line 23: Catastrophic error"],
        )

    def test_list_plugins_plugins(self) -> None:
        pl1 = mock.Mock(__doc__="Plugin one")
        pl2 = mock.Mock()
        plugins = [("pl1", pl1), ("pl2", pl2)]

        pluginpatch = mock.patch(
            "ofxstatement.plugin.list_plugins", return_value=plugins
        )
        outpatch = mock.patch("sys.stdout", self.log)

        with pluginpatch, outpatch:
            tool.run(["list-plugins"])

        self.assertEqual(
            self.log.getvalue().splitlines(),
            [
                "The following plugins are available: ",
                "",
                "  pl1              Plugin one",
                "  pl2              ",
            ],
        )

    def test_list_plugins_noplugins(self) -> None:
        pluginpatch = mock.patch("ofxstatement.plugin.list_plugins", return_value=[])
        outpatch = mock.patch("sys.stdout", self.log)
        with pluginpatch, outpatch:
            tool.run(["list-plugins"])

        self.assertEqual(
            self.log.getvalue().splitlines(),
            [
                "No plugins available. Install plugin eggs or create your own.",
                "See https://github.com/kedder/ofxstatement for more info.",
            ],
        )

    def test_editconfig_noconfdir(self) -> None:
        # config directory does not exist yet
        confdir = os.path.join(self.tmpdir, "config")
        confpath = os.path.join(confdir, "config.ini")
        locpatch = mock.patch.object(
            configuration, "get_default_location", return_value=confpath
        )

        call = mock.Mock()
        makedirs = mock.Mock()
        mkdirspatch = mock.patch("os.makedirs", makedirs)
        subprocesspatch = mock.patch("subprocess.call", call)
        envpatch = mock.patch("os.environ", {"EDITOR": "notepad.exe"})

        with locpatch, envpatch, mkdirspatch, subprocesspatch:
            tool.run(["edit-config"])

        makedirs.assert_called_once_with(confdir, mode=0o700)
        call.assert_called_once_with(["notepad.exe", confpath])

    def test_editconfig_existing(self) -> None:
        # config directory already exists
        confpath = os.path.join(self.tmpdir, "config.ini")
        locpatch = mock.patch.object(
            configuration, "get_default_location", return_value=confpath
        )
        makedirs = mock.Mock()
        mkdirspatch = mock.patch("os.makedirs", makedirs)

        call = mock.Mock()
        subprocesspatch = mock.patch("subprocess.call", call)

        envpatch = mock.patch("os.environ", {})

        with locpatch, envpatch, mkdirspatch, subprocesspatch:
            tool.run(["edit-config"])

        self.assertEqual(makedirs.mock_calls, [])
        editors = {"Linux": "vim", "Darwin": "vi", "Windows": "notepad"}
        call.assert_called_once_with([editors[platform.system()], confpath])

    def setUp(self) -> None:
        self.tmpdir = tempfile.mkdtemp(suffix="ofxstatement")
        self.setUpLogging()

    def tearDown(self) -> None:
        self.tearDownLogging()
        shutil.rmtree(self.tmpdir)

    def setUpLogging(self) -> None:
        self.log = io.StringIO()
        fmt = logging.Formatter("%(levelname)s: %(message)s")
        self.loghandler = logging.StreamHandler(self.log)
        self.loghandler.setFormatter(fmt)
        logging.root.addHandler(self.loghandler)
        logging.root.setLevel(logging.INFO)

    def tearDownLogging(self) -> None:
        logging.root.removeHandler(self.loghandler)
