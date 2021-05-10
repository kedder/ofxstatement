from unittest import TestCase
import xml.dom.minidom
from decimal import Decimal

from datetime import datetime

from ofxstatement.statement import Statement, InvestStatementLine
from ofxstatement import ofx

SIMPLE_OFX = """<?xml version="1.0" ?>
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
            <DTSERVER>20210501000000</DTSERVER>
            <LANGUAGE>ENG</LANGUAGE>
        </SONRS>
    </SIGNONMSGSRSV1>
    <SECLISTMSGSRSV1>
        <SECLIST>
            <STOCKINFO>
                <SECINFO>
                    <SECID>
                        <UNIQUEID>AAPL</UNIQUEID>
                        <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
                    </SECID>
                    <SECNAME>AAPL</SECNAME>
                    <TICKER>AAPL</TICKER>
                </SECINFO>
                <SECINFO>
                    <SECID>
                        <UNIQUEID>MSFT</UNIQUEID>
                        <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
                    </SECID>
                    <SECNAME>MSFT</SECNAME>
                    <TICKER>MSFT</TICKER>
                </SECINFO>
            </STOCKINFO>
        </SECLIST>
    </SECLISTMSGSRSV1>
    <INVSTMTMSGSRSV1>
        <INVSTMTTRNRS>
            <TRNUID>0</TRNUID>
            <STATUS>
                <CODE>0</CODE>
                <SEVERITY>INFO</SEVERITY>
            </STATUS>
            <INVSTMTRS>
                <DTASOF>20210501000000</DTASOF>
                <CURDEF>LTL</CURDEF>
                <INVACCTFROM>
                    <BROKERID>BROKERID</BROKERID>
                    <ACCTID>ACCID</ACCTID>
                </INVACCTFROM>
                <INVTRANLIST>
                    <DTSTART/>
                    <DTEND>20210501</DTEND>
                    <BUYSTOCK>
                        <BUYTYPE>BUY</BUYTYPE>
                        <INVBUY>
                            <INVTRAN>
                                <FITID>3</FITID>
                                <DTTRADE>20210101</DTTRADE>
                                <MEMO>Sample 3</MEMO>
                            </INVTRAN>
                            <SECID>
                                <UNIQUEID>AAPL</UNIQUEID>
                                <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
                            </SECID>
                            <SUBACCTSEC>OTHER</SUBACCTSEC>
                            <SUBACCTFUND>OTHER</SUBACCTFUND>
                            <FEES>1.24000</FEES>
                            <UNITPRICE>138.28000</UNITPRICE>
                            <UNITS>3.00</UNITS>
                            <TOTAL>-416.08000</TOTAL>
                        </INVBUY>
                    </BUYSTOCK>
                    <SELLSTOCK>
                        <SELLTYPE>SELL</SELLTYPE>
                        <INVSELL>
                            <INVTRAN>
                                <FITID>4</FITID>
                                <DTTRADE>20210101</DTTRADE>
                                <MEMO>Sample 4</MEMO>
                            </INVTRAN>
                            <SECID>
                                <UNIQUEID>MSFT</UNIQUEID>
                                <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
                            </SECID>
                            <SUBACCTSEC>OTHER</SUBACCTSEC>
                            <SUBACCTFUND>OTHER</SUBACCTFUND>
                            <FEES>0.28000</FEES>
                            <UNITPRICE>225.63000</UNITPRICE>
                            <UNITS>-5.00</UNITS>
                            <TOTAL>1127.87000</TOTAL>
                        </INVSELL>
                    </SELLSTOCK>
                    <INCOME>
                        <INCOMETYPE>DIV</INCOMETYPE>
                        <INVTRAN>
                            <FITID>5</FITID>
                            <DTTRADE>20210101</DTTRADE>
                            <MEMO>Sample 5</MEMO>
                        </INVTRAN>
                        <SECID>
                            <UNIQUEID>MSFT</UNIQUEID>
                            <UNIQUEIDTYPE>TICKER</UNIQUEIDTYPE>
                        </SECID>
                        <SUBACCTSEC>OTHER</SUBACCTSEC>
                        <SUBACCTFUND>OTHER</SUBACCTFUND>
                        <WITHHOLDING>0.50000</WITHHOLDING>
                        <TOTAL>0.79000</TOTAL>
                    </INCOME>
                </INVTRANLIST>
            </INVSTMTRS>
        </INVSTMTTRNRS>
    </INVSTMTMSGSRSV1>
</OFX>
"""


def prettyPrint(xmlstr):
    dom = xml.dom.minidom.parseString(xmlstr)
    return dom.toprettyxml().replace("\t", "    ").replace("<!-- ", "<!--")


class OfxInvestLinesWriterTest(TestCase):
    def test_ofxWriter(self) -> None:

        # Create sample statement:
        statement = Statement("BID", "ACCID", "LTL")
        statement.broker_id = "BROKERID"
        statement.end_date = datetime(2021, 5, 1)

        invest_line = InvestStatementLine(
            "3",
            datetime(2021, 1, 1),
            "Sample 3",
            "BUYSTOCK",
            "BUY",
            "AAPL",
            Decimal("-416.08"),
        )
        invest_line.units = Decimal("3")
        invest_line.unit_price = Decimal("138.28")
        invest_line.fees = Decimal("1.24")
        invest_line.assert_valid()
        statement.invest_lines.append(invest_line)

        invest_line = InvestStatementLine(
            "4",
            datetime(2021, 1, 1),
            "Sample 4",
            "SELLSTOCK",
            "SELL",
            "MSFT",
            Decimal("1127.87"),
        )
        invest_line.units = Decimal("-5")
        invest_line.unit_price = Decimal("225.63")
        invest_line.fees = Decimal("0.28")
        invest_line.assert_valid()
        statement.invest_lines.append(invest_line)

        invest_line = InvestStatementLine(
            "5",
            datetime(2021, 1, 1),
            "Sample 5",
            "INCOME",
            "DIV",
            "MSFT",
            Decimal("0.79"),
        )
        invest_line.fees = Decimal("0.5")
        invest_line.assert_valid()
        statement.invest_lines.append(invest_line)

        # Create writer:
        writer = ofx.OfxWriter(statement)

        # Set the generation time so it is always predictable
        writer.genTime = datetime(2021, 5, 1, 0, 0, 0)

        assert prettyPrint(writer.toxml()) == SIMPLE_OFX
