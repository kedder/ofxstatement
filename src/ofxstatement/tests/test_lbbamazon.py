import doctest

from ofxstatement.plugins.lbbamazon import LbbAmazonCsvStatementParser

def doctest_LbbAmazonCsvStatementParser():
    """Test LbbAmazonCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'lbbamazon.csv')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='iso-8859-1')
        >>> parser = LbbAmazonCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> statement.account_id
        >>> len(statement.lines)
        7
        >>> statement.start_balance
        >>> statement.start_date
        >>> statement.end_balance
        >>> statement.end_date
        >>> statement.currency

    Check first line
        >>> l = statement.lines[0]
        >>> l.amount
        -0.17
        >>> l.payee 
        >>> l.memo
        'ABGELTUNGSSTEUER'
        >>> l.date
        datetime.datetime(2012, 12, 28, 0, 0)

    Check one more line:
        >>> l=statement.lines[2]
        >>> l.amount
        0.75
        >>> l.payee
        >>> l.memo
        'HANDYRABATT'
        >>> l.date
        datetime.datetime(2013, 1, 21, 0, 0)

    Check one more line with slashes in memo:
        >>> l=statement.lines[4]
        >>> l.amount
        -30.0
        >>> l.memo
        'AMAZON.ES COMPRA / amazon.es/ay'
        >>> l.date
        datetime.datetime(2013, 1, 7, 0, 0)

    Check one more line with amazon points but without amount:
        >>> l=statement.lines[5]
        >>> l.amount
        0.0
        >>> l.memo
        '+ 15.0 AMAZON.DE PUNKTE'
        >>> l.date
        datetime.datetime(2013, 1, 7, 0, 0)
              
    """

def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite

#if __name__ == "__main__":
#    doctest.testmod()

