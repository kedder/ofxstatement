"""Command line tool for converting statements to OFX format
"""
import os
import sys

from ofxstatement.plugins.swedbank import SwedbankCsvStatementParser
from ofxstatement.plugins.dnb import DnBCsvStatementParser
from ofxstatement.ofx import OfxWriter

def run():
    infname = sys.argv[1]
    outfname = sys.argv[2]

    with open(infname, 'r', encoding='cp1257') as fin, open(outfname, 'w') as fout:
        parser = DnBCsvStatementParser(fin)
        statement = parser.parse()
        writer = OfxWriter(statement)
        fout.write(writer.toxml())
    print("Done")
