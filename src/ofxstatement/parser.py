import csv
from decimal import Decimal, Decimal as D
from datetime import datetime

from ofxstatement.statement import Statement, StatementLine


class StatementParser(object):
    """Abstract statement parser.

    Defines interface for all parser implementation
    """

    date_format = "%Y-%m-%d"
    cur_record = 0

    def __init__(self):
        self.statement = Statement()
        
    def parse(self):
        """Read and parse statement

        Return Statement object

        May raise exceptions.ParseException on malformed input.
        """
        assert hasattr(self, 'statement'), "StatementParser.__init__() not called"
        
        reader = self.split_records()
        for line in reader:
            self.cur_record += 1
            if not line:
                continue
            stmt_line = self.parse_record(line)
            if stmt_line:
                stmt_line.assert_valid()
                self.statement.lines.append(stmt_line)
        return self.statement

    def split_records(self):  # pragma: no cover
        """Return iterable object consisting of a line per transaction
        """
        raise NotImplementedError

    def parse_record(self, line):  # pragma: no cover
        """Parse given transaction line and return StatementLine object
        """
        raise NotImplementedError

    def parse_value(self, value, field):
        tp = type(getattr(StatementLine, field))
        if tp == datetime:
            return self.parse_datetime(value)
        elif tp == Decimal:
            return self.parse_decimal(value)
        else:
            return value

    def parse_datetime(self, value):
        return datetime.strptime(value, self.date_format)

    def parse_float(self, value):  # pragma: no cover
        # compatibility wrapper for old plugins
        return self.parse_decimal(value)

    def parse_decimal(self, value):
        # some plugins pass localised numbers, clean them up
        return D(value.replace(",", ".").replace(" ", ""))


class CsvStatementParser(StatementParser):
    """Generic csv statement parser"""

    statement = None
    fin = None  # file input stream

    # 0-based csv column mapping to StatementLine field
    mappings = {}

    def __init__(self, fin):
        super().__init__()
        self.fin = fin

    def split_records(self):
        return csv.reader(self.fin)

    def parse_record(self, line):
        stmt_line = StatementLine()
        for field, col in self.mappings.items():
            if col >= len(line):
                raise ValueError("Cannot find column %s in line of %s items "
                                 % (col, len(line)))
            rawvalue = line[col]
            value = self.parse_value(rawvalue, field)
            setattr(stmt_line, field, value)
        return stmt_line
