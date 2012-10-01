import doctest

from ofxstatement.plugins.litas_esis import LitasEsisCsvStatementParser


def doctest_LitasEsisCsvStatementParser():
    """Test LitasEsisCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'litas_esis.acc')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='cp1257')
        >>> parser = LitasEsisCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> statement.account_id
        'LT000000000000000000LTL'
        >>> len(statement.lines)
        7
        >>> statement.start_balance
        251.75
        >>> statement.start_date
        datetime.datetime(2012, 1, 1, 0, 0)
        >>> statement.end_balance
        74.83
        >>> statement.end_date
        datetime.datetime(2012, 3, 4, 0, 0)
        >>> statement.currency
        'LTL'

    Check first line:
        >>> l = statement.lines[0]
        >>> l.amount
        -1.0
        >>> l.payee
        'AB DNB BANKAS'
        >>> l.memo
        'Mokestis už sąskaitos aptarnavimą'
        >>> l.id
        '1987555498'

    Check credit line:
        >>> l = statement.lines[3]
        >>> l.amount
        300.0
        >>> l.payee
        'LINUS TORVALDS'
        >>> l.memo
        'Hello World'
        >>> l.id
        '2003969289'

    """
def doctest_LitasEsisCsvStatementParser_swap_payee_memo():
    """Test ability to swap payee and memo in LitasEsisCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'litas_esis.acc')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='cp1257')
        >>> parser = LitasEsisCsvStatementParser(fin)
        >>> parser.swap_payee_and_memo()
        >>> statement = parser.parse()

    Memo and payee should be swapped
        >>> l = statement.lines[3]
        >>> l.memo
        'LINUS TORVALDS'
        >>> l.payee
        'Hello World'
    """

def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
