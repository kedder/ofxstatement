from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement import statement
import csv


class DABCsvStatementParser(CsvStatementParser):

    # 0 Buchungstag
    # 1 Valuta
    # 2 Buchungstext
    # 3 Auftraggeber / Empfänger
    # 4 Verwendungszweck
    # 5 Betrag in EUR

    mappings = {"date": 1, "payee": 3, "memo": 4, "amount": 5}
    date_format = "%d.%m.%Y %H:%M:%S"

    def split_records(self):
        return csv.reader(self.fin, delimiter=';')

    def parse_record(self, line):

        if self.cur_record == 2:
            self.statement.currency = line[5].strip('Betrag in ')
            print(self.statement.currency)
            return None

        if self.cur_record <= 2:
            return None

        # Remove dots (German decimal point handling)
        # 2.000,00 => 2000,00
        line[5] = line[5].replace('.', '')

        # Replace comma with dot (German decimal point handling)
        # 2000.00 => 2000.00
        line[5] = line[5].replace(',', '.')

        # fill statement line according to mappings
        sl = super(DABCsvStatementParser, self).parse_record(line)
        print(sl)
        return sl


class DABPlugin(Plugin):
    name = "dab"

    def get_parser(self, fin):
        f = open(fin, "r", encoding='utf-8')
        parser = DABCsvStatementParser(f)
#        parser.statement.account_id = self.settings['account']
#        parser.statement.bank_id = self.settings.get('bank', 'DAB Depotkonto')
        parser.statement.account_id = "DAB Depotkonto"
        parser.statement.bank_id = "DAB"
        return parser

