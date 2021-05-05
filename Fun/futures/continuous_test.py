import unittest
from datetime import datetime

import numpy as np
from Fun.data.source import DAILY
from Fun.futures.continuous import ContinuousContract
from Fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    BARCHART,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    contract_list,
)
from Fun.futures.rolling import (
    DIFFERENCE,
    FirstOfMonth,
    LastNTradingDays,
    NO_ADJUSTMENT,
    RATIO,
    VolumeAndOpenInterest,
)
from Fun.utils.testing import parameterized


class TestContinuousContract(unittest.TestCase):
    @parameterized(
        [
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": LastNTradingDays(
                    offset=4, adjustment_method=NO_ADJUSTMENT
                ),
                "rolling_date": [
                    "20191217",
                    "20190917",
                    "20190618",
                    "20190312",
                    "20181218",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": LastNTradingDays(
                    offset=4, adjustment_method=DIFFERENCE
                ),
                "rolling_date": [
                    "20191217",
                    "20190917",
                    "20190618",
                    "20190312",
                    "20181218",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x + (3195.5 - 3192),
                    lambda x: x + (3195.5 - 3192) + (3008 - 3005.5),
                    lambda x: x
                    + (3195.5 - 3192)
                    + (3008 - 3005.5)
                    + (2926.25 - 2921.75),
                    lambda x: x
                    + (3195.5 - 3192)
                    + (3008 - 3005.5)
                    + (2926.25 - 2921.75)
                    + (2797.25 - 2792),
                    lambda x: x
                    + (3195.5 - 3192)
                    + (3008 - 3005.5)
                    + (2926.25 - 2921.75)
                    + (2797.25 - 2792)
                    + (2538 - 2535.75),
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": LastNTradingDays(offset=4, adjustment_method=RATIO),
                "rolling_date": [
                    "20191217",
                    "20190917",
                    "20190618",
                    "20190312",
                    "20181218",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x * (3195.5 / 3192),
                    lambda x: x * (3195.5 / 3192) * (3008 / 3005.5),
                    lambda x: x
                    * (3195.5 / 3192)
                    * (3008 / 3005.5)
                    * (2926.25 / 2921.75),
                    lambda x: x
                    * (3195.5 / 3192)
                    * (3008 / 3005.5)
                    * (2926.25 / 2921.75)
                    * (2797.25 / 2792),
                    lambda x: x
                    * (3195.5 / 3192)
                    * (3008 / 3005.5)
                    * (2926.25 / 2921.75)
                    * (2797.25 / 2792)
                    * (2538 / 2535.75),
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": FirstOfMonth(adjustment_method=NO_ADJUSTMENT),
                "rolling_date": [
                    "20191202",
                    "20190903",
                    "20190603",
                    "20190301",
                    "20181203",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": FirstOfMonth(adjustment_method=DIFFERENCE),
                "rolling_date": [
                    "20191202",
                    "20190903",
                    "20190603",
                    "20190301",
                    "20181203",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x + (3116 - 3114.25),
                    lambda x: x + (3116 - 3114.25) + (2906.5 - 2906),
                    lambda x: x
                    + (3116 - 3114.25)
                    + (2906.5 - 2906)
                    + (2752.5 - 2749.5),
                    lambda x: x
                    + (3116 - 3114.25)
                    + (2906.5 - 2906)
                    + (2752.5 - 2749.5)
                    + (2810.25 - 2805),
                    lambda x: x
                    + (3116 - 3114.25)
                    + (2906.5 - 2906)
                    + (2752.5 - 2749.5)
                    + (2810.25 - 2805)
                    + (2796 - 2790.75),
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": FirstOfMonth(adjustment_method=RATIO),
                "rolling_date": [
                    "20191202",
                    "20190903",
                    "20190603",
                    "20190301",
                    "20181203",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x * (3116 / 3114.25),
                    lambda x: x * (3116 / 3114.25) * (2906.5 / 2906),
                    lambda x: x
                    * (3116 / 3114.25)
                    * (2906.5 / 2906)
                    * (2752.5 / 2749.5),
                    lambda x: x
                    * (3116 / 3114.25)
                    * (2906.5 / 2906)
                    * (2752.5 / 2749.5)
                    * (2810.25 / 2805),
                    lambda x: x
                    * (3116 / 3114.25)
                    * (2906.5 / 2906)
                    * (2752.5 / 2749.5)
                    * (2810.25 / 2805)
                    * (2796 / 2790.75),
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": VolumeAndOpenInterest(
                    backup=FirstOfMonth(adjustment_method=NO_ADJUSTMENT),
                    adjustment_method=NO_ADJUSTMENT,
                ),
                "rolling_date": [
                    "20191216",
                    "20190916",
                    "20190617",
                    "20190311",
                    "20181217",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                    lambda x: x,
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": VolumeAndOpenInterest(
                    backup=FirstOfMonth(adjustment_method=DIFFERENCE),
                    adjustment_method=DIFFERENCE,
                ),
                "rolling_date": [
                    "20191216",
                    "20190916",
                    "20190617",
                    "20190311",
                    "20181217",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x + (3198.5 - 3194.25),
                    lambda x: x + (3198.5 - 3194.25) + (3001.5 - 2999),
                    lambda x: x
                    + (3198.5 - 3194.25)
                    + (3001.5 - 2999)
                    + (2896.25 - 2892),
                    lambda x: x
                    + (3198.5 - 3194.25)
                    + (3001.5 - 2999)
                    + (2896.25 - 2892)
                    + (2789 - 2784),
                    lambda x: x
                    + (3198.5 - 3194.25)
                    + (3001.5 - 2999)
                    + (2896.25 - 2892)
                    + (2789 - 2784)
                    + (2555.75 - 2552.5),
                ],
            },
            {
                "start": "20190101",
                "end": "20200101",
                "symbol": "es",
                "rolling_method": VolumeAndOpenInterest(
                    backup=FirstOfMonth(adjustment_method=RATIO),
                    adjustment_method=RATIO,
                ),
                "rolling_date": [
                    "20191216",
                    "20190916",
                    "20190617",
                    "20190311",
                    "20181217",
                ],
                "adjustment": [
                    lambda x: x,
                    lambda x: x * (3198.5 / 3194.25),
                    lambda x: x * (3198.5 / 3194.25) * (3001.5 / 2999),
                    lambda x: x
                    * (3198.5 / 3194.25)
                    * (3001.5 / 2999)
                    * (2896.25 / 2892),
                    lambda x: x
                    * (3198.5 / 3194.25)
                    * (3001.5 / 2999)
                    * (2896.25 / 2892)
                    * (2789 / 2784),
                    lambda x: x
                    * (3198.5 / 3194.25)
                    * (3001.5 / 2999)
                    * (2896.25 / 2892)
                    * (2789 / 2784)
                    * (2555.75 / 2552.5),
                ],
            },
        ]
    )
    def test_adjustment(
        self, start, end, symbol, rolling_method, rolling_date, adjustment
    ):
        c = ContinuousContract()

        s = datetime.strptime(start, "%Y%m%d")
        e = datetime.strptime(end, "%Y%m%d")

        df = c.read(
            start=s,
            end=e,
            symbol=symbol,
            frequency=DAILY,
            rolling_method=rolling_method,
        )

        self.assertEqual(df.index.nunique(), len(df))

        rolling_date = [datetime.strptime(r, "%Y%m%d") for r in rolling_date]

        months = FINANCIAL_CONTRACT_MONTHS
        if symbol == "cl":
            months = ALL_CONTRACT_MONTHS
        elif symbol == "gc":
            months = EVEN_CONTRACT_MONTHS

        cs = contract_list(s, e, symbol, months, BARCHART)

        self.assertEqual(len(rolling_date) + 1, len(adjustment))
        self.assertEqual(len(rolling_date) + 1, len(cs))

        adjust_columns = ["open", "high", "low", "close"]
        no_adjust_columns = ["volume", "open interest"]

        for i in range(len(rolling_date) + 1):
            cdf = cs[i].dataframe()
            if i == 0:
                df_selector = (df.index >= rolling_date[i]) & (df.index.isin(cdf.index))
                cdf_selector = (cdf.index >= rolling_date[i]) & (
                    cdf.index.isin(df.index)
                )

                self.assertTrue(np.isclose(df.iloc[-1], cdf.iloc[-1]).all())
            elif i > 0 and i < len(rolling_date):
                df_selector = (df.index >= rolling_date[i]) & (
                    df.index < rolling_date[i - 1]
                )
                cdf_selector = (cdf.index >= rolling_date[i]) & (
                    cdf.index < rolling_date[i - 1]
                )
            elif i >= len(rolling_date):
                df_selector = (df.index.isin(cdf.index)) & (
                    df.index < rolling_date[i - 1]
                )
                cdf_selector = (cdf.index.isin(df.index)) & (
                    cdf.index < rolling_date[i - 1]
                )

                self.assertTrue(
                    (
                        df.index[0]
                        < datetime(year=cs[i].year(), month=cs[i].month(), day=1)
                    )
                    and (
                        df.index[0]
                        >= datetime(
                            year=cs[i].previous_contract(read_data=False).year(),
                            month=cs[i].previous_contract(read_data=False).month(),
                            day=1,
                        )
                    )
                )

            self.assertTrue(
                np.isclose(
                    df.loc[df_selector, adjust_columns],
                    adjustment[i](cdf.loc[cdf_selector, adjust_columns]),
                    rtol=1e-12,
                    atol=0,
                ).all()
            )

            self.assertTrue(
                df.loc[df_selector, no_adjust_columns]
                .eq(cdf.loc[cdf_selector, no_adjust_columns])
                .all(axis=1)
                .all()
            )


if __name__ == "__main__":
    unittest.main()
