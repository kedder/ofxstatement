"""Command line tool for converting statements to OFX format
"""
import os
import sys
import argparse

import ofxstatement.plugins

import ofxstatement
from ofxstatement.ui import UI
from ofxstatement import configuration
from ofxstatement import plugin
from ofxstatement.ofx import OfxWriter
from ofxstatement.exceptions import Abort

def get_version():
    return ofxstatement.__version__

def parse_args():
    parser = argparse.ArgumentParser(
                description='Convert proprietary bank statement to OFX format.')

    parser.add_argument("-t", "--type",
                        required=True,
                        help="Input file type. This type must be present as a "
                        " section in your config file.")
    parser.add_argument("--version", action="version",
                        version='ofxstatement %s' % get_version(),
                        help="Show current version")
    parser.add_argument("input", help="Input file to process")
    parser.add_argument("output", help="Output (OFX) file to produce")
    return parser.parse_args()

def process(args, ui):
    # read configuration
    config = configuration.read(ui)

    if args.type not in config:
        raise Abort("No section named %s in config file" % args.type)

    settings = config[args.type]

    pname = settings.get('plugin', None)
    if not pname:
        raise Abort("Specify 'plugin' setting for section %s" % args.type)

    # pick and configure plugin 
    try:
        p = plugin.get_plugin(pname, ui, settings)
    except plugin.PluginNotRegistered as e:
        raise Abort("No plugin named '%s' is found" % e) from e

    # process the input and produce output
    parser = p.get_parser(args.input)
    statement = parser.parse()

    with open(args.output, "w") as out:
        writer = OfxWriter(statement)
        out.write(writer.toxml())

    ui.status("Conversion completed: %s" % args.input)


def run():
    # parse command line options
    args = parse_args()

    # set up user interface
    ui = UI()

    try:
        process(args, ui)
    except Abort as e:
        ui.error(e)

