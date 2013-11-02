"""Parser for LITAS-ESIS csv statement"""

import csv

from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin

LINETIME_HEADER = "000"
LINETYPE_TRANSACTION = "010"
LINETYPE_SUMMARY = "020"

SUMMARY_START = "LikutisPR"
SUMMARY_END = "LikutisPB"


class LitasEsisCsvDialect(object):
    delimiter = "\t"
    quotechar = None
    escapechar = None
    doublequote = False
    skipinitialspace = False
    lineterminator = '\r\n'
    quoting = csv.QUOTE_NONE


class LitasEsisCsvStatementParser(CsvStatementParser):
    date_format = "%Y%m%d"
    mappings = {"date": 2,
                "amount": 4,
                "id": 10,
                "payee": 17,
                "memo": 13,
                }
    charset = 'cp1257'

    def parse_float(self, value):
        return int(value) / 100.0

    def split_records(self):
        return csv.reader(self.fin, dialect=LitasEsisCsvDialect)

    def parse_record(self, line):
        # print(line)

        linetype = line[0]
        stmt = self.statement

        if linetype == LINETIME_HEADER:
            # Get basic account information
            stmt.currency = line[17]
            stmt.bank_id = line[3]
            stmt.account_id = line[16] + line[17]
            return None

        elif linetype == LINETYPE_TRANSACTION:
            # parse transaction line in standard fasion
            stmtline = super(LitasEsisCsvStatementParser, self).parse_record(line)
            if line[6] == "D":
                stmtline.amount = -stmtline.amount
            return stmtline

        elif linetype == LINETYPE_SUMMARY:
            summarytype = line[1]
            if summarytype == SUMMARY_START:
                stmt.start_balance = self.parse_float(line[4])
                stmt.start_date = self.parse_datetime(line[2])
            elif summarytype == SUMMARY_END:
                stmt.end_balance = self.parse_float(line[4])
                stmt.end_date = self.parse_datetime(line[2])
            return None

    def swap_payee_and_memo(self):
        payee, memo = self.mappings['payee'], self.mappings['memo']
        self.mappings['payee'] = memo
        self.mappings['memo'] = payee


class LitasEsisPlugin(Plugin):
    """Standard Lithuanian LITAS-ESIS format"""

    def get_parser(self, fin):
        encoding = self.settings.get('charset', 'utf-8')
        f = open(fin, 'r', encoding=encoding)
        parser = LitasEsisCsvStatementParser(f)
        if 'swap-payee-and-memo' in self.settings:
            parser.swap_payee_and_memo()
        return parser
