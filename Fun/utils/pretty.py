import re
import readline  # noqa # pylint: disable=unused-import
from typing import Tuple


def color_caps(hex_rgb: str, message: str) -> None:
    color_print(hex_rgb, message.upper())


def color_print(hex_rgb: str, message: str) -> None:
    # print("\033[1;38;2;{};{};{}m{}\033[0m".format(rgb[0], rgb[1], rgb[2],
    # message))

    try:
        rgb = hex_to_rgb8(hex_rgb)
    except ValueError as err:
        print(err)
        rgb = (255, 255, 255)

    print(f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m{message}\033[0m")


def color_input(hex_rgb: str, message: str) -> str:
    color_print(hex_rgb, message)
    return input()


def hex_to_rgb8(hexstr: str) -> Tuple[int, int, int]:
    match = re.match(r"#?([0-9a-zA-Z]{6})", hexstr)

    if not match:
        raise ValueError(f"invalid hex str: {hexstr}")

    s = match.group(1)

    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)

    return (r, g, b)


def hex_to_rgb32(hexstr: str) -> Tuple[float, float, float]:
    r, g, b = hex_to_rgb8(hexstr)
    return (r / 255.0, g / 255.0, b / 255.0)
