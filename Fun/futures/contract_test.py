import unittest
from datetime import datetime

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    BARCHART,
    Contract,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    QUANDL,
    contract_list,
)
from fun.utils.testing import parameterized


class TestContract(unittest.TestCase):
    @parameterized(
        [
            {
                "code": "esh2020",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "clh2010",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "nk225m",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_error": ValueError,
            },
            {
                "code": "nk225mm99",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_error": ValueError,
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_error": ValueError,
            },
            {
                "code": "esh20",
                "months": "hello",
                "fmt": BARCHART,
                "expect_error": AssertionError,
            },
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": "hello",
                "expect_error": AssertionError,
            },
        ]
    )
    def test_error(self, code, months, fmt, expect_error):
        with self.assertRaises(expect_error):
            Contract(
                code=code,
                months=months,
                fmt=fmt,
                read_data=False,
            )

    def test_read_data(self):
        c = Contract.front_month(
            symbol="es",
            months=FINANCIAL_CONTRACT_MONTHS,
            fmt=BARCHART,
            read_data=False,
        ).previous_contract(read_data=True)

        self.assertNotEqual(len(c.dataframe()), 0)
        self.assertFalse(c.dataframe().isna().any(axis=1).any())
        self.assertFalse((c.dataframe().index.hour != 0).any())

    @parameterized(
        [
            {
                "code": "esh20",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2020,
                "expect_month": 3,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esz19",
            },
            {
                "code": "esh01",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2001,
                "expect_month": 3,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esz00",
            },
            {
                "code": "esh00",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2000,
                "expect_month": 3,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esz99",
            },
            {
                "code": "esm03",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2003,
                "expect_month": 6,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esh03",
            },
            {
                "code": "esu99",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1999,
                "expect_month": 9,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esm99",
            },
            {
                "code": "esz98",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1998,
                "expect_month": 12,
                "expect_symbol": "es",
                "expect_previous_contract_code": "esu98",
            },
            {
                "code": "nk225mh2000",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 2000,
                "expect_month": 3,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mz1999",
            },
            {
                "code": "nk225mm1999",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 1999,
                "expect_month": 6,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mh1999",
            },
            {
                "code": "nk225mu2019",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 2019,
                "expect_month": 9,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mm2019",
            },
            {
                "code": "nk225mz2006",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 2006,
                "expect_month": 12,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mu2006",
            },
            {
                "code": "nk225mz1998",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": QUANDL,
                "expect_year": 1998,
                "expect_month": 12,
                "expect_symbol": "nk225m",
                "expect_previous_contract_code": "nk225mu1998",
            },
            {
                "code": "gcg01",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2001,
                "expect_month": 2,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcz00",
            },
            {
                "code": "gcg00",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2000,
                "expect_month": 2,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcz99",
            },
            {
                "code": "gcj14",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2014,
                "expect_month": 4,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcg14",
            },
            {
                "code": "gcm99",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1999,
                "expect_month": 6,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcj99",
            },
            {
                "code": "gcq04",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2004,
                "expect_month": 8,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcm04",
            },
            {
                "code": "gcv11",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2011,
                "expect_month": 10,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcq11",
            },
            {
                "code": "gcz13",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2013,
                "expect_month": 12,
                "expect_symbol": "gc",
                "expect_previous_contract_code": "gcv13",
            },
            {
                "code": "clf01",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2001,
                "expect_month": 1,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clz00",
            },
            {
                "code": "clf00",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2000,
                "expect_month": 1,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clz99",
            },
            {
                "code": "clg07",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2007,
                "expect_month": 2,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clf07",
            },
            {
                "code": "clh98",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1998,
                "expect_month": 3,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clg98",
            },
            {
                "code": "clj01",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2001,
                "expect_month": 4,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clh01",
            },
            {
                "code": "clk05",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2005,
                "expect_month": 5,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clj05",
            },
            {
                "code": "clm15",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2015,
                "expect_month": 6,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clk15",
            },
            {
                "code": "cln08",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2008,
                "expect_month": 7,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clm08",
            },
            {
                "code": "clq98",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 1998,
                "expect_month": 8,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "cln98",
            },
            {
                "code": "clu10",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2010,
                "expect_month": 9,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clq10",
            },
            {
                "code": "clv12",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2012,
                "expect_month": 10,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clu12",
            },
            {
                "code": "clx06",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2006,
                "expect_month": 11,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clv06",
            },
            {
                "code": "clz01",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_year": 2001,
                "expect_month": 12,
                "expect_symbol": "cl",
                "expect_previous_contract_code": "clx01",
            },
        ]
    )
    def test_contract(
        self,
        code,
        months,
        fmt,
        expect_year,
        expect_month,
        expect_symbol,
        expect_previous_contract_code,
    ):
        c = Contract(code=code, months=months, fmt=fmt, read_data=False)

        self.assertEqual(c.code(), code)
        self.assertEqual(c.year(), expect_year)
        self.assertEqual(c.month(), expect_month)
        self.assertEqual(c.symbol(), expect_symbol)

        self.assertEqual(
            c.previous_contract(read_data=False).code(), expect_previous_contract_code
        )

    @parameterized(
        [
            {
                "time": "20180105",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh18",
            },
            {
                "time": "20080201",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh08",
            },
            {
                "time": "19980321",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm98",
            },
            {
                "time": "20100411",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm10",
            },
            {
                "time": "20000529",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esm00",
            },
            {
                "time": "20180605",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu18",
            },
            {
                "time": "19990705",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu99",
            },
            {
                "time": "20190802",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esu19",
            },
            {
                "time": "20010923",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz01",
            },
            {
                "time": "20181005",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz18",
            },
            {
                "time": "20181119",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esz18",
            },
            {
                "time": "20181205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_code": "esh19",
            },
            {
                "time": "20181205",
                "symbol": "zn",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "znm19",
                "expect_code": "znh19",
            },
            {
                "time": "20191209",
                "symbol": "zn",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "znm20",
                "expect_code": "znh20",
            },
            {
                "time": "19980119",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clj98",
                "expect_code": "clh98",
            },
            {
                "time": "20000227",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clk00",
                "expect_code": "clj00",
            },
            {
                "time": "20010327",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clm01",
                "expect_code": "clk01",
            },
            {
                "time": "19990406",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "cln99",
                "expect_code": "clm99",
            },
            {
                "time": "20100530",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clq10",
                "expect_code": "cln10",
            },
            {
                "time": "20180605",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clu18",
                "expect_code": "clq18",
            },
            {
                "time": "20180731",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clv18",
                "expect_code": "clu18",
            },
            {
                "time": "20180805",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clx18",
                "expect_code": "clv18",
            },
            {
                "time": "20110917",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clz11",
                "expect_code": "clx11",
            },
            {
                "time": "19991023",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clf00",
                "expect_code": "clz99",
            },
            {
                "time": "20081106",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clg09",
                "expect_code": "clf09",
            },
            {
                "time": "20181206",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "clh19",
                "expect_code": "clg19",
            },
            {
                "time": "19980117",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcj98",
                "expect_code": "gcg98",
            },
            {
                "time": "20180215",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcm18",
                "expect_code": "gcj18",
            },
            {
                "time": "20180305",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcm18",
                "expect_code": "gcj18",
            },
            {
                "time": "20000425",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcq00",
                "expect_code": "gcm00",
            },
            {
                "time": "20010527",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcq01",
                "expect_code": "gcm01",
            },
            {
                "time": "20180605",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcv18",
                "expect_code": "gcq18",
            },
            {
                "time": "20030731",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcv03",
                "expect_code": "gcq03",
            },
            {
                "time": "20050831",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcz05",
                "expect_code": "gcv05",
            },
            {
                "time": "20130913",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcz13",
                "expect_code": "gcv13",
            },
            {
                "time": "19981025",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcg99",
                "expect_code": "gcz98",
            },
            {
                "time": "19991106",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcg00",
                "expect_code": "gcz99",
            },
            {
                "time": "20181206",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_code": "gcj19",
                "expect_code": "gcg19",
            },
        ]
    )
    def test_front_month(self, time, symbol, months, fmt, expect_code):
        c = Contract.front_month(
            symbol=symbol,
            months=months,
            fmt=fmt,
            time=datetime.strptime(time, "%Y%m%d"),
            read_data=False,
        )
        self.assertEqual(c.code(), expect_code)

    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh20,esz19,esu19,esm19,esh19,esz18",
                "error": None,
            },
            {
                "start": "19990201",
                "end": "20000201",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh00,esz99,esu99,esm99,esh99,esz98",
                "error": None,
            },
            {
                "start": "20070905",
                "end": "20081205",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh09,esz08,esu08,esm08,esh08,esz07,esu07,esm07",
                "error": None,
            },
            {
                "start": "19980101",
                "end": "19990101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh99,esz98,esu98,esm98,esh98",
                "error": None,
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "gcj19,gcg19,gcz18,gcv18,gcq18,gcm18,gcj18,gcg18,gcz17,gcv17",
                "expect_list": "gcg19,gcz18,gcv18,gcq18,gcm18,gcj18,gcg18,gcz17,gcv17",
                "error": None,
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "gcj98,gcg98,gcz97,gcv97,gcq97,gcm97,gcj97,gcg97",
                "expect_list": "gcg98,gcz97,gcv97,gcq97,gcm97,gcj97,gcg97",
                "error": None,
            },
            {
                "start": "20171231",
                "end": "20190101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "clj19,clh19,clg19,clf19,clz18,clx18,clv18,clu18,clq18,cln18,clm18,clk18,clj18,clh18,clg18,clf18,clz17,clx17",
                "expect_list": "clh19,clg19,clf19,clz18,clx18,clv18,clu18,clq18,cln18,clm18,clk18,clj18,clh18,clg18,clf18,clz17,clx17",
                "error": None,
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "clj98,clh98,clg98,clf98,clz97,clx97,clv97,clu97,clq97,cln97,clm97,clk97,clj97,clh97,clg97,clf97",
                "expect_list": "clh98,clg98,clf98,clz97,clx97,clv97,clu97,clq97,cln97,clm97,clk97,clj97,clh97,clg97,clf97",
                "error": None,
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "esh98",
                "error": None,
            },
            {
                "start": "19960101",
                "end": "19970101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "clj97,clh97,clg97,clf97",
                "expect_list": "clh97,clg97,clf97",
                "error": None,
            },
            {
                "start": "19960101",
                "end": "19970101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                # "expect_list": "gcj97,gcg97",
                "expect_list": "gcg97",
                "error": None,
            },
            {
                "start": "19960101",
                "end": "19970101",
                "symbol": "es",
                "months": FINANCIAL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "",
                "error": ValueError,
            },
            {
                "start": "19950101",
                "end": "19960101",
                "symbol": "cl",
                "months": ALL_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "",
                "error": ValueError,
            },
            {
                "start": "19950101",
                "end": "19960101",
                "symbol": "gc",
                "months": EVEN_CONTRACT_MONTHS,
                "fmt": BARCHART,
                "expect_list": "",
                "error": ValueError,
            },
        ]
    )
    def test_contract_list(self, start, end, symbol, months, fmt, expect_list, error):
        if error is None:
            cs = contract_list(
                start=datetime.strptime(start, "%Y%m%d"),
                end=datetime.strptime(end, "%Y%m%d"),
                symbol=symbol,
                months=months,
                fmt=fmt,
                read_data=True,
            )
            self.assertListEqual([c.code() for c in cs], expect_list.split(","))
        else:
            with self.assertRaises(error):
                contract_list(
                    start=datetime.strptime(start, "%Y%m%d"),
                    end=datetime.strptime(end, "%Y%m%d"),
                    symbol=symbol,
                    months=months,
                    fmt=fmt,
                    read_data=True,
                )


if __name__ == "__main__":
    unittest.main()