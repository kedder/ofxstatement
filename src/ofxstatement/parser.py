import sys
import csv
from datetime import datetime

from ofxstatement.statement import Statement, StatementLine

class StatementParser(object):
    """Abstract statement parser.

    Defines interface for all parser implementation
    """

    date_format = "%Y-%m-%d"
    cur_record = 0

    def parse(self):
        """Read and parse statement

        Return Statement object
        """
        reader = self.split_records()
        for line in reader:
            self.cur_record += 1
            if not line:
                continue
            stmt_line = self.parse_record(line)
            if (stmt_line):
                self.statement.lines.append(stmt_line)
        return self.statement

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        raise NotImplementedError

    def parse_record(self, line):
        """Parse given transaction line and return StatementLine object
        """
        raise NotImplementedError

    def parse_value(self, value, field):
        tp = type(getattr(StatementLine, field))
        if tp == datetime:
            return self.parse_datetime(value)
        elif tp == float:
            return self.parse_float(value)
        else:
            return value

    def parse_datetime(self, value):
        return datetime.strptime(value, self.date_format)

    def parse_float(self, value):
        return float(value)


class CsvStatementParser(StatementParser):
    """Generic csv statement parser"""

    statement = None
    fin = None  # file input stream

    # 0-based csv column mapping to StatementLine field
    mappings = {}

    def __init__(self, fin):
        self.statement = Statement()
        self.fin = fin

    def split_records(self):
        return csv.reader(self.fin)

    def parse_record(self, line):
        stmt_line = StatementLine()
        for field, col in self.mappings.items():
            if col >= len(line):
                raise ValueError("Cannot find column %s in line of %s items " \
                                 % (col, len(line)))
            rawvalue = line[col]
            value = self.parse_value(rawvalue, field)
            setattr(stmt_line, field, value)
        return stmt_line
