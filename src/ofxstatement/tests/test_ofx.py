import sys
import doctest
import xml.dom.minidom

from datetime import datetime

from ofxstatement.statement import Statement, StatementLine, BankAccount
from ofxstatement import ofx

def prettyPrint(xmlstr):
    dom = xml.dom.minidom.parseString(xmlstr)
    print(dom.toprettyxml().replace("\t", "    "))

def doctest_OfxWriter():
    """Test OfxWriter functionality.

    Create sample statement:

        >>> statement = Statement("BID", "ACCID", "LTL")
        >>> statement.lines.append(StatementLine(
        ...     "1", datetime(2012, 2, 12), "Sample 1", 15.4))
        >>> line = StatementLine("2", datetime(2012, 2, 12), "Sample 2", 25.0)
        >>> line.payee = ''
        >>> line.bank_account_to = BankAccount("SNORAS", "LT1232")
        >>> line.bank_account_to.branch_id = "VNO"
        >>> statement.lines.append(line)

    Create writer:
        >>> writer = ofx.OfxWriter(statement)

    Set the generation time so it is always predictable
        >>> writer.genTime = datetime(2012, 3, 3, 0, 0, 0)

    Produce OFX output:
        >>> prettyPrint(writer.toxml())
        <?xml version="1.0" ?>
        <!--
        OFXHEADER:100
        DATA:OFXSGML
        VERSION:102
        SECURITY:NONE
        ENCODING:UTF-8
        CHARSET:NONE
        COMPRESSION:NONE
        OLDFILEUID:NONE
        NEWFILEUID:NONE
        -->
        <OFX>
            <SIGNONMSGSRSV1>
                <SONRS>
                    <STATUS>
                        <CODE>0</CODE>
                        <SEVERITY>INFO</SEVERITY>
                    </STATUS>
                    <DTSERVER>20120303000000</DTSERVER>
                    <LANGUAGE>ENG</LANGUAGE>
                </SONRS>
            </SIGNONMSGSRSV1>
            <BANKMSGSRSV1>
                <STMTTRNRS>
                    <TRNUID>0</TRNUID>
                    <STATUS>
                        <CODE>0</CODE>
                        <SEVERITY>INFO</SEVERITY>
                    </STATUS>
                    <STMTRS>
                        <CURDEF>LTL</CURDEF>
                        <BANKACCTFROM>
                            <BANKID>BID</BANKID>
                            <ACCTID>ACCID</ACCTID>
                            <ACCTTYPE>CHECKING</ACCTTYPE>
                        </BANKACCTFROM>
                        <BANKTRANLIST>
                            <DTSTART/>
                            <DTEND/>
                            <STMTTRN>
                                <TRNTYPE>CHECK</TRNTYPE>
                                <DTPOSTED>20120212</DTPOSTED>
                                <TRNAMT>15.40</TRNAMT>
                                <FITID>1</FITID>
                                <MEMO>Sample 1</MEMO>
                            </STMTTRN>
                            <STMTTRN>
                                <TRNTYPE>CHECK</TRNTYPE>
                                <DTPOSTED>20120212</DTPOSTED>
                                <TRNAMT>25.00</TRNAMT>
                                <FITID>2</FITID>
                                <MEMO>Sample 2</MEMO>
                                <BANKACCTTO>
                                    <BANKID>SNORAS</BANKID>
                                    <BRANCHID>VNO</BRANCHID>
                                    <ACCTID>LT1232</ACCTID>
                                    <ACCTTYPE>CHECKING</ACCTTYPE>
                                </BANKACCTTO>
                             </STMTTRN>
                        </BANKTRANLIST>
                        <LEDGERBAL>
                            <BALAMT/>
                            <DTASOF/>
                        </LEDGERBAL>
                    </STMTRS>
                </STMTTRNRS>
            </BANKMSGSRSV1>
        </OFX>
        <BLANKLINE>
    """



def test_suite(*args):
    return doctest.DocTestSuite(optionflags=(doctest.NORMALIZE_WHITESPACE|
                                             doctest.ELLIPSIS|
                                             doctest.REPORT_ONLY_FIRST_FAILURE|
                                             doctest.REPORT_NDIFF
                                             ))
load_tests = test_suite
