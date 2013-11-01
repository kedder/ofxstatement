from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement import statement
import csv

class DKBCCCsvStatementParser(CsvStatementParser):
    mappings = {"date": 1, "memo": 3, "amount": 4}
    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):
        if self.cur_record  == 3:
            self.statement.start_date=self.parse_datetime(line[1])
            return None
        if self.cur_record == 5:
            self.statement.end_balance=self.parse_float(line[1].replace(' EUR',''))
            return None
        if self.cur_record == 6:
            self.statement.end_date=self.parse_datetime(line[1])
            return None

        if self.cur_record == 8:
            self.statement.currency=line[4].strip('Betrag (').strip(')')
            return None

        if self.cur_record <= 8:
            return None
        line[4]=line[4].replace(',','.')
        # fill statement line according to mappings
        sl = super(DKBCCCsvStatementParser, self).parse_record(line)
        return sl

class DKBCCPlugin(Plugin):
    def get_parser(self, fin):
        f = open(fin, "r",encoding='iso-8859-1')
        parser=DKBCCCsvStatementParser(f)
        parser.statement.account_id = self.settings['account']
        parser.statement.bank_id = self.settings.get('bank', 'DKB_VISA')
        return parser

