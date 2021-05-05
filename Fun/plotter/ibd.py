from datetime import datetime, timedelta
from typing import Dict, List, NewType, Optional

import numpy as np
import pandas as pd
from Fun.data.source import DAILY, FREQUENCY, Yahoo
from Fun.plotter.plotter import TextPlotter
from Fun.utils import colors, pretty
from matplotlib import axes, font_manager as fm

DAY_ACTION = NewType("DAY_ACTION", int)
FOLLOW_THROUGH = DAY_ACTION(0)
DISTRIBUTION = DAY_ACTION(1)
NEUTRAL = DAY_ACTION(2)


class DistributionsDay(TextPlotter):
    _dataframes = None

    @classmethod
    def _get_dataframes(cls) -> Optional[Dict[str, pd.DataFrame]]:
        return cls._dataframes

    @classmethod
    def _init_dataframes(cls) -> None:
        cls._dataframes = {}

    @classmethod
    def _add_dataframe(cls, key: str, dataframe: pd.DataFrame) -> None:
        cls._dataframes[key] = dataframe

    def __init__(
            self,
            quotes: pd.DataFrame,
            frequency: FREQUENCY,
            reference_symbols: List[str] = ("spx", "compq", "sml"),
            distribution_threshold: float = -0.2,
            distribution_invalid_threshold: float = 5.0,
            distribution_color: str = colors.PAPER_LIME_300,
            days_pass_invalid_threshold: int = 35,
            invalid_distribution_color: str = colors.PAPER_ORANGE_400,
            xoffset: float = 3,
            font_color: str = "r",
            font_size: float = 10.0,
            font_src: Optional[str] = None,
            font_properties: Optional[fm.FontProperties] = None,
            info_font_properties: Optional[fm.FontProperties] = None,
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

        self._reference_symbols = reference_symbols

        self._distribution_threshold = distribution_threshold

        self._distribution_color = distribution_color
        self._invalid_distribution_color = invalid_distribution_color

        if info_font_properties is None:
            self._info_font_properties = font_properties
        else:
            self._info_font_properties = info_font_properties

        self._xoffset = xoffset

        self._days_pass_invalid_threshold = days_pass_invalid_threshold
        self._distribution_invalid_threshold = distribution_invalid_threshold

        src = Yahoo()

        if self._get_dataframes() is None or (
                self._get_dataframes() is not None and len(self._get_dataframes().keys()) == 0):

            print("init dataframes")

            if self._get_dataframes() is None:
                self._init_dataframes()

            for symbol in self._reference_symbols:
                self._add_dataframe(
                        symbol,
                        src.read(
                                start=datetime.strptime("19000101", "%Y%m%d"),
                                end=datetime.utcnow() + timedelta(days=2),
                                symbol=symbol,
                                frequency=self._frequency,
                        ).loc[self._quotes.index[0]: self._quotes.index[-1]],
                )

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency != DAILY:
            return

        assert ax is not None
        assert self._get_dataframes() is not None

        counts = {}

        for x in range(len(self._quotes.index)):
            if x == 0:
                continue

            labels = []
            action = NEUTRAL
            color = self._invalid_distribution_color
            for key, quotes in self._get_dataframes().items():
                index = self._quotes.index[x]
                if index not in quotes.index:
                    pretty.color_print(
                            colors.PAPER_AMBER_300, f"skip {index} in {key}",
                    )
                    continue

                current_close = quotes.loc[index, "close"]
                current_volume = quotes.loc[index, "volume"]

                index = self._quotes.index[x - 1]
                if index not in quotes.index:
                    pretty.color_print(
                            colors.PAPER_AMBER_300, f"skip {index} in {key}",
                    )
                    continue

                previous_close = quotes.loc[index, "close"]
                previous_volume = quotes.loc[index, "volume"]

                if current_close <= 0 or previous_close <= 0:
                    continue

                if current_volume <= 0 or previous_volume <= 0:
                    continue

                move = ((current_close - previous_close) / previous_close) * 100.0

                if (
                        move < self._distribution_threshold
                        and current_volume > previous_volume
                ):
                    action = DISTRIBUTION

                    for k in key:
                        if k.upper() not in labels:
                            labels.append(k.upper())
                            break

                    if (
                            self._quotes.index[-1] - self._quotes.index[x]
                    ).days < self._days_pass_invalid_threshold:

                        color = self._distribution_color
                        if key in counts:
                            counts[key] += 1
                        else:
                            counts[key] = 1

            if action != NEUTRAL:
                highs = self._quotes.loc[:, "high"]
                lows = self._quotes.loc[:, "low"]

                mx = highs.max()
                mn = lows.min()
                mr = mx - mn

                middle = (mx + mn) / 2.0

                h = highs.iloc[x]
                l = lows.iloc[x]
                m = (h + l) / 2.0

                offset = mr * 0.0075

                y = l - offset if m < middle else h + offset
                va = "top" if m < middle else "bottom"

                arrow = "↑" if action == FOLLOW_THROUGH else "↓"

                labels.append(arrow)

                text = "\n".join(labels)

                ax.text(
                        x,
                        y,
                        text,
                        color=color,
                        fontproperties=self._font_properties,
                        ha="center",
                        va=va,
                )

        if len(self._quotes) > 1:
            text = "\n".join(
                    f"{k.upper()}: {counts.get(k, 0)}" for k in self._reference_symbols
            )

            h = np.amax(self._quotes.loc[:, "high"])
            l = np.amin(self._quotes.loc[:, "low"])

            lh = np.amax(self._quotes.iloc[-30:].loc[:, "high"])
            ll = np.amin(self._quotes.iloc[-30:].loc[:, "low"])

            y: float
            va: str
            if abs(l - ll) > abs(h - lh):
                y = np.amin(self._quotes.loc[:, "low"])
                va = "bottom"
            else:
                y = np.amax(self._quotes.loc[:, "high"])
                va = "top"

            ax.text(
                    len(self._quotes.index) - self._xoffset,
                    y,
                    text,
                    color=self._font_color,
                    fontproperties=self._info_font_properties,
                    ha="right",
                    va=va,
            )
