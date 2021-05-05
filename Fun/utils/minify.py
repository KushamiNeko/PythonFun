import re
from typing import IO


def _clean_js_comment(content: str) -> str:
    content = re.sub(r"""(?<![:"'])\s*\/\/\s*.+(?!["'])""", "", content)  # line comment
    content = re.sub(r"\s*\/\*\s*[\s\S]*?\s*\*\/", "", content)  # block comment
    return content


def _clean_html_comment(content: str) -> str:
    content = re.sub(r"\s*<!--\s*(?:[\s\S]*?)\s*-->", "", content)
    return content


def _clean_css_comment(content: str) -> str:
    return _clean_js_comment(content)


def _clean_leading_spaces(content: str) -> str:
    content = re.sub(r"^\s*", "", content, flags=re.MULTILINE)
    return content


def minifyWebBytes(content: bytes, encoding: str = "utf-8") -> bytes:
    c = content.decode(encoding=encoding)
    c = minifyWebString(c)
    return c.encode(encoding=encoding)


def minifyWebString(content: str) -> str:
    content = _clean_js_comment(content)
    # content = _clean_css_comment(content)
    content = _clean_html_comment(content)
    content = _clean_leading_spaces(content)

    return content


def minifyWebIO(src: IO) -> IO:
    src.seek(0)
    content = src.read()

    if type(content) == str:
        content = minifyWebString(content)
    elif type(content) == bytes:
        content = minifyWebBytes(content)

    src.seek(0)
    src.write(content)
    src.seek(0)

    return src
