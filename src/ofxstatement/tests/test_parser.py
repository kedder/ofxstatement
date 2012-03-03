import doctest

from ofxstatement.parser import CsvStatementParser

def doctest_CsvStatementParser():
    """Test generic CsvStatementParser

    Lets define some sample csv to parse and write it to file-like object

        >>> import io
        >>> csv = '''
        ... "2012-01-18","Microsoft","Windows XP",243.32,"1001"
        ... "2012-02-14","Google","Adwords",23.54,"1002"
        ... '''
        >>> f = io.StringIO(csv)

    Create and configure csv parser:
        >>> parser = CsvStatementParser(f)
        >>> parser.mappings = {0: "date",
        ...                    1: "payee",
        ...                    2: "memo",
        ...                    3: "amount",
        ...                    4: "id"}

    And parse csv:
        >>> statement = parser.parse()
        >>> len(statement.lines)
        2
        >>> statement.lines[0].amount
        243.32
        >>> statement.lines[1].payee
        'Google'




    """


def test_suite():
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
