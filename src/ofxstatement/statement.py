"""Statement model"""

from datetime import datetime
from decimal import Decimal as D
from hashlib import sha1


TRANSACTION_TYPES = [
    "CREDIT",       # Generic credit
    "DEBIT",        # Generic debit
    "INT",          # Interest earned or paid
    "DIV",          # Dividend
    "FEE",          # FI fee
    "SRVCHG",       # Service charge
    "DEP",          # Deposit
    "ATM",          # ATM debit or credit
    "POS",          # Point of sale debit or credit
    "XFER",         # Transfer
    "CHECK",        # Check
    "PAYMENT",      # Electronic payment
    "CASH",         # Cash withdrawal
    "DIRECTDEP",    # Direct deposit
    "DIRECTDEBIT",  # Merchant initiated debit
    "REPEATPMT",    # Repeating payment/standing order
    "OTHER"         # Other
]

ACCOUNT_TYPE = [
    "CHECKING",     # Checking
    "SAVINGS",      # Savings
    "MONEYMRKT",    # Money Market
    "CREDITLINE",   # Line of credit
]


class Statement(object):
    """Statement object containing statement items"""
    lines = None

    currency = None
    bank_id = None
    account_id = None
    # Type of account, must be one of ACCOUNT_TYPE
    account_type = None

    start_balance = None
    start_date = None

    end_balance = None
    end_date = None

    def __init__(self, bank_id=None, account_id=None,
                 currency=None, account_type="CHECKING"):
        self.lines = []
        self.bank_id = bank_id
        self.account_id = account_id
        self.currency = currency
        self.account_type = account_type


class StatementLine(object):
    """Statement line data.

    All fields are initialized with some sample data so that field type may be
    determined by interested parties. Constructor will reinitialize them to
    None (by default)
    """
    id = ""
    # Date transaction was posted to account
    date = datetime.now()
    memo = ""

    # Amount of transaction
    amount = D(0)

    # additional fields
    payee = ""

    # Date user initiated transaction, if known
    date_user = datetime.now()

    # Check (or other reference) number
    check_no = ""

    # Reference number that uniquely identifies the transaction. Can be used in
    # addition to or instead of a check_no
    refnum = ""

    # Transaction type, must be one of TRANSACTION_TYPES
    trntype = "CHECK"

    # Optional BankAccount instance
    bank_account_to = None

    def __init__(self, id=None, date=None, memo=None, amount=None):
        self.id = id
        self.date = date
        self.memo = memo
        self.amount = amount

        self.date_user = None
        self.payee = None
        self.check_no = None
        self.refnum = None

    def __str__(self):
        return """
        ID: %s, date: %s, amount: %s, payee: %s
        memo: %s
        check no.: %s
        """ % (self.id, self.date, self.amount, self.payee, self.memo,
               self.check_no)

    def assert_valid(self):
        """Ensure that fields have valid values
        """
        assert self.trntype in TRANSACTION_TYPES, \
            "trntype must be one of %s" % TRANSACTION_TYPES

        if self.bank_account_to:
            self.bank_account_to.assert_valid()


class BankAccount(object):
    """Structure corresponding to BANKACCTTO and BANKACCTFROM elements from OFX

    Open Financial Exchange uses the Banking Account aggregate to identify an
    account at an FI. The aggregate contains enough information to uniquely
    identify an account for the purposes of statement.
    """

    # Routing and transit number
    bank_id = ""
    # Bank identifier for international banks
    branch_id = ""
    # Account number
    acct_id = ""
    # Type of account, must be one of ACCOUNT_TYPE
    acct_type = ""
    # Checksum for international banks
    acct_key = ""

    def __init__(self, bank_id, acct_id, acct_type="CHECKING"):
        self.bank_id = bank_id
        self.acct_id = acct_id
        self.acct_type = acct_type

        self.branch_id = None
        self.acct_key = None

    def assert_valid(self):
        assert self.acct_type in ACCOUNT_TYPE, \
            "acct_type must be one of %s" % ACCOUNT_TYPE


def generate_transaction_id(stmt_line):
    """Generate pseudo-unique id for given statement line.

    This function can be used in statement parsers when real transaction id is
    not available in source statement.
    """
    h = sha1()
    h.update(stmt_line.date.strftime("%Y-%m-%d %H:%M:%S").encode("utf8"))
    h.update(stmt_line.memo.encode("utf8"))
    h.update(str(stmt_line.amount).encode("utf8"))
    return h.hexdigest()


def recalculate_balance(stmt):
    """Recalculate statement starting and ending dates and balances.

    When starting balance is not available, it will be assumed to be 0.

    This function can be used in statement parsers when balance information is
    not available in source statement.
    """

    total_amount = sum(sl.amount for sl in stmt.lines)

    stmt.start_balance = stmt.start_balance or D(0)
    stmt.end_balance = stmt.start_balance + total_amount
    stmt.start_date = min(sl.date for sl in stmt.lines)
    stmt.end_date = max(sl.date for sl in stmt.lines)
