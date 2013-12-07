import doctest

from ofxstatement.plugins.dab import DABCsvStatementParser


def doctest_DABCsvStatementParser():
    """Test DABCsvStatementParser

    Open sample csv to parse
        >>> import os
        >>> csvfile = os.path.join(os.path.dirname(__file__),
        ...                        'samples', 'dab.csv')

    Create parser object and parse:
        >>> fin = open(csvfile, 'r', encoding='utf-8')
        >>> parser = DABCsvStatementParser(fin)
        >>> statement = parser.parse()

    Check what we've got:
        >>> statement.account_id
        >>> len(statement.lines)
        7
        >>> statement.currency
        'EUR'

    Check first line
        >>> l = statement.lines[0]
        >>> l.amount
        -50.0
        >>> l.payee
        'MUSIKSCHULE'
        >>> l.memo
        'KLAVIERUNTERRICHT'
        >>> l.date
        datetime.datetime(2013, 10, 1, 0, 0)

    Check one more lines:
        >>> l=statement.lines[2]
        >>> l.amount
        -20.22
        >>> l.payee
        'REWE SAGT DANKE. 12300000'
        >>> l.memo
        'EC 87630123 ABCGFKK812430<br/> KLA277UNFTA'
        >>> l.date
        datetime.datetime(2013, 9, 30, 0, 0)

    """


def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE |
                                             doctest.ELLIPSIS |
                                             doctest.REPORT_ONLY_FIRST_FAILURE |
                                             doctest.REPORT_NDIFF
    ))


load_tests = test_suite


if __name__ == "__main__":
    import doctest
    doctest.testmod()