import doctest

from ofxstatement.plugins.dkb_cc import DKBCCCsvStatementParser

def doctest_DKBCCCsvStatementParser():
    """Test DKBCCCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'dkbcc.csv')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='iso-8859-1')
        >>> parser = DKBCCCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> statement.account_id
        >>> len(statement.lines)
        7
        >>> statement.start_balance       
        >>> statement.start_date
        datetime.datetime(2012, 2, 7, 0, 0)
        >>> statement.end_balance
        -76.77
        >>> statement.end_date
        datetime.datetime(2013, 2, 4, 0, 0)
        >>> statement.currency
        'EUR'

    Check first line
        >>> l = statement.lines[0]
        >>> l.amount
        -95.0
        >>> l.payee 
        >>> l.memo
        'MY BANK FIL'
        >>> l.date
        datetime.datetime(2013, 2, 4, 0, 0)

    Check one more lines:
        >>> l=statement.lines[2]
        >>> l.amount
        0.21
        >>> l.payee
        >>> l.memo
        'HabenzinsenZ 000000057 T 031   0000'
        >>> l.date
        datetime.datetime(2013, 1, 23, 0, 0)

    """



def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
