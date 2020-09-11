class Abort(Exception):
    pass


class ParseError(Exception):
    """Raised by parser to indicate malformed input"""

    def __init__(self, lineno: int, message: str) -> None:
        self.lineno = lineno
        self.message = message


class ValidationError(Exception):  # pragma: no cover
    """Raised by parser to indicate validation errors for an object"""

    def __init__(self, message: str, obj: object) -> None:
        self.message = message
        self.obj = obj

    def __str__(self) -> str:
        return "message: %s; object:\n%r" % (self.message, self.obj)
