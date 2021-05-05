import pandas as pd
from Fun.data.source import (
    DAILY,
    FREQUENCY,
    INTRADAY_15MINUTES,
    INTRADAY_30MINUTES,
    INTRADAY_60MINUTES,
    MONTHLY,
    WEEKLY,
)
from Fun.plotter.plotter import Plotter
from matplotlib import axes


class BackgroundTimeRangeMark(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        from_start: bool = True,
        color: str = "w",
        alpha: float = 0.075,
        market: str = "US",
    ) -> None:
        self._quotes = quotes
        self._frequency = frequency
        self._from_start = from_start
        self._color = color
        self._alpha = alpha

        self._market = market

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency == DAILY or self._frequency == WEEKLY:
            self._monthly_range(ax)
        elif self._frequency == MONTHLY:
            self._yearly_range(ax)
        elif (
            self._frequency == INTRADAY_60MINUTES
            or self._frequency == INTRADAY_30MINUTES
            or self._frequency == INTRADAY_15MINUTES
        ):
            self._daily_range(ax)

    def _time_range(self, ax: axes.Axes, range_type: str) -> None:
        anchor_x = 0

        assert range_type in ("d", "m", "y")

        if range_type == "m":
            current = self._quotes.index[0].to_pydatetime().month
        elif range_type == "y":
            current = self._quotes.index[0].to_pydatetime().year
        # elif range_type == "d":
        # current = self._quotes.index[0].to_pydatetime().day
        # current = 16

        plotting = self._from_start

        mn, mx = ax.get_ylim()

        for i, x in enumerate(self._quotes.index):

            if range_type == "m":
                cursor = x.to_pydatetime().month
            elif range_type == "y":
                cursor = x.to_pydatetime().year
            elif range_type == "d":
                cursor = x.to_pydatetime().hour

                if x.to_pydatetime().minute != 0:
                    continue

            if range_type in ("m", "y"):
                if cursor != current:
                    plotting = not plotting
                    current = cursor

                    if plotting is False:
                        ax.bar(
                            anchor_x,
                            width=i - anchor_x,
                            bottom=mn,
                            height=mx - mn,
                            align="edge",
                            color=self._color,
                            alpha=self._alpha,
                        )
                    else:
                        anchor_x = i

            else:
                market_open = 17
                if self._market == "US":
                    market_open = 17
                elif self._market == "EU":
                    market_open = 19

                if cursor == market_open:
                    plotting = not plotting

                    if plotting is False:
                        ax.bar(
                            anchor_x,
                            width=i - 1 - anchor_x,
                            # width=i - anchor_x,
                            bottom=mn,
                            height=mx - mn,
                            align="edge",
                            color=self._color,
                            alpha=self._alpha,
                        )
                    else:
                        anchor_x = i

        if plotting is True:
            ax.bar(
                anchor_x,
                width=(len(self._quotes) - 1) - anchor_x,
                bottom=mn,
                height=mx - mn,
                align="edge",
                color=self._color,
                alpha=self._alpha,
            )

    def _daily_range(self, ax: axes.Axes) -> None:
        self._time_range(ax, "d")

    def _monthly_range(self, ax: axes.Axes) -> None:
        self._time_range(ax, "m")

    def _yearly_range(self, ax: axes.Axes) -> None:
        self._time_range(ax, "y")
