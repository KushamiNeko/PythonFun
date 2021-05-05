import math
import unittest
from datetime import datetime

from fun.trading.statistic import Statistic
from fun.trading.trade import FuturesTrade
from fun.trading.transaction import FuturesTransaction
from fun.utils.testing import parameterized


class TestStatistic(unittest.TestCase):
    def _assert_with_nan(self, a, b):
        if math.isnan(a) or math.isnan(b):
            self.assertTrue(math.isnan(a) and math.isnan(b))
        else:
            self.assertAlmostEqual(a, b)

    @parameterized(
        [
            {
                "trades": [
                    [
                        {
                            "datetime": "20190204",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190205",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                    ],
                    [
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                    ],
                ],
                "expect": {
                    "statistic_start": "20190104",
                    "statistic_end": "20190205",
                    "total_trades": 2,
                    "total_long_trades": 2,
                    "total_short_trades": 0,
                    "winners_holding_mean": 1,
                    "winners_holding_mean_long": 1,
                    "winners_holding_mean_short": math.nan,
                    "losers_holding_mean": 1,
                    "losers_holding_mean_long": 1,
                    "losers_holding_mean_short": math.nan,
                    "number_of_winners": 1,
                    "number_of_losers": 1,
                    "batting_average": 0.5,
                    "batting_average_long": 0.5,
                    "batting_average_short": math.nan,
                    "nominal_win_loss_ratio": 5,
                    "nominal_win_loss_ratio_long": 5,
                    "nominal_win_loss_ratio_short": math.nan,
                    "leveraged_win_loss_ratio": 5,
                    "leveraged_win_loss_ratio_long": 5,
                    "leveraged_win_loss_ratio_short": math.nan,
                    "nominal_adjusted_win_loss_ratio": 5,
                    "nominal_adjusted_win_loss_ratio_long": 5,
                    "nominal_adjusted_win_loss_ratio_short": math.nan,
                    "leveraged_adjusted_win_loss_ratio": 5,
                    "leveraged_adjusted_win_loss_ratio_long": 5,
                    "leveraged_adjusted_win_loss_ratio_short": math.nan,
                    "nominal_expected_value": 0.02,
                    "nominal_expected_value_long": 0.02,
                    "nominal_expected_value_short": math.nan,
                    "leveraged_expected_value": 0.02,
                    "leveraged_expected_value_long": 0.02,
                    "leveraged_expected_value_short": math.nan,
                    "winners_nominal_pl_mean": 0.05,
                    "winners_nominal_pl_mean_long": 0.05,
                    "winners_nominal_pl_mean_short": math.nan,
                    "winners_leveraged_pl_mean": 0.05,
                    "winners_leveraged_pl_mean_long": 0.05,
                    "winners_leveraged_pl_mean_short": math.nan,
                    "losers_nominal_pl_mean": -0.01,
                    "losers_nominal_pl_mean_long": -0.01,
                    "losers_nominal_pl_mean_short": math.nan,
                    "losers_leveraged_pl_mean": -0.01,
                    "losers_leveraged_pl_mean_long": -0.01,
                    "losers_leveraged_pl_mean_short": math.nan,
                },
            },
            {
                "trades": [
                    [
                        # 11 days
                        {
                            "datetime": "20190314",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20190325",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 105,
                        },
                    ],
                    [
                        # 32 days
                        {
                            "datetime": "20190824",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20190925",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 99,
                        },
                    ],
                ],
                "expect": {
                    "statistic_start": "20190314",
                    "statistic_end": "20190925",
                    "total_trades": 2,
                    "total_long_trades": 2,
                    "total_short_trades": 0,
                    "winners_holding_mean": 11,
                    "winners_holding_mean_long": 11,
                    "winners_holding_mean_short": math.nan,
                    "losers_holding_mean": 32,
                    "losers_holding_mean_long": 32,
                    "losers_holding_mean_short": math.nan,
                    "number_of_winners": 1,
                    "number_of_losers": 1,
                    "batting_average": 0.5,
                    "batting_average_long": 0.5,
                    "batting_average_short": math.nan,
                    "nominal_win_loss_ratio": 5,
                    "nominal_win_loss_ratio_long": 5,
                    "nominal_win_loss_ratio_short": math.nan,
                    "leveraged_win_loss_ratio": 5,
                    "leveraged_win_loss_ratio_long": 5,
                    "leveraged_win_loss_ratio_short": math.nan,
                    "nominal_adjusted_win_loss_ratio": 5,
                    "nominal_adjusted_win_loss_ratio_long": 5,
                    "nominal_adjusted_win_loss_ratio_short": math.nan,
                    "leveraged_adjusted_win_loss_ratio": 5,
                    "leveraged_adjusted_win_loss_ratio_long": 5,
                    "leveraged_adjusted_win_loss_ratio_short": math.nan,
                    "nominal_expected_value": 0.02,
                    "nominal_expected_value_long": 0.02,
                    "nominal_expected_value_short": math.nan,
                    "leveraged_expected_value": 0.04,
                    "leveraged_expected_value_long": 0.04,
                    "leveraged_expected_value_short": math.nan,
                    "winners_nominal_pl_mean": 0.05,
                    "winners_nominal_pl_mean_long": 0.05,
                    "winners_nominal_pl_mean_short": math.nan,
                    "winners_leveraged_pl_mean": 0.1,
                    "winners_leveraged_pl_mean_long": 0.1,
                    "winners_leveraged_pl_mean_short": math.nan,
                    "losers_nominal_pl_mean": -0.01,
                    "losers_nominal_pl_mean_long": -0.01,
                    "losers_nominal_pl_mean_short": math.nan,
                    "losers_leveraged_pl_mean": -0.02,
                    "losers_leveraged_pl_mean_long": -0.02,
                    "losers_leveraged_pl_mean_short": math.nan,
                },
            },
            {
                "trades": [
                    [
                        # 28 days
                        {
                            "datetime": "20190914",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190924",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 101.5,
                        },
                        {
                            "datetime": "20191002",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                        {
                            "datetime": "20191012",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 106.5,
                        },
                    ],
                    # 0.04950495
                    [
                        # 21 days
                        {
                            "datetime": "20191025",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        {
                            "datetime": "20191105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                        {
                            "datetime": "20191115",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                    ],
                    # -0.015
                ],
                "expect": {
                    "statistic_start": "20190914",
                    "statistic_end": "20191115",
                    "total_trades": 2,
                    "total_long_trades": 2,
                    "total_short_trades": 0,
                    "winners_holding_mean": 28,
                    "winners_holding_mean_long": 28,
                    "winners_holding_mean_short": math.nan,
                    "losers_holding_mean": 21,
                    "losers_holding_mean_long": 21,
                    "losers_holding_mean_short": math.nan,
                    "number_of_winners": 1,
                    "number_of_losers": 1,
                    "batting_average": 0.5,
                    "batting_average_long": 0.5,
                    "batting_average_short": math.nan,
                    "nominal_win_loss_ratio": 3.300330033,
                    "nominal_win_loss_ratio_long": 3.300330033,
                    "nominal_win_loss_ratio_short": math.nan,
                    "leveraged_win_loss_ratio": 4.950495,
                    "leveraged_win_loss_ratio_long": 4.950495,
                    "leveraged_win_loss_ratio_short": math.nan,
                    "nominal_adjusted_win_loss_ratio": 3.300330033,
                    "nominal_adjusted_win_loss_ratio_long": 3.300330033,
                    "nominal_adjusted_win_loss_ratio_short": math.nan,
                    "leveraged_adjusted_win_loss_ratio": 4.950495,
                    "leveraged_adjusted_win_loss_ratio_long": 4.950495,
                    "leveraged_adjusted_win_loss_ratio_short": math.nan,
                    "nominal_expected_value": 0.017252475,
                    "nominal_expected_value_long": 0.017252475,
                    "nominal_expected_value_short": math.nan,
                    "leveraged_expected_value": 0.059257425,
                    "leveraged_expected_value_long": 0.059257425,
                    "leveraged_expected_value_short": math.nan,
                    "winners_nominal_pl_mean": 0.04950495,
                    "winners_nominal_pl_mean_long": 0.04950495,
                    "winners_nominal_pl_mean_short": math.nan,
                    "winners_leveraged_pl_mean": 0.14851485,
                    "winners_leveraged_pl_mean_long": 0.14851485,
                    "winners_leveraged_pl_mean_short": math.nan,
                    "losers_nominal_pl_mean": -0.015,
                    "losers_nominal_pl_mean_long": -0.015,
                    "losers_nominal_pl_mean_short": math.nan,
                    "losers_leveraged_pl_mean": -0.03,
                    "losers_leveraged_pl_mean_long": -0.03,
                    "losers_leveraged_pl_mean_short": math.nan,
                },
            },
            {
                "trades": [
                    [
                        # 9 days
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190111",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 101.5,
                        },
                        # 101
                        {
                            "datetime": "20190109",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 105,
                        },
                        {
                            "datetime": "20190113",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 2,
                            "price": 106.5,
                        },
                        # 106
                    ],
                    # 0.04950495
                    [
                        # 3 days
                        {
                            "datetime": "20190106",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 102,
                        },
                        {
                            "datetime": "20190107",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 100
                        {
                            "datetime": "20190109",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 90,
                        },
                        # 90
                    ],
                    # 0.1
                    [
                        # 2 days
                        {
                            "datetime": "20190103",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 102,
                        },
                        {
                            "datetime": "20190104",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 100
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 94,
                        },
                        # 94
                    ],
                    # 0.06
                    [
                        # 4 days
                        {
                            "datetime": "20190102",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 2,
                            "price": 100,
                        },
                        # 100
                        {
                            "datetime": "20190105",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 99,
                        },
                        {
                            "datetime": "20190106",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 98,
                        },
                        # 98.5
                    ],
                    # -0.015
                    [
                        # 8 days
                        {
                            "datetime": "20190107",
                            "symbol": "es",
                            "operation": "-",
                            "leverage": 1,
                            "price": 100,
                        },
                        {
                            "datetime": "20190115",
                            "symbol": "es",
                            "operation": "+",
                            "leverage": 1,
                            "price": 101,
                        },
                    ],
                    # -0.01
                ],
                "expect": {
                    "statistic_start": "20190102",
                    "statistic_end": "20190115",
                    "total_trades": 5,
                    "total_long_trades": 2,
                    "total_short_trades": 3,
                    "winners_holding_mean": 4.666666667,
                    "winners_holding_mean_long": 9,
                    "winners_holding_mean_short": 2.5,
                    "losers_holding_mean": 6,
                    "losers_holding_mean_long": 4,
                    "losers_holding_mean_short": 8,
                    "number_of_winners": 3,
                    "number_of_losers": 2,
                    "batting_average": 0.6,
                    "batting_average_long": 0.5,
                    "batting_average_short": 0.666666667,
                    "nominal_win_loss_ratio": 5.586798667,
                    "nominal_win_loss_ratio_long": 3.30033,
                    "nominal_win_loss_ratio_short": 8,
                    "leveraged_win_loss_ratio": 7.808580833,
                    "leveraged_win_loss_ratio_long": 4.950495,
                    "leveraged_win_loss_ratio_short": 16,
                    "nominal_adjusted_win_loss_ratio": 8.380198,
                    "nominal_adjusted_win_loss_ratio_long": 3.30033,
                    "nominal_adjusted_win_loss_ratio_short": 16.000000008,
                    "leveraged_adjusted_win_loss_ratio": 11.71287125,
                    "leveraged_adjusted_win_loss_ratio_long": 4.950495,
                    "leveraged_adjusted_win_loss_ratio_short": 32.000000016,
                    "nominal_expected_value": 0.03690099,
                    "nominal_expected_value_long": 0.017252475,
                    "nominal_expected_value_short": 0.05,
                    "leveraged_expected_value": 0.08570297,
                    "leveraged_expected_value_long": 0.059257425,
                    "leveraged_expected_value_short": 0.103333333,
                    "winners_nominal_pl_mean": 0.069834983,
                    "winners_nominal_pl_mean_long": 0.04950495,
                    "winners_nominal_pl_mean_short": 0.08,
                    "winners_leveraged_pl_mean": 0.156171617,
                    "winners_leveraged_pl_mean_long": 0.14851485,
                    "winners_leveraged_pl_mean_short": 0.16,
                    "losers_nominal_pl_mean": -0.0125,
                    "losers_nominal_pl_mean_long": -0.015,
                    "losers_nominal_pl_mean_short": -0.01,
                    "losers_leveraged_pl_mean": -0.02,
                    "losers_leveraged_pl_mean_long": -0.03,
                    "losers_leveraged_pl_mean_short": -0.01,
                },
            },
        ]
    )
    def test_statistic(self, trades, expect):
        ts = [
            FuturesTrade([FuturesTransaction.from_entity(t) for t in trade])
            for trade in trades
        ]
        stat = Statistic(ts)

        self.assertEqual(
            stat.statistic_start(),
            datetime.strptime(expect["statistic_start"], "%Y%m%d"),
        )
        self.assertEqual(
            stat.statistic_end(), datetime.strptime(expect["statistic_end"], "%Y%m%d")
        )

        self.assertEqual(stat.total_trades(), expect["total_trades"])
        self.assertEqual(stat.total_long_trades(), expect["total_long_trades"])
        self.assertEqual(stat.total_short_trades(), expect["total_short_trades"])

        self.assertEqual(stat.number_of_winners(), expect["number_of_winners"])
        self.assertEqual(stat.number_of_losers(), expect["number_of_losers"])

        self._assert_with_nan(stat.batting_average(), expect["batting_average"])
        self._assert_with_nan(
            stat.batting_average_long(), expect["batting_average_long"]
        )
        self._assert_with_nan(
            stat.batting_average_short(), expect["batting_average_short"]
        )

        self._assert_with_nan(
            stat.winners_holding_mean(), expect["winners_holding_mean"]
        )
        self._assert_with_nan(
            stat.winners_holding_mean_long(), expect["winners_holding_mean_long"]
        )
        self._assert_with_nan(
            stat.winners_holding_mean_short(), expect["winners_holding_mean_short"]
        )

        self._assert_with_nan(stat.losers_holding_mean(), expect["losers_holding_mean"])
        self._assert_with_nan(
            stat.losers_holding_mean_long(), expect["losers_holding_mean_long"]
        )
        self._assert_with_nan(
            stat.losers_holding_mean_short(), expect["losers_holding_mean_short"]
        )

        self._assert_with_nan(
            stat.nominal_win_loss_ratio(), expect["nominal_win_loss_ratio"]
        )
        self._assert_with_nan(
            stat.nominal_win_loss_ratio_long(), expect["nominal_win_loss_ratio_long"]
        )
        self._assert_with_nan(
            stat.nominal_win_loss_ratio_short(), expect["nominal_win_loss_ratio_short"]
        )

        self._assert_with_nan(
            stat.leveraged_win_loss_ratio(), expect["leveraged_win_loss_ratio"]
        )
        self._assert_with_nan(
            stat.leveraged_win_loss_ratio_long(),
            expect["leveraged_win_loss_ratio_long"],
        )
        self._assert_with_nan(
            stat.leveraged_win_loss_ratio_short(),
            expect["leveraged_win_loss_ratio_short"],
        )

        self._assert_with_nan(
            stat.nominal_adjusted_win_loss_ratio(),
            expect["nominal_adjusted_win_loss_ratio"],
        )
        self._assert_with_nan(
            stat.nominal_adjusted_win_loss_ratio_long(),
            expect["nominal_adjusted_win_loss_ratio_long"],
        )
        self._assert_with_nan(
            stat.nominal_adjusted_win_loss_ratio_short(),
            expect["nominal_adjusted_win_loss_ratio_short"],
        )

        self._assert_with_nan(
            stat.leveraged_adjusted_win_loss_ratio(),
            expect["leveraged_adjusted_win_loss_ratio"],
        )
        self._assert_with_nan(
            stat.leveraged_adjusted_win_loss_ratio_long(),
            expect["leveraged_adjusted_win_loss_ratio_long"],
        )
        self._assert_with_nan(
            stat.leveraged_adjusted_win_loss_ratio_short(),
            expect["leveraged_adjusted_win_loss_ratio_short"],
        )

        self._assert_with_nan(
            stat.nominal_expected_value(), expect["nominal_expected_value"]
        )
        self._assert_with_nan(
            stat.nominal_expected_value_long(), expect["nominal_expected_value_long"]
        )
        self._assert_with_nan(
            stat.nominal_expected_value_short(), expect["nominal_expected_value_short"]
        )

        self._assert_with_nan(
            stat.leveraged_expected_value(), expect["leveraged_expected_value"]
        )
        self._assert_with_nan(
            stat.leveraged_expected_value_long(),
            expect["leveraged_expected_value_long"],
        )
        self._assert_with_nan(
            stat.leveraged_expected_value_short(),
            expect["leveraged_expected_value_short"],
        )

        self._assert_with_nan(
            stat.winners_nominal_pl_mean(),
            expect["winners_nominal_pl_mean"],
        )
        self._assert_with_nan(
            stat.winners_nominal_pl_mean_long(),
            expect["winners_nominal_pl_mean_long"],
        )
        self._assert_with_nan(
            stat.winners_nominal_pl_mean_short(),
            expect["winners_nominal_pl_mean_short"],
        )

        self._assert_with_nan(
            stat.winners_leveraged_pl_mean(),
            expect["winners_leveraged_pl_mean"],
        )
        self._assert_with_nan(
            stat.winners_leveraged_pl_mean_long(),
            expect["winners_leveraged_pl_mean_long"],
        )
        self._assert_with_nan(
            stat.winners_leveraged_pl_mean_short(),
            expect["winners_leveraged_pl_mean_short"],
        )

        self._assert_with_nan(
            stat.losers_nominal_pl_mean(),
            expect["losers_nominal_pl_mean"],
        )
        self._assert_with_nan(
            stat.losers_nominal_pl_mean_long(),
            expect["losers_nominal_pl_mean_long"],
        )
        self._assert_with_nan(
            stat.losers_nominal_pl_mean_short(),
            expect["losers_nominal_pl_mean_short"],
        )

        self._assert_with_nan(
            stat.losers_leveraged_pl_mean(),
            expect["losers_leveraged_pl_mean"],
        )
        self._assert_with_nan(
            stat.losers_leveraged_pl_mean_long(),
            expect["losers_leveraged_pl_mean_long"],
        )
        self._assert_with_nan(
            stat.losers_leveraged_pl_mean_short(),
            expect["losers_leveraged_pl_mean_short"],
        )


if __name__ == "__main__":
    unittest.main()
