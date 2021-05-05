import time
import unittest
from datetime import datetime

from Fun.trading.transaction import FuturesTransaction
from Fun.utils.testing import parameterized


class TestFuturesTransaction(unittest.TestCase):
    @parameterized(
        [
            {
                "inputs": {
                    "datetime": datetime.strptime("20190313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
                "expected": {
                    "datetime": datetime.strptime("20190313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20190310", "%Y%m%d"),
                    "symbol": "ES",
                    "operation": "-",
                    "leverage": 10,
                    "price": 2722,
                },
                "expected": {
                    "datetime": datetime.strptime("20190310", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 10,
                    "price": 2722,
                },
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20210313", "%Y%m%d"),
                    "symbol": "Es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
                "expected": {
                    "datetime": datetime.strptime("20210313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20190113", "%Y%m%d"),
                    "symbol": "eS",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
                "expected": {
                    "datetime": datetime.strptime("20190113", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
                "expected": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                },
            },
        ]
    )
    def test_new_transaction_succeed(self, inputs, expected):
        t = FuturesTransaction(
            dtime=inputs["datetime"],
            symbol=inputs["symbol"],
            operation=inputs["operation"],
            leverage=inputs["leverage"],
            price=inputs["price"],
        )

        self.assertEqual(
            expected["datetime"].strftime("%Y%m%d"),
            t.datetime().strftime("%Y%m%d"),
        )
        self.assertEqual(expected["symbol"], t.symbol())
        self.assertEqual(expected["operation"], t.operation())
        self.assertEqual(expected["leverage"], t.leverage())
        self.assertEqual(expected["price"], t.price())

        self.assertNotEqual("", t.index())
        self.assertLess(0, t.time_stamp())

    @parameterized(
        [
            {
                "inputs": {
                    "datetime": -1,
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "[\\]",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "a123",
                    "operation": "-",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "hello",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "\\",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "123",
                    "leverage": 2,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 0,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": -1,
                    "price": 2722.75,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 0,
                }
            },
            {
                "inputs": {
                    "datetime": datetime.strptime("20160313", "%Y%m%d"),
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": -1,
                }
            },
        ]
    )
    def test_new_transaction_invalid(self, inputs):
        with self.assertRaises(ValueError):
            FuturesTransaction(
                dtime=inputs["datetime"],
                symbol=inputs["symbol"],
                operation=inputs["operation"],
                leverage=inputs["leverage"],
                price=inputs["price"],
            )

    @parameterized(
        [
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                    "index": "",
                    "time_stamp": "0",
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                    "index": "abc",
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                    "time_stamp": str(time.time()),
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
            {
                "inputs": {
                    "datetime": "20190308",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                    "index": "abc",
                    "time_stamp": str(time.time()),
                },
                "expected": {
                    "datetime": "20190308",
                    "symbol": "es",
                    "operation": "+",
                    "leverage": 1,
                    "price": 2722.75,
                },
            },
        ]
    )
    def test_futures_transaction_from_entity_succeed(self, inputs, expected):
        t = FuturesTransaction.from_entity(inputs)

        self.assertEqual(expected["datetime"], t.datetime().strftime("%Y%m%d"))
        self.assertEqual(expected["symbol"], t.symbol())
        self.assertEqual(expected["operation"], t.operation())
        self.assertEqual(expected["leverage"], t.leverage())
        self.assertEqual(expected["price"], t.price())

        if inputs.get("time_stamp", "") == "" or inputs.get("time_stamp", "") == "0":
            self.assertNotEqual(0, t.time_stamp())
            self.assertLess(0, t.time_stamp())
        else:
            self.assertEqual(inputs.get("time_stamp", ""), str(t.time_stamp()))

        if inputs.get("index", "") == "":
            self.assertNotEqual("", t.index())
        else:
            self.assertEqual(inputs.get("index", ""), t.index())

    def test_futures_transaction_from_entity_time_stamp_sort_succeed(self):
        tf = FuturesTransaction.from_entity(
            {
                "datetime": "20190308",
                "symbol": "es",
                "operation": "+",
                "leverage": "1",
                "price": "2722.75",
                "time_stamp": str(time.time()),
            }
        )

        ts = FuturesTransaction.from_entity(
            {
                "datetime": "20190308",
                "symbol": "es",
                "operation": "+",
                "leverage": "1",
                "price": "2722.75",
                "time_stamp": str(time.time()),
            }
        )

        self.assertNotEqual(0, tf.time_stamp())
        self.assertNotEqual(0, ts.time_stamp())
        self.assertNotEqual(tf.time_stamp(), ts.time_stamp())
        self.assertLess(tf.time_stamp(), ts.time_stamp())

    def test_futures_transaction_to_entity_succeed(self):
        t = FuturesTransaction(
            dtime=datetime.strptime("20191004", "%Y%m%d"),
            symbol="es",
            operation="+",
            leverage=1,
            price=2722.75,
        )

        nt = FuturesTransaction.from_entity(t.to_entity())

        self.assertEqual(nt.datetime(), t.datetime())
        self.assertEqual(nt.symbol(), t.symbol())
        self.assertEqual(nt.operation(), t.operation())
        self.assertEqual(nt.leverage(), t.leverage())
        self.assertEqual(nt.price(), t.price())
        self.assertEqual(nt.index(), t.index())
        self.assertEqual(nt.time_stamp(), t.time_stamp())

    @parameterized(
        [
            {
                "inputs": {
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "datetime": "20191004",
                    "operation": "+",
                    "leverage": "1",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "datetime": "20191004",
                    "symbol": "ES",
                    "leverage": "1",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "datetime": "20191004",
                    "symbol": "ES",
                    "operation": "+",
                    "price": "2722.75",
                }
            },
            {
                "inputs": {
                    "datetime": "20191004",
                    "symbol": "ES",
                    "operation": "+",
                    "leverage": "1",
                }
            },
        ]
    )
    def test_futures_transaction_from_entity_missing_key(self, inputs):
        with self.assertRaises(KeyError):
            FuturesTransaction.from_entity(inputs)


if __name__ == "__main__":
    unittest.main()
