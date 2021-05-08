from typing import Dict, Optional, Any, Iterable, List, TextIO, TypeVar, Generic
from abc import abstractmethod
import csv
from decimal import Decimal, Decimal as D
from datetime import datetime

from ofxstatement.statement import Statement, StatementLine

LT = TypeVar("LT")


class AbstractStatementParser:
    @abstractmethod
    def parse(self) -> Statement:
        """Parse the input and produce the statement object"""


class StatementParser(AbstractStatementParser, Generic[LT]):
    """Abstract statement parser.

    Defines interface for all parser implementation
    """

    statement: Statement

    date_format: str = "%Y-%m-%d"
    cur_record: int = 0

    def __init__(self) -> None:
        self.statement = Statement()

    def parse(self) -> Statement:
        """Read and parse statement

        Return Statement object

        May raise exceptions.ParseException on malformed input.
        """
        assert hasattr(self, "statement"), "StatementParser.__init__() not called"

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

    def split_records(self) -> Iterable[LT]:  # pragma: no cover
        """Return iterable object consisting of a line per transaction"""
        raise NotImplementedError

    def parse_record(self, line: LT) -> Optional[StatementLine]:  # pragma: no cover
        """Parse given transaction line and return StatementLine object"""
        raise NotImplementedError

    def parse_value(self, value: Optional[str], field: str) -> Any:
        tp = StatementLine.__annotations__.get(field)
        if value is None:
            return None

        if tp in (datetime, Optional[datetime]):
            return self.parse_datetime(value)
        elif tp in (Decimal, Optional[Decimal]):
            return self.parse_decimal(value)
        else:
            return value

    def parse_datetime(self, value: str) -> datetime:
        return datetime.strptime(value, self.date_format)

    def parse_float(self, value: str) -> D:  # pragma: no cover
        # compatibility wrapper for old plugins
        return self.parse_decimal(value)

    def parse_decimal(self, value: str) -> D:
        # some plugins pass localised numbers, clean them up
        return D(value.replace(",", ".").replace(" ", ""))


class CsvStatementParser(StatementParser[List[str]]):
    """Generic csv statement parser"""

    fin: TextIO  # file input stream

    # 0-based csv column mapping to StatementLine field
    mappings: Dict[str, int] = {}

    def __init__(self, fin: TextIO) -> None:
        super().__init__()
        self.fin = fin

    def split_records(self) -> Iterable[List[str]]:
        return csv.reader(self.fin)

    def parse_record(self, line: List[str]) -> Optional[StatementLine]:
        stmt_line = StatementLine()
        for field, col in self.mappings.items():
            if col >= len(line):
                raise ValueError(
                    "Cannot find column %s in line of %s items " % (col, len(line))
                )
            rawvalue = line[col]
            value = self.parse_value(rawvalue, field)
            setattr(stmt_line, field, value)
        return stmt_line
