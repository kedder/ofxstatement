"""Statement model"""

class Statement(object):
    """Statement object containing statement items"""
    lines = None

    def __init__(self):
        self.lines = []

class StatementLine(object):
    """Statement line data"""
    date = None
    currency = None
    description = None
    amount = None
