import os

import config
import cv2
from fun.utils import colors, pretty


class Chart:
    def __init__(self, symbol, year, frequency, file_path, image):
        self._symbol = symbol
        self._year = year
        self._frequency = frequency
        self._file_path = file_path
        self._image = image

    @property
    def symbol(self):
        return self._symbol

    @property
    def year(self):
        return int(self._year)

    @property
    def frequency(self):
        return self._frequency

    @property
    def file_path(self):
        return self._file_path

    @property
    def image(self):
        return self._image


class Charts:
    def __init__(self, symbols, year, frequency):

        if len(symbols) == 0:
            raise ValueError("empty symbols")

        self._symbols = symbols
        self._year = year
        self._frequency = frequency

        self._charts = []
        self._studying = None

        self._get_charts()

    @property
    def length(self):
        return len(self._charts)

    @property
    def studying(self):
        return self._studying

    def set_studying_with_index(self, index):
        self._studying = self._charts[index]

    def set_studying_with_symbol(self, symbol):
        for chart in self._charts:
            if chart.symbol == symbol:
                self._studying = chart

    def _get_charts(self):

        for i, symbol in enumerate(self._symbols):
            path = os.path.join(
                    config.ROOT,
                    symbol,
                    self._frequency,
                    f"{self._year}_{symbol}_{self._frequency}.png",
            )
            if not os.path.exists(path):
                pretty.color_print(
                        colors.PAPER_RED_400,
                        f"invalid symbol {symbol.upper()} with frequency {self._frequency.upper()}",
                )

                continue

            chart = cv2.imread(path, cv2.IMREAD_COLOR)
            chart = cv2.resize(chart, config.SIZE)

            self._charts.append(Chart(symbol, self._year, self._frequency, path, chart))

        if len(self._charts) == 0:
            raise ValueError("empty charts")

        self._studying = self._charts[0]
