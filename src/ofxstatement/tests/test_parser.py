import io
from textwrap import dedent
from unittest import TestCase
from decimal import Decimal

from ofxstatement.parser import CsvStatementParser

class CsvStatementParserTest(TestCase):

    def test_simple_csv_parser(self):
        # Test generic CsvStatementParser

        # Lets define some sample csv to parse and write it to file-like object
        csv = dedent('''
            "2012-01-18","Microsoft","Windows XP",243.32,"1001"
            "2012-02-14","Google","Adwords",23.54,"1002"
            ''')
        f = io.StringIO(csv)

        # Create and configure csv parser:
        parser = CsvStatementParser(f)
        parser.mappings = {
            "date": 0,
            "payee": 1,
            "memo": 2,
            "amount": 3,
            "id": 4
        }

        # And parse csv:
        statement = parser.parse()
        self.assertEqual(len(statement.lines), 2)
        self.assertEqual(statement.lines[0].amount, Decimal('243.32'))
        self.assertEqual(statement.lines[1].payee, 'Google')
