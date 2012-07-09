import unittest
import os.path
from ofxstatement.plugins.maxibps import PSTextFormatParser


class Test_Parser(unittest.TestCase):
    def setUp(self):
        test_file_name = os.path.join(os.path.dirname(__file__),
            "samples", "maxibps.txt")
        test_file = open(test_file_name, "U", encoding="utf-8-sig")
        self.parser = PSTextFormatParser(test_file)

    def test_parser(self):
        records = self.parser.split_records()
        self.assertEqual(len(records), 3,
                "split the input file into records\nrecords = %s"
                % records)

    def test_parseLine(self):
        for rec_str in self.parser.split_records():
            rec = self.parser.parse_record(rec_str)
            self.assertIsNotNone(rec, "StatementLine created")

if __name__ == "__main__":
    unittest.main()
