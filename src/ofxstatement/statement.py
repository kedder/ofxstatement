"""Statement model"""

from datetime import datetime

class Statement(object):
    """Statement object containing statement items"""
    lines = None

    currency = None
    bank_id = None
    account_id = None

    start_balance = None
    start_date = None

    end_balance = None
    end_date = None

    def __init__(self, bank_id=None, account_id=None, currency=None):
        self.lines = []
        self.bank_id = bank_id
        self.account_id = account_id
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
    date_user = ""
    check_no = ""

    def __init__(self, id=None, date=None, memo=None, amount=None):
        self.id = id
        self.date = date
        self.memo = memo
        self.amount = amount

        self.date_user = None
        self.payee = None
        self.check_no = None

    def __str__(self):
        return """
        ID: %s, date: %s, amount: %s, payee: %s
        memo: %s
        check no.: %s
        """ % (self.id, self.date, self.amount, self.payee, self.memo,
               self.check_no)


def generate_transaction_id(stmt_line):
    """Generate pseudo-unique id for given statement line.

    This function can be used in statement parsers when real transaction id is
    not available in source statement.
    """
    return str(abs(hash((stmt_line.date,
                         stmt_line.memo,
                         stmt_line.amount))))

def recalculate_balance(stmt):
    """Recalculate statement starting and ending dates and balances.

    When starting balance is not available, it will be assumed to be 0.

    This function can be used in statement parsers when balance information is
    not available in source statement.
    """

    total_amount = sum(sl.amount for sl in stmt.lines)

    stmt.start_balance = stmt.start_balance or 0.0
    stmt.end_balance = stmt.start_balance + total_amount;
    stmt.start_date = min(sl.date for sl in stmt.lines)
    stmt.end_date = max(sl.date for sl in stmt.lines)
