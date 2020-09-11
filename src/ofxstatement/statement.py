"""Statement model"""
from typing import List, Optional
from datetime import datetime
from decimal import Decimal as D
from hashlib import sha1
from pprint import pformat
from math import isclose

from ofxstatement import exceptions

TRANSACTION_TYPES = [
    "CREDIT",  # Generic credit
    "DEBIT",  # Generic debit
    "INT",  # Interest earned or paid
    "DIV",  # Dividend
    "FEE",  # FI fee
    "SRVCHG",  # Service charge
    "DEP",  # Deposit
    "ATM",  # ATM debit or credit
    "POS",  # Point of sale debit or credit
    "XFER",  # Transfer
    "CHECK",  # Check
    "PAYMENT",  # Electronic payment
    "CASH",  # Cash withdrawal
    "DIRECTDEP",  # Direct deposit
    "DIRECTDEBIT",  # Merchant initiated debit
    "REPEATPMT",  # Repeating payment/standing order
    "OTHER",  # Other
]

ACCOUNT_TYPE = [
    "CHECKING",  # Checking
    "SAVINGS",  # Savings
    "MONEYMRKT",  # Money Market
    "CREDITLINE",  # Line of credit
]


# Inspired by "How to print instances of a class using print()?"
# on stackoverflow.com
class Printable:
    def __repr__(self) -> str:  # pragma: no cover
        # do not set width to 1 because that makes the output really ugly
        return "<" + type(self).__name__ + "> " + pformat(vars(self), indent=4)


class Statement(Printable):
    """Statement object containing statement items"""

    lines: List["StatementLine"]

    currency: Optional[str] = None
    bank_id: Optional[str] = None
    account_id: Optional[str] = None
    # Type of account, must be one of ACCOUNT_TYPE
    account_type: Optional[str] = None

    start_balance: Optional[D] = None
    start_date: Optional[datetime] = None

    end_balance: Optional[D] = None
    end_date: Optional[datetime] = None

    def __init__(
        self,
        bank_id: str = None,
        account_id: str = None,
        currency: str = None,
        account_type: str = "CHECKING",
    ) -> None:
        self.lines = []
        self.bank_id = bank_id
        self.account_id = account_id
        self.currency = currency
        self.account_type = account_type

    def assert_valid(self) -> None:  # pragma: no cover
        if not (self.start_balance is None or self.end_balance is None):
            total_amount = sum(
                [sl.amount for sl in self.lines if sl.amount is not None], D(0)
            )

            msg = (
                "Start balance ({0}) plus the total amount ({1}) "
                "should be equal to the end balance ({2})".format(
                    self.start_balance, total_amount, self.end_balance
                )
            )
            if not isclose(self.start_balance + total_amount, self.end_balance):
                raise exceptions.ValidationError(msg, self)


class StatementLine(Printable):
    """Statement line data. """

    id: Optional[str]
    # Date transaction was posted to account
    date: Optional[datetime]
    memo: Optional[str]

    # Amount of transaction
    amount: Optional[D]

    # additional fields
    payee: Optional[str]

    # Date user initiated transaction, if known
    date_user: Optional[datetime]

    # Check (or other reference) number
    check_no: Optional[str]

    # Reference number that uniquely identifies the transaction. Can be used in
    # addition to or instead of a check_no
    refnum: Optional[str]

    # Transaction type, must be one of TRANSACTION_TYPES
    trntype: Optional[str] = "CHECK"

    # Optional BankAccount instance
    bank_account_to: Optional["BankAccount"] = None

    def __init__(
        self, id: str = None, date: datetime = None, memo: str = None, amount: D = None
    ) -> None:
        self.id = id
        self.date = date
        self.memo = memo
        self.amount = amount

        self.date_user = None
        self.payee = None
        self.check_no = None
        self.refnum = None

    def __str__(self) -> str:  # pragma: no cover
        return """
        ID: %s, date: %s, amount: %s, payee: %s
        memo: %s
        check no.: %s
        """ % (
            self.id,
            self.date,
            self.amount,
            self.payee,
            self.memo,
            self.check_no,
        )

    def assert_valid(self) -> None:
        """Ensure that fields have valid values"""
        assert self.trntype in TRANSACTION_TYPES, (
            "trntype must be one of %s" % TRANSACTION_TYPES
        )

        if self.bank_account_to:
            self.bank_account_to.assert_valid()

        assert self.id or self.check_no or self.refnum


