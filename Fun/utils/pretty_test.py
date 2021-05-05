import unittest

from fun.utils import pretty
from fun.utils.testing import parameterized


class TestHelper(unittest.TestCase):
    @parameterized(
        [
            {"rgb": "ffffff", "expect": (255, 255, 255)},
            {"rgb": "000000", "expect": (0, 0, 0)},
            {"rgb": "ff0000", "expect": (255, 0, 0)},
            {"rgb": "00ff00", "expect": (0, 255, 0)},
            {"rgb": "0000ff", "expect": (0, 0, 255)},
        ]
    )
    def test_hex_to_rgb(self, rgb, expect):
        rgb = pretty.hex_to_rgb8(rgb)
        self.assertTupleEqual(rgb, expect)


if __name__ == "__main__":
    unittest.main()
