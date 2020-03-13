class Abort(Exception):
    pass


class ParseError(Exception):
    """Raised by parser to indicate malformed input
    """
    def __init__(self, lineno, message):
        self.lineno = lineno
        self.message = message


class ValidationError(Exception):  # pragma: no cover
    """Raised by parser to indicate validation errors for an object
    """
    def __init__(self, message, obj):
        self.message = message
        self.obj = obj

    def __str__(self):
        return "message: %s; object:\n%r" % (self.message, self.obj)
