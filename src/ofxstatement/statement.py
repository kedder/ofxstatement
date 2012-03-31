"""Statement model"""

from datetime import datetime

class Statement(object):
    """Statement object containing statement items"""
    lines = None

    currency = None
    bankId = None
    accountId = None

    startingBalance = None
    startingBalanceDate = None

    endingBalance = None
    endingBalanceDate = None

    def __init__(self, bankId=None, accountId=None, currency=None):
        self.lines = []
        self.bankId = bankId
        self.accountId = accountId
        self.currency = currency

class StatementLine(object):
    """Statement line data.

    All fields are initialized with some sample data so that field type may be
    determined by interested parties. Constructor will reinitialize them to
    None (by default)
    """
    id = ""
    date = datetime.now()
    memo = ""
    amount = 0.0

    # additional fields
    payee = ""
    dateUser = ""
    checkNumber = ""

    def __init__(self, id=None, date=None, memo=None, amount=None):
        self.id = id
        self.date = date
        self.memo = memo
        self.amount = amount

        self.dateUser = None
        self.payee = None
        self.checkNumber = None

    def __str__(self):
        return """
        ID: %s, date: %s, amount: %s, payee: %s
        memo: %s
        check no.: %s
        """ % (self.id, self.date, self.amount, self.payee, self.memo,
            self.checkNumber)


def generate_transaction_id(statementLine):
    """Generate pseudo-unique id for given statement line.

    This function can be used in statement parsers when real transaction id is
    not available in source statement.
    """
    return str(abs(hash((statementLine.date,
                         statementLine.memo,
                         StatementLine.amount))))

def recalculate_balance(stmt):
    """Recalculate statement starting and ending dates and balances.

    When starting balance is not available, it will be assumed to be 0.

    This function can be used in statement parsers when balance information is
    not available in source statement.
    """

    total_amount = sum(sl.amount for sl in stmt.lines)

    stmt.startingBalance = stmt.startingBalance or 0.0
    stmt.endingBalance = stmt.startingBalance + total_amount;
    stmt.startingBalanceDate = min(sl.date for sl in stmt.lines)
    stmt.endingBalanceDate = max(sl.date for sl in stmt.lines)
