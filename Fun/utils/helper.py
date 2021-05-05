import random
import re
import readline  # noqa # pylint: disable=unused-import
import string
from typing import Dict

from fun.utils import pretty


def key_value_input(hex_rgb: str, message: str) -> Dict[str, str]:
    user_input = pretty.color_input(hex_rgb, message).strip()
    if user_input == "":
        raise ValueError("empty input")

    pair = key_value_pair(user_input)
    return pair


def key_value_pair(inputs: str) -> Dict[str, str]:
    regex_pattern = r"([^;]*)=([^;]*)"
    pair = {}

    matches = re.finditer(regex_pattern, inputs, re.DOTALL)

    for match in matches:
        key = match.group(1).strip()
        value = match.group(2).strip()

        if key == "" or value == "":
            raise ValueError(f"invalid key value pair: {key}={value}")

        pair[key] = value

    if not pair:
        raise ValueError("empty key value pair")

    return pair


def random_string(
        length: int = 32,
        has_letter: bool = True,
        has_digits: bool = True,
        has_punctuation: bool = False,
) -> str:
    random.seed()

    src = ""
    if has_letter:
        src += string.ascii_letters
    if has_digits:
        src += string.digits
    if has_punctuation:
        src += string.punctuation

    rand_str = ""

    for _ in range(0, length):
        index = random.randrange(0, len(src))
        rand_str += src[index]

    return rand_str
