"""Statement model"""

class Statement(object):
    """Statement object containing statement items"""
    lines = None

    currency = None
    bankId = None
    accountId = None

    def __init__(self, bankId, accountId, currency):
        self.lines = []
        self.bankId = bankId
        self.accountId = accountId
        self.currency = currency

class StatementLine(object):
    """Statement line data"""
    id = None
    date = None
    memo = None
    amount = None

    # additional fields
    dateUser = None
    payee = None

    def __init__(self, id, date, memo, amount):
        self.id = id
        self.date = date
        self.memo = memo
        self.amount = amount
