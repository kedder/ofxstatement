class Abort(Exception):
    pass


class ParseError(Exception):
    """Raised by parser to indicate malformed input
    """
    def __init__(self, lineno, message):
        self.lineno = lineno
        self.message = message

class DownloadError(Exception):
    """Raised by downloader to indicate problem on web scraper
    """
    def __init__(self, message):
        self.message = message
