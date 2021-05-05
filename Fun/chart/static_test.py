import io
import unittest
from datetime import datetime

from Fun.chart.static import TradingChart
from Fun.data.source import DAILY, WEEKLY
from Fun.futures.continuous import ContinuousContract
from Fun.utils.testing import parameterized


class TestStaticTradingChart(unittest.TestCase):
    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "freqneucy": DAILY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19980101",
                "end": "19990101",
                "symbol": "es",
                "freqneucy": DAILY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19970101",
                "end": "19980101",
                "symbol": "es",
                "freqneucy": DAILY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19960101",
                "end": "19970101",
                "symbol": "es",
                "freqneucy": DAILY,
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "19950101",
                "end": "19960101",
                "symbol": "es",
                "freqneucy": DAILY,
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "20160101",
                "end": "20200101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19950101",
                "end": "19990101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19940101",
                "end": "19980101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "make_slice": True,
                "error": None,
            },
            {
                "start": "19930101",
                "end": "19970101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "make_slice": True,
                "error": ValueError,
            },
            {
                "start": "19920101",
                "end": "19960101",
                "symbol": "es",
                "freqneucy": WEEKLY,
                "make_slice": True,
                "error": ValueError,
            },
        ]
    )
    def test_plot(self, start, end, symbol, freqneucy, make_slice, error):
        c = ContinuousContract()

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        if error is not None:
            with self.assertRaises(error):
                c.read(s, e, symbol, freqneucy)

        else:
            df = c.read(s, e, symbol, freqneucy)

            if make_slice:
                df = df.loc[(df.index >= s) & (df.index <= e)]

            original = df.copy()

            buf = io.BytesIO()

            chart = TradingChart(
                quotes=df.loc[(df.index >= s) & (df.index <= e)],
            )

            chart.render(buf)

            self.assertTrue(original.eq(df).all(axis=1).all())


if __name__ == "__main__":
    unittest.main()
