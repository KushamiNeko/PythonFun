from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from matplotlib import axes

from fun.data.source import DAILY, FREQUENCY
from fun.plotter.plotter import Plotter
from fun.utils import colors


class EntryZone(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        operation: str,
        notice_signal: Optional[datetime] = None,
        prepare_signal: Optional[datetime] = None,
        notice_to_entry_minimum_days: int = 30,
        notice_to_entry_warning_days: int = 30,
        prepare_minimum_days: int = 5,
        prepare_warning_days: int = 9,
        color_notice_stop: str = colors.PAPER_RED_600,
        color_notice_warning: str = colors.PAPER_RED_200,
        color_prepare_stop: str = colors.PAPER_PINK_600,
        color_prepare_warning: str = colors.PAPER_PINK_200,
        alpha: float = 0.15,
    ) -> None:
        assert quotes is not None

        assert operation in ("long" "short")

        self._quotes = quotes
        self._frequency = frequency

        self._operation = operation

        self._notice_signal = notice_signal
        self._prepare_signal = prepare_signal

        self._notice_to_entry_minimum_days = notice_to_entry_minimum_days
        self._notice_to_entry_warning_days = notice_to_entry_warning_days

        self._prepare_minimum_days = prepare_minimum_days
        self._prepare_warning_days = prepare_warning_days

        self._color_notice_stop = color_notice_stop
        self._color_notice_warning = color_notice_warning
        self._color_prepare_stop = color_prepare_stop
        self._color_prepare_warning = color_prepare_warning

        self._alpha = alpha

    def plot(self, ax: axes.Axes) -> None:
        if self._frequency != DAILY:
            return

        mn, mx = ax.get_ylim()

        try:
            if self._notice_signal is not None:
                first_signal_index = self._quotes.index.get_loc(self._notice_signal)
                minimum_days_index = self._quotes.index.get_loc(
                    self._notice_signal
                    + timedelta(days=self._notice_to_entry_minimum_days),
                    method="nearest",
                )

                ax.bar(
                    first_signal_index,
                    width=minimum_days_index - first_signal_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_notice_stop,
                    alpha=self._alpha,
                )

            if self._prepare_signal is not None:
                prepare_signal_index = self._quotes.index.get_loc(self._prepare_signal)
                minimum_days_index = self._quotes.index.get_loc(
                    self._prepare_signal + timedelta(days=self._prepare_minimum_days),
                    method="nearest",
                )
                warning_days_index = self._quotes.index.get_loc(
                    self._prepare_signal + timedelta(days=self._prepare_warning_days),
                    method="nearest",
                )

                ax.bar(
                    prepare_signal_index,
                    width=minimum_days_index - prepare_signal_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_prepare_stop,
                    alpha=self._alpha,
                )

                ax.bar(
                    minimum_days_index,
                    width=warning_days_index - minimum_days_index,
                    bottom=mn,
                    height=mx - mn,
                    align="edge",
                    color=self._color_prepare_warning,
                    alpha=self._alpha,
                )

        except KeyError:
            return
