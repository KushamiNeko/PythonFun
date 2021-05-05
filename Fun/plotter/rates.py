from datetime import datetime

# import numpy as np
import pandas as pd
from Fun.data.barchart import Barchart
from Fun.data.source import DAILY, FREQUENCY, MONTHLY, WEEKLY
from Fun.plotter.plotter import Plotter
from Fun.utils import colors
from matplotlib import axes


class InterestRatesSummary(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        height_ratio: float = 1.0,
        line_color_short: str = colors.PAPER_YELLOW_300,
        # line_color_medium: str = colors.PAPER_BLUE_GREY_200,
        line_color_long: str = colors.PAPER_BLUE_GREY_200,
        # line_color_long: str = colors.PAPER_INDIGO_400,
        line_alpha: float = 0.5,
        line_width: float = 2.5,
    ) -> None:

        self._quotes = quotes
        self._frequency = frequency

        self._height_ratio = height_ratio

        self._line_color_short = line_color_short
        # self._line_color_medium = line_color_medium
        self._line_color_long = line_color_long

        self._line_alpha = line_alpha
        self._line_width = line_width

        src = Barchart()

        self._short_rates = src.read(
            start=datetime.strptime("19000101", "%Y%m%d"),
            end=datetime.now(),
            symbol="ustm3",
            frequency=self._frequency,
        ).loc[self._quotes.index[0] : self._quotes.index[-1]]

        # self._medium_rates = src.read(
        #     start=datetime.strptime("19000101", "%Y%m%d"),
        #     end=datetime.now(),
        #     symbol="usty2",
        #     frequency=self._frequency,
        # ).loc[self._quotes.index[0] : self._quotes.index[-1]]

        self._long_rates = src.read(
            start=datetime.strptime("19000101", "%Y%m%d"),
            end=datetime.now(),
            symbol="usty10",
            frequency=self._frequency,
        ).loc[self._quotes.index[0] : self._quotes.index[-1]]

    def plot(self, ax: axes.Axes) -> None:

        if self._frequency not in (DAILY, WEEKLY, MONTHLY):
            return

        mn, mx = ax.get_ylim()

        top = ((mx - mn) * self._height_ratio) + mn

        rates_max = max(
            self._short_rates.loc[:, "close"].max(),
            self._long_rates.loc[:, "close"].max(),
        )

        # rates_max = max(
        #     max(
        #         self._short_rates.loc[:, "close"].max(),
        #         self._medium_rates.loc[:, "close"].max(),
        #     ),
        #     self._long_rates.loc[:, "close"].max(),
        # )

        rates_min = min(
            self._short_rates.loc[:, "close"].min(),
            self._long_rates.loc[:, "close"].min(),
        )

        # rates_min = min(
        #     min(
        #         self._short_rates.loc[:, "close"].min(),
        #         self._medium_rates.loc[:, "close"].min(),
        #     ),
        #     self._long_rates.loc[:, "close"].min(),
        # )

        self._short_rates -= rates_min
        # self._medium_rates -= rates_min
        self._long_rates -= rates_min

        self._short_rates /= rates_max - rates_min
        # self._medium_rates /= rates_max - rates_min
        self._long_rates /= rates_max - rates_min

        self._short_rates *= top - mn
        # self._medium_rates *= top - mn
        self._long_rates *= top - mn

        self._short_rates += mn
        # self._medium_rates += mn
        self._long_rates += mn

        ax.plot(
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._short_rates.index
            ],
            self._short_rates.loc[
                [d for d in self._short_rates.index if d in self._quotes.index], "close"
            ],
            color=self._line_color_short,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )

        # ax.plot(
        #     [
        #         i
        #         for i, d in enumerate(self._quotes.index)
        #         if d in self._medium_rates.index
        #     ],
        #     self._medium_rates.loc[
        #         [d for d in self._medium_rates.index if d in self._quotes.index],
        #         "close",
        #     ],
        #     color=self._line_color_medium,
        #     alpha=self._line_alpha,
        #     linewidth=self._line_width,
        # )

        ax.plot(
            [
                i
                for i, d in enumerate(self._quotes.index)
                if d in self._long_rates.index
            ],
            self._long_rates.loc[
                [d for d in self._long_rates.index if d in self._quotes.index], "close"
            ],
            color=self._line_color_long,
            alpha=self._line_alpha,
            linewidth=self._line_width,
        )
