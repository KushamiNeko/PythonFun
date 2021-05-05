from datetime import datetime

import pandas as pd
from Fun.data.barchart import Barchart
from Fun.data.source import FREQUENCY, Yahoo
from Fun.plotter.plotter import LinePlotter
from Fun.utils import colors
from matplotlib import axes


class EqualWeightedSource:
    def __init__(self, symbol: str) -> None:
        self._symbol = symbol

        self._ew_symbol = None
        src = Barchart()

        if self._symbol in ("es", "spx"):
            self._ew_symbol = "spxew"
        elif self._symbol in ("nq", "ndx"):
            self._ew_symbol = "ndxew"
            src = Yahoo()
        elif self._symbol in ("qr", "sml", "vle"):
            self._ew_symbol = "smlew"
            src = Barchart()

        self._src = src


class EqualWeightedRelativeStrength(EqualWeightedSource, LinePlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        symbol: str,
        height_ratio: float = 0.5,
        line_color: str = colors.PAPER_LIGHT_GREEN_A100,
        line_alpha: float = 0.5,
        line_width: float = 2.5,
    ) -> None:

        EqualWeightedSource.__init__(self, symbol=symbol)

        LinePlotter.__init__(
            self, line_color=line_color, line_alpha=line_alpha, line_width=line_width
        )

        self._quotes = quotes
        self._frequency = frequency
        self._symbol = symbol

        self._height_ratio = height_ratio

        if self._ew_symbol is not None and self._src is not None:
            self._ew_quotes = self._src.read(
                start=datetime.strptime("19000101", "%Y%m%d"),
                end=datetime.now(),
                symbol=self._ew_symbol,
                frequency=self._frequency,
            ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:
        if self._ew_symbol is None or self._ew_quotes is None:
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._height_ratio) + mn

        rs = (
            self._ew_quotes.loc[:, "close"]
            / self._quotes.loc[self._ew_quotes.index, "close"]
        )

        rs_max = rs.max()
        rs_min = rs.min()

        rs -= rs_min
        rs /= rs_max - rs_min

        rs *= top - mn
        rs += mn

        ax.plot(
            [i for i, d in enumerate(self._quotes.index) if d in self._ew_quotes.index],
            rs,
            color=self._line_color,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )
