from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
import csv


class LbbAmazonCsvStatementParser(CsvStatementParser):
    mappings = {"date": 1, "memo": 3, "amount": 6}
    date_format = "%d.%m.%Y"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):
        #Free Headerline
        if self.cur_record <= 1:
            return None

        # Empty transactions to include amazon points
        if line[6] == '':
            line[6] = '0,00'
        #Change decimalsign from , to .
        line[6] = line[6].replace(',', '.')

        # fill statement line according to mappings
        sl = super(LbbAmazonCsvStatementParser, self).parse_record(line)
        return sl


class LbbAmazonPlugin(Plugin):

    def get_parser(self, fin):
        f = open(fin, "r", encoding='iso-8859-1')
        parser = LbbAmazonCsvStatementParser(f)
        parser.statement.account_id = self.settings['account']
        parser.statement.currency = self.settings['currency']
        parser.statement.bank_id = self.settings.get('bank', 'LBB_Amazon')
        return parser
