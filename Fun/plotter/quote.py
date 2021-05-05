from datetime import timedelta
from typing import Optional

import numpy as np
import pandas as pd
from Fun.data.source import (
    FREQUENCY,
    INTRADAY_15MINUTES,
    INTRADAY_30MINUTES,
    INTRADAY_60MINUTES,
)
from Fun.plotter.plotter import TextPlotter
from matplotlib import axes
from matplotlib import font_manager as fm


class LastQuote(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        decimals: int = 4,
        x_offset: float = 3,
        font_color: str = "k",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes
        self._frequency = frequency

        self._decimals = decimals

        self._x_offset = x_offset

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) > 1:
            quote = self._quotes.iloc[-1]
            prev_quote = self._quotes.iloc[-2]

            info = [
                f"CST D:  {self._quotes.index[-1].strftime('%Y-%m-%d %a')}",
            ]

            if (
                self._frequency == INTRADAY_15MINUTES
                or self._frequency == INTRADAY_30MINUTES
                or self._frequency == INTRADAY_60MINUTES
            ):
                info.append(
                    f"CST T:  {self._quotes.index[-1].strftime('%H:%M')}",
                )

                offset = 6

                gmt = self._quotes.index[-1] + timedelta(hours=offset)
                info.append(f"GMT D:  {gmt.strftime('%Y-%m-%d %a')}")
                info.append(f"GMT T:  {gmt.strftime('%H:%M')}")

                offset = 15
                if self._quotes.index[-1].month in range(3, 11):
                    offset = 14

                jst = self._quotes.index[-1] + timedelta(hours=offset)

                info.append(f"JST D:  {jst.strftime('%Y-%m-%d %a')}")
                info.append(f"JST T:  {jst.strftime('%H:%M')}")

                info.append("")

            info.extend(
                [
                    f"Open:  {quote.loc['open']:,.{self._decimals}f}",
                    f"High: {quote.loc['high']:,.{self._decimals}f}",
                    f"Low: {quote.loc['low']:,.{self._decimals}f}",
                    f"Close:  {quote.loc['close']:,.{self._decimals}f}",
                    f"Volume:  {int(quote.get('volume', 0)):,}",
                    f"Interest:  {int(quote.get('open interest', 0)):,}",
                    f"Diff($):  {quote.loc['close'] - prev_quote.loc['close']:,.{self._decimals}f}",
                    f"Diff(%):  {((quote.loc['close'] - prev_quote.loc['close']) / prev_quote.loc['close']) * 100.0:,.{self._decimals}f}",
                ],
            )

            text = "\n".join(info)

            h = np.amax(self._quotes.loc[:, "high"])
            l = np.amin(self._quotes.loc[:, "low"])

            lh = np.amax(self._quotes.iloc[:30].loc[:, "high"])
            ll = np.amin(self._quotes.iloc[:30].loc[:, "low"])

            mn, mx = ax.get_ylim()

            y: float
            va: str
            if abs(l - ll) > abs(h - lh):
                # y = l
                y = mn
                va = "bottom"
            else:
                # y = h
                y = mx
                va = "top"

            ax.text(
                self._x_offset,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="left",
                va=va,
                zorder=9,
            )
