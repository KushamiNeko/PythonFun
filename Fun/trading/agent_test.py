import os
import unittest
from datetime import datetime
from typing import cast

from fun.trading.agent import TradingAgent
from fun.utils import colors, pretty
from fun.utils.jsondb import JsonDB
from fun.utils.testing import parameterized


class TestTradingAgent(unittest.TestCase):
    def _check_root(self, root):
        if not os.path.exists(root):
            os.makedirs(root)
        else:
            for f in os.listdir(root):
                pretty.color_print(
                    colors.PAPER_RED_500, f"removing file {os.path.join(root, f)}"
                )
                os.remove(os.path.join(root, f))

        self.assertTrue(os.path.exists(root))

    def _clean_root(self, root):
        for f in os.listdir(root):
            pretty.color_print(
                colors.PAPER_RED_500, f"removing file {os.path.join(root, f)}"
            )
            os.remove(os.path.join(root, f))

            self.assertFalse(os.path.exists(os.path.join(root, f)))

        pretty.color_print(colors.PAPER_RED_500, f"removing dir {root}")
        os.rmdir(root)

        self.assertFalse(os.path.exists(root))

    @parameterized(
        [
            {
                "user_name": "nonexist",
                "new_user": False,
                "error": ValueError,
                "expected": None,
            },
            {
                "user_name": "new",
                "new_user": True,
                "error": None,
                "expected": [{"name": "new", "uid": ""}],
            },
        ]
    )
    def test_init(self, user_name, new_user, error, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "agent",
        )

        self._check_root(root)

        if os.path.exists(os.path.join(root, "admin_user.json")):
            jsonDB = JsonDB(root)
            jsonDB.drop("admin", "user")

        if error is not None:
            with self.assertRaises(ValueError):
                TradingAgent(
                    root, user_name=user_name, new_user=new_user,
                )
        else:
            self.assertTrue(expected is not None)

            TradingAgent(
                root, user_name=user_name, new_user=new_user,
            )

            db = "admin"
            col = "user"

            self.assertTrue(os.path.exists(os.path.join(root, f"{db}_{col}.json")))

            jsonDB = JsonDB(root)
            results = jsonDB.find(db, col, query=None)

            if len(expected) == 0:
                self.assertIsNone(results)

            else:
                assert results is not None

                self.assertEqual(len(results), len(expected))

                for i in range(len(results)):
                    r = results[i]
                    e = expected[i]

                    for k in r.keys():
                        er = e.get(k, None)
                        if er != "":
                            self.assertEqual(r[k], e.get(k, None))
                        else:
                            self.assertNotEqual(r[k], "")

        self._clean_root(root)

    @parameterized(
        [
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
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
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
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
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
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 1},
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
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
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
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
        ]
    )
    def test_read_trades(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_trades",
        )

        self._check_root(root)

        book = "read_trades"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 1)

        trades = agent.read_trades(book)

        self.assertEqual(len(trades), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
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
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
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
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
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
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 3},
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
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 6},
            },
        ]
    )
    def test_read_records(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_records",
        )

        self._check_root(root)

        book = "read_records"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 1)

        records = agent.read_records(book)

        self.assertEqual(len(records), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders_a": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
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
                ],
                "orders_b": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
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
                ],
                "expected": {"length": 4},
            },
            {
                "orders_a": [
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
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "orders_b": [
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
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 8},
            },
            {
                "orders_a": [
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "orders_b": [
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders_a": [
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "orders_b": [
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
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
        ]
    )
    def test_read_all_records(self, orders_a, orders_b, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "read_all_records",
        )

        self._check_root(root)

        book_a = "read_all_records_a"
        book_b = "read_all_records_b"

        agent = TradingAgent(root, new_user=True)

        for order in orders_a:
            agent.new_record(book_a, order, new_book=True)

        for order in orders_b:
            agent.new_record(book_b, order, new_book=True)

        books = agent.books()
        self.assertEqual(len(books), 2)

        records = agent.read_all_records()
        self.assertEqual(len(records), expected["length"])

        self._clean_root(root)

    @parameterized(
        [
            {"orders": [], "expected": {}},
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {
                    "length": 1,
                    "leverage": 1,
                    "nominal_average_opening": 10000,
                    "leverage_average_opening": 10000,
                },
            },
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
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {},
            },
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
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {
                    "length": 1,
                    "leverage": 1,
                    "nominal_average_opening": 10000,
                    "leverage_average_opening": 10000,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {
                    "length": 2,
                    "leverage": 1,
                    "nominal_average_opening": 10000,
                    "leverage_average_opening": 10000,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190408",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190508",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "13000",
                    },
                    {
                        "datetime": "20190510",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "8000",
                    },
                ],
                "expected": {
                    "length": 3,
                    "leverage": 2,
                    "nominal_average_opening": 11500,
                    "leverage_average_opening": 11000,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190308",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190309",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190408",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190508",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "13000",
                    },
                    {
                        "datetime": "20190510",
                        "symbol": "ty",
                        "operation": "+",
                        "leverage": "1",
                        "price": "8000",
                    },
                    {
                        "datetime": "20190512",
                        "symbol": "ty",
                        "operation": "-",
                        "leverage": "1",
                        "price": "13000",
                    },
                ],
                "expected": {
                    "length": 4,
                    "leverage": 3,
                    "nominal_average_opening": 12000,
                    "leverage_average_opening": 11500,
                },
            },
        ]
    )
    def test_open_positions(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "open_positions",
        )

        self._check_root(root)

        book = "open_positions"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        if len(orders) == 0:
            self.assertIsNone(books)
        else:
            self.assertEqual(len(books), 1)

            ps = agent.open_positions(book)
            if "length" in expected.keys():
                self.assertEqual(len(ps), expected["length"])
                self.assertEqual(
                    agent.open_positions_leverage(book), expected["leverage"],
                )
                self.assertEqual(
                    agent.open_positions_nominal_average_opening(book),
                    expected["nominal_average_opening"],
                )
                self.assertEqual(
                    agent.open_positions_leverage_average_opening(book),
                    expected["leverage_average_opening"],
                )
            else:
                self.assertIsNone(ps)
                self.assertIsNone(agent.open_positions_leverage(book))
                self.assertIsNone(agent.open_positions_nominal_average_opening(book))
                self.assertIsNone(agent.open_positions_leverage_average_opening(book))

        self._clean_root(root)

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
                ],
                "virtual_order": {"datetime": "20190315", "price": "10100",},
                "expected": {"nominal_pl": 0.01, "leveraged_pl": 0.01,},
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "10100",},
                "expected": {"nominal_pl": 0.01, "leveraged_pl": 0.02,},
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "2777",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "2777",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "10100",},
                "expected": {"nominal_pl": 0.007481297, "leveraged_pl": 0.014962594,},
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "9900",},
                "expected": {"nominal_pl": -0.01, "leveraged_pl": -0.01,},
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "9900",},
                "expected": {"nominal_pl": -0.01, "leveraged_pl": -0.02,},
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "2722",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "2722",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "9925",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "73.05",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "73.05",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "46.53",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "46.53",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "8020",},
                "expected": {"nominal_pl": 0.20, "leveraged_pl": 0.40,},
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "75.15",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "75.15",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "73.8",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190318", "price": "73.8",},
                "expected": {
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
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125",},
                "expected": {
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
                },
            },
        ]
    )
    def test_open_positions_virtual_pl(self, orders, virtual_order, expected):

        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "open_positions_virtual_pl",
        )
        self._check_root(root)

        book = "open_positions_virtual_pl"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        if len(orders) == 0:
            self.assertIsNone(books)
        else:
            self.assertEqual(len(books), 1)
            nominal, leveraged = agent.open_positions_virtual_pl(
                title=book,
                dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                virtual_close=float(virtual_order["price"]),
            )

            self.assertAlmostEqual(nominal, expected["nominal_pl"] * 100, 0)
            self.assertAlmostEqual(leveraged, expected["leveraged_pl"] * 100, 0)

        self._clean_root(root)

    @parameterized(
        [
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
                        "operation": "+",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190310",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190311",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190317",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {
                    "length": 2,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
                },
            },
            {
                "orders": [
                    {
                        "datetime": "20190310",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "datetime": "20190311",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190317",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {
                    "length": 2,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
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
                        "datetime": "20190320",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {
                    "length": 2,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
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
                        "datetime": "20190320",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190325",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {
                    "length": 2,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
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
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190320",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190325",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {
                    "length": 2,
                    "nominal_pl": -0.00997506234,
                    "leveraged_pl": -0.01995012469,
                },
            },
            {
                "orders": [],
                "virtual_order": {"datetime": "20190315", "price": "10125"},
                "expected": {"length": None},
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
                        "datetime": "20190315",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190320",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                    {
                        "datetime": "20190325",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10050",
                    },
                ],
                "virtual_order": {"datetime": "20190301", "price": "10125"},
                "expected": {"length": None},
            },
        ]
    )
    def test_open_positions_slice_virtual_pl(self, orders, virtual_order, expected):

        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "open_positions_virtual_pl",
        )
        self._check_root(root)

        book = "open_positions_virtual_pl"

        agent = TradingAgent(root, new_user=True)

        for order in orders:
            agent.new_record(book, order, new_book=True)

        books = agent.books()
        if len(orders) == 0:
            self.assertIsNone(books)
        else:
            self.assertEqual(len(books), 1)

            if expected["length"] is None:
                self.assertIsNone(
                    agent.open_positions(
                        title=book,
                        dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                    )
                )

                self.assertIsNone(
                    agent.open_positions_virtual_pl(
                        title=book,
                        dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                        virtual_close=float(virtual_order["price"]),
                    )
                )

                self.assertIsNone(
                    agent.open_positions_leverage(
                        title=book,
                        dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                    )
                )

                self.assertIsNone(
                    agent.open_positions_nominal_average_opening(
                        title=book,
                        dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                    )
                )

                self.assertIsNone(
                    agent.open_positions_leverage_average_opening(
                        title=book,
                        dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                    )
                )

            else:
                self.assertEqual(
                    len(
                        agent.open_positions(
                            title=book,
                            dtime=datetime.strptime(
                                virtual_order["datetime"], r"%Y%m%d"
                            ),
                        )
                    ),
                    expected["length"],
                )

                nominal, leveraged = agent.open_positions_virtual_pl(
                    title=book,
                    dtime=datetime.strptime(virtual_order["datetime"], r"%Y%m%d"),
                    virtual_close=float(virtual_order["price"]),
                )

                self.assertAlmostEqual(nominal, expected["nominal_pl"] * 100, 0)
                self.assertAlmostEqual(leveraged, expected["leveraged_pl"] * 100, 0)

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 4},
            },
            {
                "orders": [
                    {
                        "symbol": "es",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "es",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "es",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "es",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 2},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "2",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 3},
            },
            {
                "orders": [
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "hedging",
                        "operation": "-",
                        "leverage": "2",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                    {
                        "symbol": "ty",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "10000",
                    },
                ],
                "expected": {"length": 6},
            },
        ]
    )
    def test_new_order(self, orders, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "orders",
        )

        self._check_root(root)

        agent = TradingAgent(root, new_user=True)
        agent.delete_all_orders()

        for order in orders:
            agent.new_order(order)

        orders = agent.read_orders()

        self.assertEqual(len(orders), expected["length"])

        for i in range(len(orders)):
            agent.delete_order(0)
            orders = agent.read_orders()
            self.assertEqual(len(orders), expected["length"] - (i + 1))

        self._clean_root(root)

    @parameterized(
        [
            {
                "orders": [
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
                "events": [{"account": "trading", "dtime": "20191231", "price": 110}],
                "expected": [
                    {
                        "datetime": "20191231",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
            },
            {
                "orders": [
                    {
                        "symbol": "ym",
                        "account": "hedging",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
                "events": [{"account": "hedging", "dtime": "20191231", "price": 110}],
                "expected": [
                    {
                        "datetime": "20191231",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
            },
            {
                "orders": [
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "120",
                    },
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "symbol": "ym",
                        "account": "trading",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
                "events": [
                    {"account": "trading", "dtime": "20191229", "price": 110},
                    {"account": "trading", "dtime": "20191231", "price": 90},
                ],
                "expected": [
                    {
                        "datetime": "20191229",
                        "symbol": "ym",
                        "operation": "+",
                        "leverage": "1",
                        "price": "100",
                    },
                    {
                        "datetime": "20191231",
                        "symbol": "ym",
                        "operation": "-",
                        "leverage": "1",
                        "price": "100",
                    },
                ],
            },
        ]
    )
    def test_check_orders(self, orders, events, expected):
        root = os.path.join(
            cast(str, os.getenv("HOME")),
            "Documents",
            "database",
            "testing",
            "json",
            "check_orders",
        )

        self._check_root(root)

        book = "check_orders"

        agent = TradingAgent(root, new_user=True)
        agent.delete_all_orders()

        for order in orders:
            agent.new_order(order)

        self.assertEqual(len(orders), len(agent.read_orders()))

        self.assertEqual(len(events), len(expected))

        for ei, event in enumerate(events):
            agent.check_orders(
                book,
                datetime.strptime(event["dtime"], "%Y%m%d"),
                event["price"],
                new_book=True,
            )

            self.assertEqual(len(orders) - (ei + 1), len(agent.read_orders()))

            # ts = agent.read_records(book)
            ts = agent.read_records(f"{book}_{event['account']}")

            self.assertTrue(ts is not None)
            self.assertNotEqual(len(ts), 0)

            for i, t in enumerate(ts):
                te = t.to_entity()
                ee = expected[i]

                self.assertEqual(te["datetime"], ee["datetime"])
                self.assertEqual(te["symbol"], ee["symbol"])
                self.assertEqual(te["operation"], ee["operation"])
                self.assertEqual(float(te["leverage"]), float(ee["leverage"]))
                self.assertEqual(float(te["price"]), float(ee["price"]))

        self._clean_root(root)


if __name__ == "__main__":
    unittest.main()
