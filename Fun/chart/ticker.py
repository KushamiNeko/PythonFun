from abc import ABCMeta, abstractmethod
from typing import List, Optional, Tuple

import numpy as np
import pandas as pd
from fun.data.source import (
    DAILY,
    FREQUENCY,
    INTRADAY_15MINUTES,
    INTRADAY_30MINUTES,
    INTRADAY_60MINUTES,
    MONTHLY,
    WEEKLY,
)
from matplotlib import ticker


class Ticker(metaclass=ABCMeta):
    @abstractmethod
    def ticks(self) -> Tuple[List[float], List[str]]:
        raise NotImplementedError


class TimeTicker(Ticker):
    def __init__(self, quotes: pd.DataFrame) -> None:
        self._quotes = quotes

    def ticks(self) -> Tuple[List[float], List[str]]:
        frequency: FREQUENCY

        start = self._quotes.index[0]
        end = self._quotes.index[-1]

        period = end - start
        if period.days < 3:
            frequency = INTRADAY_15MINUTES
        elif period.days < 6:
            frequency = INTRADAY_30MINUTES
        elif period.days < 16:
            frequency = INTRADAY_60MINUTES
        elif period.days < 365:
            frequency = DAILY
        elif period.days < 365 * 5:
            frequency = WEEKLY
        else:
            frequency = MONTHLY

        assert frequency is not None

        loc: List[float] = []
        labels: List[str] = []

        if frequency == DAILY:
            dates = self._quotes.index.strftime("%Y-%b")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

        elif frequency == WEEKLY:
            dates = self._quotes.index.strftime("%Y-%b")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

            func = np.vectorize(
                lambda x: x.split("-")[0] if "Jan" in x else x.split("-")[1]
            )
            labels = func(labels)

        elif frequency == MONTHLY:
            dates = self._quotes.index.strftime("%Y")
            labels = np.unique(dates)
            loc = [np.argwhere(dates == l).min() for l in labels]

        elif frequency == INTRADAY_60MINUTES:
            pattern = "%y-%m-%d\n%H:%M"
            dates = self._quotes.index.strftime(pattern)

            labels = self._quotes.index[
                (self._quotes.index.hour == 17)
                | (self._quotes.index.hour == 6)
                | (self._quotes.index.hour == 0)
                | (self._quotes.index.hour == 11)
            ].strftime(pattern)
            loc = [np.argwhere(dates == l).min() for l in labels]

        elif frequency == INTRADAY_15MINUTES or frequency == INTRADAY_30MINUTES:
            pattern = "%y-%m-%d\n%H:%M"
            dates = self._quotes.index.strftime(pattern)

            labels = self._quotes.index[
                (
                    (self._quotes.index.hour == 17)
                    | (self._quotes.index.hour == 6)
                    | (self._quotes.index.hour == 0)
                    | (self._quotes.index.hour == 11)
                )
                & (self._quotes.index.minute == 0)
            ].strftime(pattern)
            loc = [np.argwhere(dates == l).min() for l in labels]

        else:
            raise NotImplementedError

        aloc = np.array(loc)
        condition = aloc >= 4

        return np.extract(condition, aloc), np.extract(condition, labels)


class StepTicker(Ticker):
    def __init__(
        self,
        mn: float,
        mx: float,
        nbins: int = 25,
        steps: Optional[List[int]] = [1, 2, 5, 10],
        decimals: int = 3,
    ) -> None:
        self._nbins = nbins
        self._steps = steps
        self._min = mn
        self._max = mx

        self._decimals = decimals

    def ticks(self) -> Tuple[List[float], List[str]]:
        locator = ticker.MaxNLocator(nbins=self._nbins, steps=self._steps)
        values = locator.tick_values(self._min, self._max)

        return values, [f"{v:.{self._decimals}f}" for v in values]
