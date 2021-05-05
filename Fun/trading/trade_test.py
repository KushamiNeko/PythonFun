import unittest

from fun.trading.trade import FuturesTrade
from fun.trading.transaction import FuturesTransaction
from fun.utils.testing import parameterized


class TestFuturesTrade(unittest.TestCase):
    @parameterized(
        [
            {"orders": []},
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "short",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "3",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ]
            },
        ]
    )
    def test_init_invalid(self, orders):
        with self.assertRaises(ValueError):
            orders = [FuturesTransaction.from_entity(order) for order in orders]

            FuturesTrade(orders)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10100",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 1,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10000,
                    "average_close": 10100,
                    "nominal_pl": 0.01,
                    "leveraged_pl": 0.01,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10100",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10000,
                    "average_close": 10100,
                    "nominal_pl": 0.01,
                    "leveraged_pl": 0.02,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2722.75",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2742",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2776.25",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2777",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": -2732.375,
                    "average_close": 2776.625,
                    "nominal_pl": 0.01619470241,
                    "leveraged_pl": 0.03238940482,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2722.75",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "2742",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2776.25",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "2777",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 3,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": -2735.583333333,
                    "average_close": 2776.75,
                    "nominal_pl": 0.01504858805,
                    "leveraged_pl": 0.04514576415,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10100",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10025,
                    "average_close": 10100,
                    "nominal_pl": 0.007481297,
                    "leveraged_pl": 0.014962594,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "9900",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 1,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10000,
                    "average_close": 9900,
                    "nominal_pl": -0.01,
                    "leveraged_pl": -0.01,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "9900",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10000,
                    "average_close": 9900,
                    "nominal_pl": -0.01,
                    "leveraged_pl": -0.02,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2722.75",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2742",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2725.5",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2722",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": -2732.375,
                    "average_close": 2723.75,
                    "nominal_pl": -0.00315659454,
                    "leveraged_pl": -0.00631319,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "1",
                        "price": "2722.75",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "es",
                        "operation": "+",
                        "leverage": "2",
                        "price": "2742",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "1",
                        "price": "2725.5",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "es",
                        "operation": "-",
                        "leverage": "2",
                        "price": "2722",
                    },
                ],
                "expected": {
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 3,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": -2735.583333333,
                    "average_close": 2723.166666667,
                    "nominal_pl": -0.0045389466,
                    "leveraged_pl": -0.0136168398,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "2",
                        "price": "9925",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "+",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": -10025,
                    "average_close": 9925,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012468,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "73.05",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 1,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 74.4,
                    "average_close": -73.05,
                    "nominal_pl": 0.01814516129,
                    "leveraged_pl": 0.01814516129,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "2",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "2",
                        "price": "73.05",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 74.4,
                    "average_close": -73.05,
                    "nominal_pl": 0.01814516129,
                    "leveraged_pl": 0.03629032258,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "73.05",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "53.81",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "46.53",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": 73.725,
                    "average_close": -50.17,
                    "nominal_pl": 0.31949813496,
                    "leveraged_pl": 0.63899626992,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "2",
                        "price": "73.05",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "53.81",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "2",
                        "price": "46.53",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 3,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": 73.5,
                    "average_close": -48.956666667,
                    "nominal_pl": 0.33392290249,
                    "leveraged_pl": 1.00176870748,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "2",
                        "price": "8020",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 10025,
                    "average_close": -8020,
                    "nominal_pl": 0.20,
                    "leveraged_pl": 0.40,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "75.15",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 1,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 74.4,
                    "average_close": -75.15,
                    "nominal_pl": -0.01008064516,
                    "leveraged_pl": -0.01008064516,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "2",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "2",
                        "price": "75.15",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 74.4,
                    "average_close": -75.15,
                    "nominal_pl": -0.01008064516,
                    "leveraged_pl": -0.02016129,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "73.05",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "75.1",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "73.8",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": 73.725,
                    "average_close": -74.45,
                    "nominal_pl": -0.00983384198,
                    "leveraged_pl": -0.01966768396,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "1",
                        "price": "74.4",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "cl",
                        "operation": "-",
                        "leverage": "2",
                        "price": "73.05",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "1",
                        "price": "75.1",
                    },
                    {
                        "datetime": "20190318",
                        "symbol": "cl",
                        "operation": "+",
                        "leverage": "2",
                        "price": "73.8",
                    },
                ],
                "expected": {
                    "symbol": "cl",
                    "operation": "-",
                    "leverage": 3,
                    "open_time": "20190308",
                    "close_time": "20190318",
                    "average_open": 73.5,
                    "average_close": -74.233333333,
                    "nominal_pl": -0.00997732426,
                    "leveraged_pl": -0.02993197279,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10125",
                    },
                ],
                "expected": {
                    "symbol": "ym",
                    "operation": "-",
                    "leverage": 2,
                    "open_time": "20190308",
                    "close_time": "20190315",
                    "average_open": 10025,
                    "average_close": -10125,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
                },
            },
        ]
    )
    def test_trade(self, orders, expected):
        orders = [FuturesTransaction.from_entity(order) for order in orders]

        trade = FuturesTrade(orders)

        self.assertEqual(trade.symbol(), expected["symbol"])
        self.assertEqual(trade.operation(), expected["operation"])
        self.assertEqual(trade.leverage(), expected["leverage"])
        self.assertEqual(trade.open_time().strftime("%Y%m%d"), expected["open_time"])
        self.assertEqual(trade.close_time().strftime("%Y%m%d"), expected["close_time"])

        self.assertEqual(trade.open_time_stamp(), orders[0].time_stamp())
        self.assertEqual(trade.close_time_stamp(), orders[-1].time_stamp())

        self.assertAlmostEqual(trade.average_open(), expected["average_open"])
        self.assertAlmostEqual(trade.average_close(), expected["average_close"])

        self.assertAlmostEqual(trade.nominal_pl(), expected["nominal_pl"])
        self.assertAlmostEqual(trade.leveraged_pl(), expected["leveraged_pl"], places=6)


if __name__ == "__main__":
    unittest.main()
