"""Parser for the statement of Poštovní spořitelna"""
from ofxstatement.parser import StatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import Statement, StatementLine
import re
import datetime

RecordParseRE = re.compile(r"\n{2,}", re.MULTILINE)


class PSTextFormatParser(StatementParser):
    # these keys mean in order: amount, date of transaction being recorded in
    # books, transaction type for statistical purposes, currency, name of
    # the other account, type of the transaction, memo, other account no.,
    # possible number of other sub-account, variable symbol (for identification
    # of the transaction), balance of the account after transaction
    #
    # note, that variable symbol is not guaranteed to be unique (it is quite
    # often number of the invoice or something which allows accountants to
    # identify the transaction on the account statement).
    _keys = set(('částka', 'datum zaúčtování', 'konstantní symbol', 'měna',
        'název protiúčtu', 'označení operace', 'poznámka', 'protiúčet',
        'specifický symbol', 'variabilní symbol', 'zůstatek',))

    statement = None
    currentLine = 0

    def __init__(self, fname):
        StatementParser.__init__(self)
        # bank_id=None, account_id=None, currency=None
        self.statement = Statement(currency="CZK")
        self.statement.start_date = datetime.date.fromtimestamp(0)
        self.statement.end_date = datetime.date.today()
        self.fin = fname

    def split_records(self):
        # uses self.fin
        return RecordParseRE.split(self.fin.read().strip())[1:]

    def parse_record(self, rec):
        MultilineRecRE = re.compile(r"\n\s+")
        SplitItemRE = re.compile(r":\s+")
        # join together multiline items
        rec = MultilineRecRE.sub(" ", rec)
        res_iter = (SplitItemRE.split(line) for line in rec.split("\n"))
        res_dict = dict((item[0].strip(), item[1].strip())
            for item in res_iter)
        res_key_set = set(res_dict.keys())
        # Insurance against unknown keys in the statement
        assert res_key_set <= self._keys, \
            "Unknown keys in the transaction: %s" % (res_key_set - self._keys)

        # no idea, how to make this unique and monotonically increasing
        trans_ID = res_dict['datum zaúčtování'] + res_dict['částka'] + \
            res_dict['variabilní symbol'] + res_dict['protiúčet']
        date_str = res_dict['datum zaúčtování'].split('.')
        stat_line = StatementLine(id=trans_ID,
            date=datetime.date(int(date_str[2]), int(date_str[1]),
                int(date_str[0])),
            memo="%s\nozn. operace: %s" % (res_dict['poznámka'],
                res_dict['označení operace']),
            amount=float(res_dict['částka']))
        stat_line.payee = res_dict['název protiúčtu']
        # According to OFX spec this could be "check (or other reference) no."
        # I don't see any requirement on monotonicity or uniqueness, but
        # I wonder how GnuCash understands that
        stat_line.check_no = res_dict['variabilní symbol']
        return stat_line


class PSPlugin(Plugin):
    name = "maxibps"

    def get_parser(self, fin):
        encoding = self.settings.get('charset', 'utf-8-sig')
        inf = open(fin, encoding=encoding)
        return PSTextFormatParser(inf)
