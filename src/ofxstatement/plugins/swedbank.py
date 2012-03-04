"""Parser implementation for swedbank generated statement reports"""

import sys

from ofxstatement.parser import CsvStatementParser

LINETYPE_TRANSACTION = "20"
LINETYPE_STARTBALANCE = "10"
LINETYPE_ENDBALANCE = "86"

class SwedbankCsvStatementParser(CsvStatementParser):
    mappings = {"date": 2,
                "payee": 3,
                "memo": 4,
                "amount": 5,
                "id": 8,
                "checkNumber": 8}

    def createReader(self):
        # We cannot parse swedbank csv as regular csv because swedbanks format
        # uses unescaped quote symbols.
        return self.fin.readlines()

    def parseLine(self, line):
        if not line.strip():
            return None

        if self.currentLine == 1:
            # Skip header line
            return None

        # Split line to the parts and strip quotes around fields
        parts = [l[1:] for l in line.split('",')]
        if not self.statement.accountId:
            self.statement.accountId = parts[0]
        if not self.statement.currency:
            self.statement.currency = parts[6]

        lineType = parts[1]

        if lineType == LINETYPE_TRANSACTION:
            line = super(SwedbankCsvStatementParser, self).parseLine(parts)
            if parts[7] == "D":
                line.amount = -line.amount
            return line
        elif lineType == LINETYPE_ENDBALANCE:
            self.statement.endingBalance = self.parseFloat(parts[5])
            self.statement.endingBalanceDate = self.parseDateTime(parts[2])
        elif lineType == LINETYPE_STARTBALANCE:
            self.statement.startingBalance = self.parseFloat(parts[5])
            self.statement.startingBalanceDate = self.parseDateTime(parts[2])
