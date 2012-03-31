from ofxstatement.parser import CsvStatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import generate_transaction_id

class DanskeCsvStatementParser(CsvStatementParser):
    mappings = {"date": 0,
                "payee": 4,
                "memo": 5,
                "amount": 8
                }
    dateFormat = "%Y:%m:%d"

    def parseLine(self, line):
        if self.currentLine == 1:
            return None

        # fill statement line according to mappings
        sl = super(DanskeCsvStatementParser, self).parseLine(line)

        # generate transaction id out of available data
        sl.id = generate_transaction_id(sl)
        return sl


class DanskePlugin(Plugin):
    name = "danske"

    def get_parser(self, fin):
        f = open(fin, "r")
        return DanskeCsvStatementParser(f)
