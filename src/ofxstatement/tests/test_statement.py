from typing import Set
import unittest
from datetime import datetime
from decimal import Decimal

from ofxstatement import statement


class StatementTests(unittest.TestCase):
    def test_generate_transaction_id_idempotent(self) -> None:
        # GIVEN
        stl = statement.StatementLine(
            "one", datetime(2020, 3, 25), memo="123", amount=Decimal("12.43")
        )
        tid1 = statement.generate_transaction_id(stl)

        # WHEN
        # Subsequent calls with the same data generates exactly the same
        # transaction id
        tid2 = statement.generate_transaction_id(stl)

        # THEN
        self.assertEqual(tid1, tid2)

    def test_generate_transaction_id_identifying(self) -> None:
        # GIVEN
        stl = statement.StatementLine(
            "one", datetime(2020, 3, 25), memo="123", amount=Decimal("12.43")
        )
        tid1 = statement.generate_transaction_id(stl)

        # WHEN
        # Different data generates different transaction id
        stl.amount = Decimal("1.01")
        tid2 = statement.generate_transaction_id(stl)

        # THEN
        self.assertNotEqual(tid1, tid2)

    def test_generate_unique_transaction_id(self) -> None:
        # GIVEN
        stl = statement.StatementLine("one", datetime(2020, 3, 25))
        txnids: Set[str] = set()

        # WHEN
        tid1 = statement.generate_unique_transaction_id(stl, txnids)
        tid2 = statement.generate_unique_transaction_id(stl, txnids)

        self.assertNotEqual(tid1, tid2)

        self.assertTrue(tid2.endswith("-1"))
        self.assertEqual(len(txnids), 2)

    def test_transfer_line_validation(self) -> None:
        line = statement.InvestStatementLine("id", datetime(2020, 3, 25))
        line.trntype = "TRANSFER"
        line.security_id = "ABC"
        line.units = Decimal(2)
        line.assert_valid()
        with self.assertRaises(AssertionError):
            line.security_id = None
            line.assert_valid()
        line.security_id = "ABC"
        with self.assertRaises(AssertionError):
            line.units = None
            line.assert_valid()
        line.units = Decimal(2)
        with self.assertRaises(AssertionError):
            line.trntype_detailed = "DETAIL"
            line.assert_valid()

    def test_invbank_line_validation(self) -> None:
        line = statement.InvestStatementLine("id", datetime(2020, 3, 25))
        line.trntype = "INVBANKTRAN"
        line.trntype_detailed = "INT"
        line.amount = Decimal(1)
        line.assert_valid()
        with self.assertRaises(AssertionError):
            line.amount = None
            line.assert_valid()
        line.amount = Decimal(1)
        with self.assertRaises(AssertionError):
            line.trntype_detailed = "BLAH"
            line.assert_valid()

    def test_income_line_validation(self) -> None:
        line = statement.InvestStatementLine("id", datetime(2020, 3, 25))
        line.trntype = "INCOME"
        line.trntype_detailed = "INTEREST"
        line.amount = Decimal(1)
        line.security_id = "AAPL"
        line.assert_valid()
        with self.assertRaises(AssertionError):
            line.amount = None
            line.assert_valid()
        line.amount = Decimal(1)
        with self.assertRaises(AssertionError):
            line.trntype_detailed = "BLAH"
            line.assert_valid()
        line.trntype_detailed = "INTEREST"
        with self.assertRaises(AssertionError):
            line.security_id = None
            line.assert_valid()

    def test_buy_line_validation(self) -> None:
        line = statement.InvestStatementLine("id", datetime(2020, 3, 25))
        line.trntype = "BUYSTOCK"
        line.trntype_detailed = "BUY"
        line.amount = Decimal(1)
        line.security_id = "AAPL"
        line.units = Decimal(3)
        line.unit_price = Decimal(1.1)
        line.assert_valid()

        with self.assertRaises(AssertionError):
            line.amount = None
            line.assert_valid()
        line.amount = Decimal(1)

        with self.assertRaises(AssertionError):
            line.trntype_detailed = "BLAH"
            line.assert_valid()
        line.trntype_detailed = "INTEREST"

        with self.assertRaises(AssertionError):
            line.security_id = None
            line.assert_valid()
        line.security_id = "AAPL"

        with self.assertRaises(AssertionError):
            line.units = None
            line.assert_valid()
        line.units = Decimal(3)

        with self.assertRaises(AssertionError):
            line.unit_price = None
            line.assert_valid()
