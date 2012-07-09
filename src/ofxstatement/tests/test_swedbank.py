import doctest

from ofxstatement.plugins.swedbank import SwedbankCsvStatementParser

def doctest_SwedbankCsvStatementParser():
    """Test SwedbankCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'swedbank.csv')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='utf-8')
        >>> parser = SwedbankCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> statement.account_id
        'LT797300010XXXXXXXXX'
        >>> len(statement.lines)
        5
        >>> statement.start_balance
        2123.82
        >>> statement.start_date
        datetime.datetime(2012, 1, 1, 0, 0)
        >>> statement.end_balance
        3917.3
        >>> statement.end_date
        datetime.datetime(2012, 1, 31, 0, 0)
        >>> statement.currency
        'LTL'

    Check first line
        >>> l = statement.lines[0]
        >>> l.amount
        -14.34
        >>> l.payee
        "McDonald's restoranas AKR Vilnius"
        >>> l.memo
        "PIRKINYS ... 00000"
        >>> l.id
        '2012010200041787'
        >>> l.check_no
        '059553'
        >>> l.date
        datetime.datetime(2012, 1, 2, 0, 0)
        >>> l.date_user
        datetime.datetime(2011, 12, 30, 0, 0)

    Check line with awkward quotation marks:
        >>> l = statement.lines[2]
        >>> l.id
        '2012012600096815'
        >>> l.amount
        -12.2
        >>> l.payee
        'UAB "Naktida"'
        >>> l.memo
        'PIRKINYS 0000000000000000 ... UAB "Naktida" ... 00000'

    Check income line:
        >>> l = statement.lines[3]
        >>> l.id
        '2012011000673562'
        >>> l.amount
        1600.0
        >>> l.payee
        'Company'
        >>> l.memo
        'Salary'

    Check line with empty payee:
        >>> l = statement.lines[4]
        >>> l.id
        '2012022900875660'
        >>> l.payee
        ''


    """



def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
