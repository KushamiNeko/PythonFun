from typing import List

import pandas as pd
from fun.plotter.plotter import Plotter
from fun.trading.order import TransactionOrder
from fun.utils import colors
from matplotlib import axes


class StopOrder(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        orders: List[TransactionOrder],
        line_length: int = 20,
        long_color: str = colors.PAPER_LIGHT_GREEN_A200,
        short_color: str = colors.PAPER_YELLOW_A200,
        line_alpha: float = 0.6,
        line_width: float = 3,
    ) -> None:
        self._quotes = quotes
        self._orders = orders
        self._line_length = line_length

        self._line_alpha = line_alpha
        self._line_width = line_width

        self._long_color = long_color
        self._short_color = short_color

    def plot(self, ax: axes.Axes) -> None:
        full = len(self._quotes) - 1

        for order in self._orders:
            color = self._long_color
            if order.operation() == "-":
                color = self._short_color

            ax.plot(
                [full - self._line_length, full],
                [order.price(), order.price()],
                color=color,
                alpha=self._line_alpha,
                linewidth=self._line_width,
            )
