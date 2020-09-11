"""Command line tool for converting statements to OFX format
"""
import os
import argparse
import shlex
import subprocess
import logging
import platform
import sys
import contextlib

import pkg_resources

from ofxstatement import ui, configuration, plugin, ofx, exceptions


log = logging.getLogger(__name__)


@contextlib.contextmanager
def smart_open(filename: str = None):
    """See https://stackoverflow.com/questions/17602878/how-to-handle-both-with-open-and-sys-stdout-nicely"""  # noqa
    if filename and filename != "-":
        fh = open(filename, "w")
    else:
        fh = sys.stdout

    try:
        yield fh
    finally:
        if fh is not sys.stdout:
            fh.close()


def get_version() -> str:
    dist = pkg_resources.get_distribution("ofxstatement")
    return dist.version


def configure_logging(args: argparse.Namespace) -> None:
    format = "%(levelname)s: %(message)s"
    arg_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(format=format, level=arg_level)


def make_args_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Tool to convert proprietary bank statement " + "to OFX format."
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%%(prog)s %s" % get_version(),
        help="show current version",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="show debugging information",
    )

    subparsers = parser.add_subparsers(title="action")

    # convert
    parser_convert = subparsers.add_parser("convert", help="convert to OFX")

    parser_convert.add_argument(
        "-t",
        "--type",
        required=True,
        help=(
            "input file type. This is a section in "
            "the config file or plugin name if you "
            "have no config file."
        ),
    )
    parser_convert.add_argument("input", help="input file to process")
    parser_convert.add_argument(
        "output",
        help=(
            "output (OFX) file to produce where a minus (-) "
            "means writing to standard output instead"
        ),
    )
    parser_convert.set_defaults(func=convert)

    # list-plugins
    parser_list = subparsers.add_parser("list-plugins", help="list available plugins")
    parser_list.set_defaults(func=list_plugins)

    # edit-config
    parser_edit = subparsers.add_parser(
        "edit-config", help=("open configuration file in " "default editor")
    )
    parser_edit.set_defaults(func=edit_config)

    return parser


def list_plugins(args: argparse.Namespace) -> None:
    available_plugins = plugin.list_plugins()
    if not available_plugins:
        print("No plugins available. Install plugin eggs or create your own.")
        print("See https://github.com/kedder/ofxstatement for more info.")

    else:
        print("The following plugins are available: ")
        print("")
        for name, plclass in available_plugins:
            if plclass.__doc__:
                title = plclass.__doc__.splitlines()[0]
            else:
                title = ""
            print("  %-16s %s" % (name, title))


def edit_config(args: argparse.Namespace) -> None:
    editors = {"Linux": "vim", "Darwin": "vi", "Windows": "notepad"}
    editor = os.environ.get("EDITOR", editors[platform.system()])
    configfname = configuration.get_default_location()
    configdir = os.path.dirname(configfname)
    if not os.path.exists(configdir):
        log.info("Creating confugration directory: %s" % configdir)
        os.makedirs(configdir, mode=0o700)
    log.info("Running editor: %s %s" % (editor, configfname))
    subprocess.call(shlex.split(editor, posix=(os.name == "posix")) + [configfname])


def convert(args: argparse.Namespace) -> int:
    appui = ui.UI()
    config = configuration.read()

    if config is None:
        # No configuration mode
        settings = {}
        pname = args.type
    else:
        # Configuration is loaded
        if args.type not in config:
            log.error("No section '%s' in config file." % args.type)
            log.error(
                "Edit configuration using ofxstatement edit-config and "
                "add section [%s]." % args.type
            )
            return 1  # error

        settings = dict(config[args.type])

        pname = settings.get("plugin", None)
        if not pname:
            log.error("Specify 'plugin' setting for section [%s]" % args.type)
            return 1  # error

    # pick and configure plugin
    try:
        p = plugin.get_plugin(pname, appui, settings)
    except plugin.PluginNotRegistered:
        log.error("No plugin named '%s' is found" % pname)
        return 1  # error

    # process the input and produce output
    parser = p.get_parser(args.input)
    try:
        statement = parser.parse()
    except exceptions.ParseError as e:
        log.error("Parse error on line %s: %s" % (e.lineno, e.message))
        return 2  # parse error

    # Validate the statement
    try:
        statement.assert_valid()
    except exceptions.ValidationError as e:
        log.error("Statement validation error: %s" % (e.message))
        return 2  # Validation error

    with smart_open(args.output) as out:
        writer = ofx.OfxWriter(statement)
        out.write(writer.toxml())

    log.info("Conversion completed: %s" % args.input)
    return 0  # success


def run(argv=None) -> int:
    parser = make_args_parser()
    args = parser.parse_args(argv)
    configure_logging(args)

    if not hasattr(args, "func"):
        parser.print_usage()
        parser.exit(1)

    return args.func(args)
