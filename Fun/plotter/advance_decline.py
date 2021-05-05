from datetime import datetime

import pandas as pd
from Fun.data.cumulative import BarchartCumulativeSum
from Fun.data.source import FREQUENCY
from Fun.plotter.plotter import LinePlotter
from Fun.utils import colors
from matplotlib import axes


class AdvanceDeclineSource:
    def __init__(self, symbol: str, volume_diff: bool = False) -> None:
        self._symbol = symbol

        self._ad_symbol = None

        src = BarchartCumulativeSum()

        if self._symbol in ("es", "spx", "spxew"):
            self._ad_symbol = "addn" if not volume_diff else "avdn"

        elif self._symbol in ("nq", "ndx", "ndxew"):
            self._ad_symbol = "addq" if not volume_diff else "avdq"

        self._src = src


class AdvanceDeclineLine(AdvanceDeclineSource, LinePlotter):
    def __init__(
            self,
            quotes: pd.DataFrame,
            frequency: FREQUENCY,
            symbol: str,
            volume_diff: bool = False,
            height_ratio: float = 0.5,
            line_color: str = colors.PAPER_AMBER_A100,
            line_alpha: float = 0.5,
            line_width: float = 2.5,
    ) -> None:

        AdvanceDeclineSource.__init__(self, symbol=symbol, volume_diff=volume_diff)

        LinePlotter.__init__(
                self, line_color=line_color, line_alpha=line_alpha, line_width=line_width
        )

        self._quotes = quotes
        self._frequency = frequency
        self._symbol = symbol

        self._height_ratio = height_ratio

        if self._ad_symbol is not None and self._src is not None:
            self._ad_quotes = self._src.read(
                    start=datetime.strptime("19000101", "%Y%m%d"),
                    end=datetime.now(),
                    symbol=self._ad_symbol,
                    frequency=self._frequency,
            ).loc[self._quotes.index[0]: self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:
        if self._ad_symbol is None or self._ad_quotes is None:
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._height_ratio) + mn

        rs_max = self._ad_quotes.loc[:, "close"].max()
        rs_min = self._ad_quotes.loc[:, "close"].min()

        self._ad_quotes.loc[:, "close"] -= rs_min
        self._ad_quotes.loc[:, "close"] /= rs_max - rs_min

        self._ad_quotes.loc[:, "close"] *= top - mn
        self._ad_quotes.loc[:, "close"] += mn

        ax.plot(
                [
                    i
                    for i, d in enumerate(self._quotes.index)
                    if d in self._ad_quotes.index
                ],
                self._ad_quotes.loc[[d for d in self._ad_quotes.index if d in self._quotes.index], "close"],
                color=self._line_color,
                alpha=self._line_alpha,
                linewidth=self._line_width,
        )
