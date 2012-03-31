from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement import statement

DETAILS_FIELD = 5

class DanskeCsvStatementParser(CsvStatementParser):
    mappings = {"date": 0,
                "memo": 4,
                "amount": 8
                }
    dateFormat = "%Y:%m:%d"

    def parse(self):
        stmt = super(DanskeCsvStatementParser, self).parse()
        statement.recalculate_balance(stmt)
        return stmt

    def parseLine(self, line):
        if self.currentLine == 1:
            return None

        # fill statement line according to mappings
        sl = super(DanskeCsvStatementParser, self).parseLine(line)

        # generate transaction id out of available data
        sl.id = statement.generate_transaction_id(sl)
        if not sl.memo:
            sl.memo = line[DETAILS_FIELD]
        return sl

    def use_details_for_memo(self):
        self.mappings['memo'] = DETAILS_FIELD


class DanskePlugin(Plugin):
    name = "danske"

    def get_parser(self, fin):
        encoding = self.settings.get('charset', 'utf-8')
        f = open(fin, 'r', encoding=encoding)
        parser = DanskeCsvStatementParser(f)
        parser.statement.currency = self.settings['currency']
        parser.statement.accountId = self.settings['account']
        parser.statement.bankId = self.settings.get('bank', 'Danske')
        if self.settings.getboolean('use-details-for-memo'):
            parser.use_details_for_memo()
        return parser
