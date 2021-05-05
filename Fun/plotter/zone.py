from datetime import datetime

import pandas as pd
from Fun.plotter.plotter import Plotter
from matplotlib import axes


class VolatilityZone(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        dtime: datetime,
        op: str,
        long_tolerant: float = 0.1,
        long_tolerant_extended_ratio: float = 1.5,
        short_tolerant: float = 0.05,
        short_tolerant_extended_ratio: float = 2.0,
        tolerant_color: str = "w",
        tolerant_extended_color: str = "w",
        tolerant_alpha: float = 0.3,
        tolerant_extended_alpha: float = 0.2,
    ) -> None:
        assert quotes is not None

        assert op in "long" "short"

        self._quotes = quotes
        self._datetime = dtime
        self._op = op

        self._long_tolerant = long_tolerant
        self._long_tolerant_extended_ratio = long_tolerant_extended_ratio

        self._short_tolerant = short_tolerant
        self._short_tolerant_extended_ratio = short_tolerant_extended_ratio

        self._tolerant_color = tolerant_color
        self._tolerant_extended_color = tolerant_extended_color
        self._tolerant_alpha = tolerant_alpha
        self._tolerant_extended_alpha = tolerant_extended_alpha

    def _long_zone(self, ax: axes.Axes, p_open: float, p_close: float) -> None:
        h = max(p_open, p_close)

        l = h * (1.0 - self._long_tolerant)
        le = h * (1.0 - (self._long_tolerant * self._long_tolerant_extended_ratio))

        ax.barh(
            h,
            width=len(self._quotes),
            height=l - h,
            align="edge",
            color=self._tolerant_color,
            alpha=self._tolerant_alpha,
        )

        ax.barh(
            l,
            width=len(self._quotes),
            height=le - l,
            align="edge",
            color=self._tolerant_extended_color,
            alpha=self._tolerant_extended_alpha,
        )

    def _short_zone(self, ax: axes.Axes, p_open: float, p_close: float) -> None:
        l = min(p_open, p_close)

        h = l * (1.0 + self._short_tolerant)
        he = l * (1.0 + (self._short_tolerant * self._short_tolerant_extended_ratio))

        ax.barh(
            l,
            width=len(self._quotes),
            height=h - l,
            align="edge",
            color=self._tolerant_color,
            alpha=self._tolerant_alpha,
        )

        ax.barh(
            h,
            width=len(self._quotes),
            height=he - h,
            align="edge",
            color=self._tolerant_extended_color,
            alpha=self._tolerant_extended_alpha,
        )

    def plot(self, ax: axes.Axes) -> None:
        try:
            p_open = self._quotes.loc[self._datetime, "open"]
            p_close = self._quotes.loc[self._datetime, "close"]

            if self._op == "long":
                self._long_zone(ax, p_open, p_close)
            elif self._op == "short":
                self._short_zone(ax, p_open, p_close)
            else:
                raise ValueError("invalid vix op")

        except KeyError:
            return
