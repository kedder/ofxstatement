"""Command line tool for converting statements to OFX format
"""
import os
import sys
import argparse
import tempfile
import subprocess

import pkg_resources

import ofxstatement
from ofxstatement import ui
from ofxstatement import configuration
from ofxstatement import plugin
from ofxstatement.ofx import OfxWriter
from ofxstatement.exceptions import Abort


def get_version():
    dist = pkg_resources.get_distribution("ofxstatement")
    return dist.version


def make_args_parser():
    parser = argparse.ArgumentParser(
        description='Tool to convert proprietary bank statement to OFX format.')
    parser.add_argument("--version", action="version",
                        version='%%(prog)s %s' % get_version(),
                        help="show current version")

    subparsers = parser.add_subparsers(title="action")

    # convert
    parser_convert = subparsers.add_parser("convert",
                                           help="convert to OFX")

    parser_convert.add_argument("-t", "--type",
                                required=True,
                                help=("input file type. This is a section in "
                                      "config file, or plugin name if you "
                                      "have no config file."))
    parser_convert.add_argument("input", help="input file to process")
    parser_convert.add_argument("output", help="output (OFX) file to produce")
    parser_convert.set_defaults(func=convert)

    # list-plugins
    parser_list = subparsers.add_parser("list-plugins",
                                        help="list available plugins")
    parser_list.set_defaults(func=list_plugins)

    # edit-config
    parser_edit = subparsers.add_parser("edit-config",
                                        help=("open configuration file in "
                                              "default editor"))
    parser_edit.set_defaults(func=edit_config)

    return parser


def list_plugins(args):
    print("The following plugins are available: ")
    print()
    for name, plclass in plugin.list_plugins():
        if plclass.__doc__:
            title = plclass.__doc__.splitlines()[0]
        else:
            title = ""
        print("  %-16s %s" % (name, title))


def edit_config(args):
    editor = os.environ.get('EDITOR', 'vim')
    configfname = configuration.get_default_location()
    configdir = os.path.dirname(configfname)
    if not os.path.exists(configdir):
        os.makedirs(configdir, mode=0o700)
    subprocess.call([editor, configfname])


def convert(args):
    appui = ui.UI()
    # read configuration
    config = configuration.read()

    if config is None:
        # No configuration mode
        settings = {}
        pname = args.type
    else:
        # Configuration is loaded
        if args.type not in config:
            raise Abort("No section named %s in config file" % args.type)

        settings = dict(config[args.type])

        pname = settings.get('plugin', None)
        if not pname:
            raise Abort("Specify 'plugin' setting for section %s" % args.type)

    # pick and configure plugin
    try:
        p = plugin.get_plugin(pname, appui, settings)
    except plugin.PluginNotRegistered as e:
        raise Abort("No plugin named '%s' is found" % pname) from e

    # process the input and produce output
    parser = p.get_parser(args.input)
    statement = parser.parse()

    with open(args.output, "w") as out:
        writer = OfxWriter(statement)
        out.write(writer.toxml())

    appui.status("Conversion completed: %s" % args.input)
    return 0  # success


def run():
    parser = make_args_parser()
    args = parser.parse_args()

    if not hasattr(args, "func"):
        parser.print_usage()
        parser.exit(1)

    return args.func(args)
