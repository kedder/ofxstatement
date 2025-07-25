import codecs
from typing import Optional, Union
from datetime import datetime, date
from decimal import Decimal

from xml.etree import ElementTree as etree
from xml.dom import minidom

from ofxstatement.statement import (
    Statement,
    StatementLine,
    InvestStatementLine,
    BankAccount,
    Currency,
)


class OfxWriter(object):
    def __init__(self, statement: Statement) -> None:
        self.statement = statement
        self.genTime = datetime.now()
        self.tb = etree.TreeBuilder()
        self.default_float_precision = 2
        self.invest_transactions_float_precision = 5

    def toxml(self, pretty: bool = False, encoding: str = "utf-8") -> str:
        et = self.buildDocument()
        root = et.getroot()
        assert root is not None
        xmlstring = etree.tostring(root, "unicode")
        if pretty:
            dom = minidom.parseString(xmlstring)
            xmlstring = dom.toprettyxml(indent="  ", newl="\r\n")
            xmlstring = xmlstring.replace('<?xml version="1.0" ?>', "").lstrip()

        codec = codecs.lookup(encoding)
        if codec.name == "utf-8":
            encoding_name = "UNICODE"
            charset_name = "NONE"
        elif codec.name.startswith("cp"):
            encoding_name = "USASCII"
            charset_name = codec.name[2:]
        else:
            # This is non-standard, because according to the OFX spec the
            # CHARSET should be the codepage number. We handle this gracefully,
            # since the only alternative is throwing an error here.
            encoding_name = "USASCII"
            charset_name = codec.name.upper()

        header = (
            "OFXHEADER:100\r\n"
            "DATA:OFXSGML\r\n"
            "VERSION:102\r\n"
            "SECURITY:NONE\r\n"
            f"ENCODING:{encoding_name}\r\n"
            f"CHARSET:{charset_name}\r\n"
            "COMPRESSION:NONE\r\n"
            "OLDFILEUID:NONE\r\n"
            "NEWFILEUID:NONE\r\n"
            "\r\n"
        )

        return header + xmlstring

    def buildDocument(self) -> etree.ElementTree:
        tb = self.tb
        tb.start("OFX", {})

        self.buildSignon()

        self.buildTransactionList()

        tb.end("OFX")
        return etree.ElementTree(tb.close())

    def buildSignon(self) -> None:
        tb = self.tb
        tb.start("SIGNONMSGSRSV1", {})
        tb.start("SONRS", {})
        tb.start("STATUS", {})
        self.buildText("CODE", "0")
        self.buildText("SEVERITY", "INFO")
        tb.end("STATUS")

        self.buildDateTime("DTSERVER", self.genTime)
        self.buildText("LANGUAGE", "ENG")

        tb.end("SONRS")
        tb.end("SIGNONMSGSRSV1")

    def buildTransactionList(self) -> None:
        if self.statement.lines:
            self.buildBankTransactionList()

        if self.statement.invest_lines:
            self.buildInvestTransactionList()

    def buildBankTransactionList(self) -> None:
        tb = self.tb
        tb.start("BANKMSGSRSV1", {})
        tb.start("STMTTRNRS", {})

        self.buildText("TRNUID", "0")
        tb.start("STATUS", {})
        self.buildText("CODE", "0")
        self.buildText("SEVERITY", "INFO")
        tb.end("STATUS")

        tb.start("STMTRS", {})
        self.buildText("CURDEF", self.statement.currency)
        tb.start("BANKACCTFROM", {})
        self.buildText("BANKID", self.statement.bank_id, False)
        self.buildText("ACCTID", self.statement.account_id, False)
        self.buildText("ACCTTYPE", self.statement.account_type)
        tb.end("BANKACCTFROM")

        tb.start("BANKTRANLIST", {})
        self.buildDate("DTSTART", self.statement.start_date, False)
        self.buildDate("DTEND", self.statement.end_date, False)

        for line in self.statement.lines:
            self.buildBankTransaction(line)

        tb.end("BANKTRANLIST")

        tb.start("LEDGERBAL", {})
        self.buildAmount("BALAMT", self.statement.end_balance, False)
        self.buildDateTime("DTASOF", self.statement.end_date, False)
        tb.end("LEDGERBAL")

        tb.end("STMTRS")
        tb.end("STMTTRNRS")
        tb.end("BANKMSGSRSV1")

    def buildBankTransaction(self, line: StatementLine) -> None:
        tb = self.tb
        tb.start("STMTTRN", {})

        self.buildText("TRNTYPE", line.trntype)
        self.buildDate("DTPOSTED", line.date)
        self.buildDate("DTUSER", line.date_user)
        self.buildAmount("TRNAMT", line.amount)
        self.buildText("FITID", line.id)
        self.buildText("CHECKNUM", line.check_no)
        self.buildText("REFNUM", line.refnum)
        self.buildText("NAME", line.payee)
        if line.bank_account_to:
            tb.start("BANKACCTTO", {})
            self.buildBankAccount(line.bank_account_to)
            tb.end("BANKACCTTO")
        self.buildText("MEMO", line.memo)
        if line.currency is not None:
            self.buildCurrency("CURRENCY", line.currency)
        if line.orig_currency is not None:
            self.buildCurrency("ORIG_CURRENCY", line.orig_currency)

        tb.end("STMTTRN")

    def buildCurrency(self, tag: str, currency: Currency) -> None:
        self.tb.start(tag, {})
        self.buildText("CURSYM", currency.symbol)
        self.buildAmount("CURRATE", currency.rate)
        self.tb.end(tag)

    def buildInvestTransactionList(self) -> None:
        tb = self.tb
        tb.start("SECLISTMSGSRSV1", {})
        tb.start("SECLIST", {})

        # get unqiue tickers
        for security_id in dict.fromkeys(
            map(lambda x: x.security_id, self.statement.invest_lines)
        ):
            if security_id is None:
                continue
            tb.start("STOCKINFO", {})
            tb.start("SECINFO", {})
            tb.start("SECID", {})
            self.buildText("UNIQUEID", security_id)
            self.buildText("UNIQUEIDTYPE", "TICKER")
            tb.end("SECID")
            self.buildText("SECNAME", security_id)
            self.buildText("TICKER", security_id)
            tb.end("SECINFO")
            tb.end("STOCKINFO")

        tb.end("SECLIST")
        tb.end("SECLISTMSGSRSV1")

        tb.start("INVSTMTMSGSRSV1", {})
        tb.start("INVSTMTTRNRS", {})

        self.buildText("TRNUID", "0")
        tb.start("STATUS", {})
        self.buildText("CODE", "0")
        self.buildText("SEVERITY", "INFO")
        tb.end("STATUS")

        tb.start("INVSTMTRS", {})
        self.buildDateTime("DTASOF", self.statement.end_date, False)
        self.buildText("CURDEF", self.statement.currency)
        tb.start("INVACCTFROM", {})
        self.buildText("BROKERID", self.statement.broker_id, False)
        self.buildText("ACCTID", self.statement.account_id, False)
        tb.end("INVACCTFROM")

        tb.start("INVTRANLIST", {})
        self.buildDate("DTSTART", self.statement.start_date, False)
        self.buildDate("DTEND", self.statement.end_date, False)

        for line in self.statement.invest_lines:
            self.buildInvestTransaction(line)

        tb.end("INVTRANLIST")
        tb.end("INVSTMTRS")
        tb.end("INVSTMTTRNRS")
        tb.end("INVSTMTMSGSRSV1")

    def buildInvestTransaction(self, line: InvestStatementLine) -> None:
        # invest transactions must always have trntype
        if line.trntype is None:
            return

        tb = self.tb

        if line.trntype == "INVBANKTRAN":
            tb.start(line.trntype, {})
            bankTran = StatementLine(line.id, line.date, line.memo, line.amount)
            bankTran.trntype = line.trntype_detailed
            self.buildBankTransaction(bankTran)
            self.buildText("SUBACCTFUND", "OTHER")
            tb.end(line.trntype)
            return

        tran_type_detailed_tag_name = None
        inner_tran_type_tag_name = None
        if line.trntype.startswith("BUY"):
            inner_tran_type_tag_name = "INVBUY"
            if line.trntype == "BUYMF" or line.trntype == "BUYSTOCK":
                tran_type_detailed_tag_name = "BUYTYPE"
        elif line.trntype.startswith("SELL"):
            inner_tran_type_tag_name = "INVSELL"
            if line.trntype == "SELLMF" or line.trntype == "SELLSTOCK":
                tran_type_detailed_tag_name = "SELLTYPE"
        elif line.trntype == "INCOME":
            tran_type_detailed_tag_name = "INCOMETYPE"
            inner_tran_type_tag_name = (
                None  # income transactions don't have an envelope element
            )
        else:
            # INVEXPENSE and TRANSFER transactions don't have details or an envelope
            tran_type_detailed_tag_name = None
            inner_tran_type_tag_name = None

        tb.start(line.trntype, {})
        if tran_type_detailed_tag_name:
            self.buildText(tran_type_detailed_tag_name, line.trntype_detailed, False)

        if inner_tran_type_tag_name:
            tb.start(inner_tran_type_tag_name, {})

        tb.start("INVTRAN", {})
        self.buildText("FITID", line.id)
        self.buildDate("DTTRADE", line.date, False)
        self.buildText("MEMO", line.memo)
        tb.end("INVTRAN")

        tb.start("SECID", {})
        self.buildText("UNIQUEID", line.security_id, False)
        self.buildText("UNIQUEIDTYPE", "TICKER")
        tb.end("SECID")

        self.buildText("SUBACCTSEC", "OTHER")
        if line.trntype != "TRANSFER":
            self.buildText("SUBACCTFUND", "OTHER")

        if line.fees:
            if line.trntype == "INCOME":
                self.buildAmount(
                    "WITHHOLDING",
                    line.fees,
                    False,
                    precision=self.invest_transactions_float_precision,
                )
            else:
                self.buildAmount(
                    "FEES",
                    line.fees,
                    False,
                    precision=self.invest_transactions_float_precision,
                )

        self.buildAmount(
            "UNITPRICE",
            line.unit_price,
            precision=self.invest_transactions_float_precision,
        )
        self.buildAmount(
            "UNITS",
            line.units,
            precision=self.invest_transactions_float_precision,
        )

        self.buildAmount("TOTAL", line.amount)

        if inner_tran_type_tag_name:
            tb.end(inner_tran_type_tag_name)
        tb.end(line.trntype)

    def buildBankAccount(self, account: BankAccount) -> None:
        self.buildText("BANKID", account.bank_id)
        self.buildText("BRANCHID", account.branch_id)
        self.buildText("ACCTID", account.acct_id)
        self.buildText("ACCTTYPE", account.acct_type)
        self.buildText("ACCTKEY", account.acct_key)

    def buildText(self, tag: str, text: Optional[str], skipEmpty: bool = True) -> None:
        if not text and skipEmpty:
            return
        self.tb.start(tag, {})
        self.tb.data(text or "")
        self.tb.end(tag)

    def buildDate(
        self, tag: str, dt: Optional[Union[date, datetime]], skipEmpty: bool = True
    ) -> None:
        if not dt and skipEmpty:
            return
        if dt is None:
            self.buildText(tag, "", skipEmpty)
        else:
            self.buildText(tag, dt.strftime("%Y%m%d"))

    def buildDateTime(
        self, tag: str, dt: Optional[datetime], skipEmpty: bool = True
    ) -> None:
        if not dt and skipEmpty:
            return
        if dt is None:
            self.buildText(tag, "", skipEmpty)
        else:
            self.buildText(tag, dt.strftime("%Y%m%d%H%M%S"))

    def buildAmount(
        self,
        tag: str,
        amount: Optional[Decimal],
        skipEmpty: bool = True,
        precision: Optional[int] = None,
    ) -> None:
        if amount is None and skipEmpty:
            return
        if amount is None:
            self.buildText(tag, "", skipEmpty)
        else:
            if precision is None:
                precision = self.default_float_precision

            self.buildText(tag, "{0:.{precision}f}".format(amount, precision=precision))
