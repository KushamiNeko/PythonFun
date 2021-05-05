from datetime import datetime

# from typing import Optional

# import numpy as np
import pandas as pd
from matplotlib import axes

# from matplotlib import font_manager as fm

from Fun.data.source import FREQUENCY, DataSource, InvestingCom, StockCharts, Yahoo
from Fun.plotter.plotter import LinePlotter
from Fun.utils import colors


class VolatilitySource:
    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

        self._vix_symbol = None
        src: DataSource = Yahoo()

        if self._symbol in ("es", "spx"):
            self._vix_symbol = "vix"
        elif self._symbol in ("nq", "ndx"):
            self._vix_symbol = "vxn"
        elif self._symbol in ("rut", "qr", "sml", "vle"):
            self._vix_symbol = "rvx"
            src = StockCharts()
        elif self._symbol in ("np", "nl", "no", "nikk"):
            self._vix_symbol = "jniv"
            src = InvestingCom()
        elif self._symbol in ("fx", "ezu"):
            self._vix_symbol = "vstx"
            src = InvestingCom()
        elif self._symbol == "hsi":
            self._vix_symbol = "vhsi"
            src = InvestingCom()
        elif self._symbol == "fxi":
            self._vix_symbol = "vxfxi"
            src = InvestingCom()
        elif self._symbol == "cl":
            self._vix_symbol = "ovx"
        elif self._symbol == "gc":
            self._vix_symbol = "gvz"
        elif self._symbol in ("zn", "zt", "zf", "zb", "ge"):
            self._vix_symbol = "vix"
        elif self._symbol == "tj":
            self._vix_symbol = "jniv"
        elif self._symbol == "gg":
            self._vix_symbol = "vstx"

        self._src = src


class VolatilitySummary(VolatilitySource, LinePlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        symbol: str,
        height_ratio: float = 1.0,
        line_color: str = colors.PAPER_LIGHT_BLUE_A100,
        line_alpha: float = 0.5,
        line_width: float = 2.5,
    ) -> None:

        VolatilitySource.__init__(self, symbol=symbol)

        LinePlotter.__init__(
            self, line_color=line_color, line_alpha=line_alpha, line_width=line_width
        )

        self._quotes = quotes
        self._frequency = frequency
        self._symbol = symbol

        self._height_ratio = height_ratio

        if self._vix_symbol is not None and self._src is not None:
            self._vix_quotes = self._src.read(
                start=datetime.strptime("19000101", "%Y%m%d"),
                end=datetime.now(),
                symbol=self._vix_symbol,
                frequency=self._frequency,
            ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:
        if self._vix_symbol is None or self._vix_quotes is None:
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._height_ratio) + mn

        vix_max = self._vix_quotes.loc[:, "close"].max()
        vix_min = self._vix_quotes.loc[:, "close"].min()

        self._vix_quotes -= vix_min
        self._vix_quotes /= vix_max - vix_min

        self._vix_quotes *= top - mn
        self._vix_quotes += mn

        ax.plot(
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._vix_quotes.index
            ],
            self._vix_quotes.loc[
                [d for d in self._vix_quotes.index if d in self._quotes.index], "close"
            ],
            color=self._line_color,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )


class VolatilityRealBodyContraction(VolatilitySource, LinePlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        symbol: str,
        height_ratio: float = 1.0,
        line_color: str = colors.PAPER_PINK_A100,
        line_alpha: float = 0.5,
        line_width: float = 2.5,
    ) -> None:

        VolatilitySource.__init__(self, symbol=symbol)

        LinePlotter.__init__(
            self, line_color=line_color, line_alpha=line_alpha, line_width=line_width
        )

        self._quotes = quotes
        self._frequency = frequency
        self._symbol = symbol

        self._height_ratio = height_ratio

        if self._vix_symbol is not None and self._src is not None:
            self._vix_quotes = self._src.read(
                start=datetime.strptime("19000101", "%Y%m%d"),
                end=datetime.now(),
                symbol=self._vix_symbol,
                frequency=self._frequency,
            ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:
        if self._vix_symbol is None or self._vix_quotes is None:
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._height_ratio) + mn
        # bottom = ((mx - mn) * self._height_ratio) + (mx + mn) / 2.0

        rb = self._vix_quotes.loc[:, "open"] - self._vix_quotes.loc[:, "close"]
        rb = rb.abs()

        rb_max = rb.max()
        rb_min = rb.min()

        # vix_max = self._vix_quotes.loc[:, "close"].max()
        # vix_min = self._vix_quotes.loc[:, "close"].min()

        rb -= rb_min
        rb /= rb_max - rb_min

        # rb *= mx - bottom
        # rb += bottom
        rb *= top - mn
        rb += mn

        mrb = rb.rolling(3).mean()

        ax.plot(
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._vix_quotes.index
            ],
            rb,
            color=self._line_color,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )

        ax.plot(
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._vix_quotes.index
            ],
            mrb,
            color=colors.PAPER_AMBER_A100,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )
