import sys
import csv
from datetime import datetime

from ofxstatement.statement import Statement, StatementLine

class StatementParser(object):
    """Abstract statement parser.

    Defines interface for all parser implementation
    """

    dateFormat = "%Y-%m-%d"

    def parse(self):
        """Read and parse statement

        Return Statement object
        """
        reader = self.createReader()
        for line in reader:
            self.currentLine += 1
            if not line:
                continue
            stmtLine = self.parseLine(line)
            if (stmtLine):
                self.statement.lines.append(stmtLine)
        return self.statement

    def createReader(self):
        """Return iterable object consisting of a line per transaction
        """
        raise NotImplementedError

    def parseLine(self, line):
        """Parse given transaction line and return StatementLine object
        """
        raise NotImplementedError

    def parseValue(self, value, field):
        tp = type(getattr(StatementLine, field))
        if tp == datetime:
            return self.parseDateTime(value)
        elif tp == float:
            return self.parseFloat(value)
        else:
            return value

    def parseDateTime(self, value):
        return datetime.strptime(value, self.dateFormat)

    def parseFloat(self, value):
        return float(value)


class CsvStatementParser(StatementParser):
    """Generic csv statement parser"""

    statement = None
    fin = None  # file input stream

    # 0-based csv column mapping to StatementLine field
    mappings = {}

    currentLine = 0

    def __init__(self, fin):
        self.statement = Statement()
        self.fin = fin

    def createReader(self):
        return csv.reader(self.fin)

    def parseLine(self, line):
        stmtLine = StatementLine()
        for field, col in self.mappings.items():
            rawvalue = line[col]
            value = self.parseValue(rawvalue, field)
            setattr(stmtLine, field, value)
        return stmtLine
