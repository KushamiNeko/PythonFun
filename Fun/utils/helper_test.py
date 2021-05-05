import unittest

from fun.utils import helper
from fun.utils.testing import parameterized


class TestHelper(unittest.TestCase):
    def test_random_string(self):
        for _ in range(1000):
            rand_string_01 = helper.random_string()
            rand_string_02 = helper.random_string()

            self.assertNotEqual(rand_string_01, rand_string_02)

    @parameterized(
            [
                {"inputs": "price=100;op=l", "expected": {"price": "100", "op": "l"}},
                {"inputs": "price=100 ; op=l", "expected": {"price": "100", "op": "l"}},
                {
                    "inputs":   "price=100.5 ; note=hello world",
                    "expected": {"price": "100.5", "note": "hello world"},
                },
                {"inputs": "action=+ ; op=-", "expected": {"action": "+", "op": "-"}},
            ]
    )
    def test_key_value_pair_succeed(self, inputs, expected):
        pair = helper.key_value_pair(inputs)
        for k, v in expected.items():
            self.assertEqual(pair.get(k, None), v)

    @parameterized([{"inputs": ""}, {"inputs": "price=;o=l"}, {"inputs": "=100.5;o=l"}])
    def test_key_value_pair_empty(self, inputs):
        with self.assertRaises(ValueError):
            helper.key_value_pair(inputs)


if __name__ == "__main__":
    unittest.main()
