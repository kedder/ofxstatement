"""Parser for DnB csv statement"""

import sys
import csv

from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin

LINETIME_HEADER = "000"
LINETYPE_TRANSACTION = "010"
LINETYPE_SUMMARY = "020"

SUMMARY_START = "LikutisPR"
SUMMARY_END = "LikutisPB"

class DnBCsvDialect(object):
    delimiter = "\t"
    quotechar = None
    escapechar = None
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE

class DnBCsvStatementParser(CsvStatementParser):
    dateFormat = "%Y%m%d"
    mappings = {"date": 2,
                "amount": 4,
                "id": 10,
                "payee": 17,
                "memo": 13,
                }
    charset = 'cp1257'

    def parseFloat(self, value):
        return int(value) / 100.0

    def createReader(self):
        return csv.reader(self.fin, dialect=DnBCsvDialect)

    def parseLine(self, line):
        # print(line)

        lineType = line[0]

        if lineType == LINETIME_HEADER:
            # Get basic account information
            self.statement.currency = line[17]
            self.statement.bankId = line[3]
            self.statement.accountId = line[16]
            return None

        elif lineType == LINETYPE_TRANSACTION:
            # parse transaction line in standard fasion
            stmtline = super(DnBCsvStatementParser, self).parseLine(line)
            if line[6] == "D":
                stmtline.amount = -stmtline.amount
            return stmtline

        elif lineType == LINETYPE_SUMMARY:
            summaryType = line[1]
            if summaryType == SUMMARY_START:
                self.statement.startingBalance = self.parseFloat(line[4])
                self.statement.startingBalanceDate = self.parseDateTime(line[2])
            elif summaryType == SUMMARY_END:
                self.statement.endingBalance = self.parseFloat(line[4])
                self.statement.endingBalanceDate = self.parseDateTime(line[2])
            return None

class DnBPlugin(Plugin):
     name = "dnb"

     def get_parser(self, fin):
         encoding = self.settings.get('charset', 'utf-8')
         f = open(fin, encoding=encoding)
         return DnBCsvStatementParser(f)
