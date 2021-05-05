from __future__ import annotations

import os
from typing import Dict

from fun.utils import colors, pretty
from matplotlib import font_manager as fm

_FONTS = sorted(fm.findSystemFonts(fontpaths=None), key=lambda x: os.path.basename(x))

_FONT_FILE = "Roboto-Bold"

_FONT_SRC = None
for font in _FONTS:
    if _FONT_FILE in font:
        _FONT_SRC = font
        break

assert _FONT_SRC is not None
pretty.color_print(colors.GOOGLE_GREEN_300, f"font source: {_FONT_SRC}")


class Theme:
    def __init__(self) -> None:
        self._colors: Dict[str, str] = {}
        self._alpha: Dict[str, float] = {}

        self.dart_theme()

    def dart_theme(self) -> None:
        self._colors["up"] = colors.PAPER_TEAL_400
        self._colors["down"] = colors.PAPER_RED_400
        self._colors["unchanged"] = colors.PAPER_BLUE_GREY_200

        self._colors["records"] = "#ffffff"

        self._colors["bb0"] = colors.PAPER_PURPLE_400
        self._colors["bb1"] = colors.PAPER_INDIGO_400
        self._colors["bb2"] = colors.PAPER_RED_900
        self._colors["bb3"] = colors.PAPER_BLUE_700

        self._colors["sma0"] = colors.PAPER_YELLOW_300
        self._colors["sma1"] = colors.PAPER_BLUE_GREY_200
        # self._colors["sma2"] = colors.PAPER_LIGHT_GREEN_300
        self._colors["sma2"] = colors.PAPER_INDIGO_400
        self._colors["sma3"] = colors.PAPER_PURPLE_400
        # self._colors["sma4"] = colors.PAPER_ORANGE_400
        self._colors["sma4"] = colors.PAPER_RED_900
        self._colors["sma5"] = colors.PAPER_BLUE_700
        self._colors["sma6"] = colors.PAPER_BROWN_300
        # self._colors["sma6"] = colors.PAPER_LIGHT_GREEN_400

        self._colors["background"] = "#000000"
        self._colors["grid"] = colors.PAPER_GREY_400
        self._colors["ticks"] = "#ffffff"
        self._colors["text"] = "#ffffff"

        self._alpha["sma"] = 1.0
        self._alpha["bb"] = 0.6

        self._alpha["grid"] = 0.35

    def get_color(self, key: str) -> str:
        return self._colors[key]

    def get_alpha(self, key: str) -> float:
        return self._alpha[key]

    def get_font(self, font_size: float) -> fm.FontProperties:
        return fm.FontProperties(fname=_FONT_SRC, size=font_size)


class InteractiveTheme(Theme):
    def __init__(self):
        super().__init__()

    def dart_theme(self):
        super().dart_theme()

        self._colors["crosshair"] = colors.PAPER_GREY_100

        self._alpha["bb"] = 0.65
        self._alpha["crosshair"] = 0.5


class MagicalTheme(Theme):
    def __init__(self):
        super().__init__()

    def dart_theme(self) -> None:
        super().dart_theme()

        self._colors["up"] = colors.PAPER_GREY_300
        self._colors["down"] = colors.PAPER_GREY_900
        self._colors["unchanged"] = colors.PAPER_BLUE_GREY_200

        self._colors["records"] = "#ffffff"

        self._colors["sma3"] = colors.PAPER_PINK_200
        self._colors["sma5"] = colors.PAPER_RED_600
        self._colors["sma7"] = "#000000"
        self._colors["sma10"] = colors.PAPER_YELLOW_500

        self._colors["sma20"] = colors.PAPER_GREEN_500
        self._colors["sma30"] = colors.PAPER_GREY_500
        self._colors["sma60"] = colors.PAPER_BLUE_500
        self._colors["sma100"] = colors.PAPER_PURPLE_400
        self._colors["sma300"] = colors.PAPER_ORANGE_500

        self._colors["background"] = colors.PAPER_GREY_700
        self._colors["grid"] = colors.PAPER_GREY_900
        self._colors["ticks"] = "#ffffff"
        self._colors["text"] = "#ffffff"
