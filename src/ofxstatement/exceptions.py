class Abort(Exception):
    pass


class ParseError(Exception):
    """Raised by parser to indicate malformed input
    """
    def __init__(self, lineno, message):
        self.lineno = lineno
        self.message = message