class BankAccount(Printable):
    """Structure corresponding to BANKACCTTO and BANKACCTFROM elements from OFX

    Open Financial Exchange uses the Banking Account aggregate to identify an
    account at an FI. The aggregate contains enough information to uniquely
    identify an account for the purposes of statement.
    """

    # Routing and transit number
    bank_id: str
    # Bank identifier for international banks
    branch_id: Optional[str] = None
    # Account number
    acct_id: str
    # Type of account, must be one of ACCOUNT_TYPE
    acct_type: str
    # Checksum for international banks
    acct_key: Optional[str] = None

    def __init__(self, bank_id: str, acct_id: str, acct_type: str = "CHECKING") -> None:
        self.bank_id = bank_id
        self.acct_id = acct_id
        self.acct_type = acct_type

        self.branch_id = None
        self.acct_key = None

    def assert_valid(self) -> None:
        assert self.acct_type in ACCOUNT_TYPE, (
            "acct_type must be one of %s" % ACCOUNT_TYPE
        )


def generate_transaction_id(stmt_line: StatementLine) -> str:
    """Generate pseudo-unique id for given statement line.

    This function can be used in statement parsers when real transaction id is
    not available in source statement.
    """
    h = sha1()
    assert stmt_line.date is not None
    h.update(stmt_line.date.strftime("%Y-%m-%d %H:%M:%S").encode("utf8"))
    if stmt_line.memo is not None:
        h.update(stmt_line.memo.encode("utf8"))
    if stmt_line.amount is not None:
        h.update(str(stmt_line.amount).encode("utf8"))
    return h.hexdigest()


def generate_unique_transaction_id(stmt_line: StatementLine, unique_id_set: set) -> str:
    """
    Generate a unique transaction id.

    A bit of background: the problem with these transaction id's is that
    they do do not only have to be unique, they also have to stay the same
    for the same transaction every time you generate the statement.  So
    generating random ids will not work, even though they will be unique,
    GnuCash or beancount will recognize these transaction as "new" if you
    happen to generate and import the same statement twice or import two
    statements with overlapping periods.

    The function generate_transaction_id() is deterministic, but does not
    necesserily generate an unique id.

    Therefore this function improves on it since you can create a
    really unique id by adding an increment to the generated id (a string)
    and keep on incrementing till it succeeds.

    These are the steps:
    1) supply a unique id set you want to use for checking uniqueness
    2) next you generate an initial id by calling
       generate_transaction_id()
    3) assign the initial id to the current id (id)
    4) increment a counter while the current id is a member of the set and
       add the counter to the initial id and assign that to the current id
    5) add the current id to the unique id set
    6) return a list of the current id and the counter (if not 0)

    The counter is returned in order to enable the caller to modify
    its statement line, for example the memo field.
    """
    # Save the initial id
    id = initial_id = generate_transaction_id(stmt_line)
    counter = 0
    while id in unique_id_set:
        counter += 1
        id = initial_id + str(counter)

    unique_id_set.add(id)
    return id + ("" if counter == 0 else "-" + str(counter))


def recalculate_balance(stmt: Statement) -> None:
    """Recalculate statement starting and ending dates and balances.

    When starting balance is not available, it will be assumed to be 0.

    This function can be used in statement parsers when balance information is
    not available in source statement.
    """

    total_amount = sum([sl.amount for sl in stmt.lines if sl.amount is not None], D(0))

    stmt.start_balance = stmt.start_balance or D(0)
    stmt.end_balance = stmt.start_balance + total_amount
    stmt.start_date = min(sl.date for sl in stmt.lines)
    stmt.end_date = max(sl.date for sl in stmt.lines)
