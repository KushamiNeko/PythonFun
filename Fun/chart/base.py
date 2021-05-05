import io
from abc import ABCMeta, abstractmethod
from typing import List, NewType, Optional, Tuple, Union

import numpy as np
import pandas as pd
from Fun.plotter.plotter import Plotter

CHART_SIZE = NewType("CHART_SIZE", int)
LARGE_CHART = CHART_SIZE(0)
MEDIUM_CHART = CHART_SIZE(1)
SMALL_CHART = CHART_SIZE(2)


class ChartFactory(metaclass=ABCMeta):
    def __init__(self, quotes: pd.DataFrame) -> None:
        assert quotes is not None

        self._quotes = quotes

    def quotes_range(self) -> Tuple[float, float]:
        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])

        return mn, mx

    def chart_xrange(self) -> Tuple[float, float]:
        return -0.5, (len(self._quotes) - 1) + 0.5

    def chart_yrange(self) -> Tuple[float, float]:
        extend_ratio = 0.0025

        mn, mx = self.quotes_range()
        mid = (mn + mx) / 2.0

        ratio = (mx - mid) / mid

        if ratio < 0.01:
            extend_ratio = 0.00035
        elif ratio < 0.05:
            extend_ratio = 0.002
        elif ratio < 0.1:
            extend_ratio = 0.0035
        elif ratio < 0.5:
            extend_ratio = 0.01
        else:
            extend_ratio = 0.05

        return (mn * (1 - extend_ratio), mx * (1 + extend_ratio))

    @abstractmethod
    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        raise NotImplementedError

    @abstractmethod
    def render(
        self,
        output: Optional[Union[str, io.BytesIO]] = None,
        plotters: Optional[List[Plotter]] = None,
        interactive: bool = False,
    ) -> None:
        raise NotImplementedError
