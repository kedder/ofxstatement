import unittest
import os.path
from ofxstatement.plugins.maxibps import PSTextFormatParser


class Test_Parser(unittest.TestCase):
    def setUp(self):
        self.test_file = open(os.path.join(os.path.dirname(__file__),
            "samples", "maxibps.txt"))

    def test_parser(self):
        parser = PSTextFormatParser(self.test_file)
        records = parser.createReader()
        self.assertEqual(len(records), 3, "split the input file into records")

    def test_parseLine(self):
        parser = PSTextFormatParser(self.test_file)
        for rec_str in parser.createReader():
            rec = parser.parseLine(rec_str)
            self.assertIsNotNone(rec, "StatementLine created")

if __name__ == "__main__":
    unittest.main()
