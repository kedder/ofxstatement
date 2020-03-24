import unittest
from datetime import date
from decimal import Decimal

from ofxstatement import statement

class StatementTests(unittest.TestCase):
    def test_generate_transaction_id_idempotent(self):
        # GIVEN
        stl = statement.StatementLine(
            "one", date(2020, 3, 25), memo='123', amount=Decimal("12.43"))
        tid1 = statement.generate_transaction_id(stl)

        # WHEN
        # Subsequent calls with the same data generates exactly the same
        # transaction id
        tid2 = statement.generate_transaction_id(stl)

        # THEN
        self.assertEqual(tid1, tid2)

    def test_generate_transaction_id_identifying(self):
        # GIVEN
        stl = statement.StatementLine(
            "one", date(2020, 3, 25), memo='123', amount=Decimal("12.43"))
        tid1 = statement.generate_transaction_id(stl)

        # WHEN
        # Different data generates different transaction id
        stl.amount = Decimal("1.01")
        tid2 = statement.generate_transaction_id(stl)

        # THEN
        self.assertNotEqual(tid1, tid2)

    def test_generate_unique_transaction_id(self):
        # GIVEN
        stl = statement.StatementLine("one", date(2020, 3, 25))
        txnids = set()

        # WHEN
        tid1 = statement.generate_unique_transaction_id(stl, txnids)
        tid2 = statement.generate_unique_transaction_id(stl, txnids)

        self.assertNotEqual(tid1, tid2)

        self.assertTrue(tid2.endswith("-1"))
        self.assertEqual(len(txnids), 2)