from __future__ import annotations

import argparse
import os
import re

import config
import cv2
import numpy as np
from fun.utils import colors, pretty
from happy.compare_charts.chart import Charts
from happy.compare_charts.cover import Cover


def parse_arg():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "--symbols", metavar="", type=str, nargs="+", help="symbols to compare",
    )

    parser.add_argument(
            "--year", metavar="", type=str, help="year of the chart",
    )

    parser.add_argument(
            "--frequency", metavar="", type=str, help="chart frequency",
    )

    args = vars(parser.parse_args())

    symbols = args.get("symbols", None)
    if symbols is None:
        pretty.color_print(colors.PAPER_RED_400, "invalid symbols")
        exit(1)

    if len(symbols) < 2:
        pretty.color_print(colors.PAPER_RED_400, "need at least 2 symbols")
        exit(1)

    year = args.get("year", None)
    if year is None or not re.match(r"\d{4}", year):
        pretty.color_print(colors.PAPER_RED_400, "invalid year")
        exit(1)

    frequency = args.get("frequency", None)
    if frequency is None or not re.match(r"d|w", frequency):
        pretty.color_print(colors.PAPER_RED_400, "invalid frequency")
        exit(1)

    return symbols, year, frequency


def main():
    symbols, year, frequency = parse_arg()

    charts = Charts(symbols, year, frequency)
    cover = Cover(charts.studying.image.shape, config.COVER_COLOR)

    cv2.namedWindow("Chart")
    cv2.setWindowTitle("Chart", os.path.basename(charts.studying.file_path))
    cv2.setMouseCallback("Chart", Cover.draw, cover)

    while True:
        k = cv2.waitKey(1) & 0xFF

        if k == 32:
            cover.next_function()

        if k == 27:
            break

        if 49 <= k <= 57:
            i = k - 49

            if i >= charts.length:
                i = charts.length - 1

            charts.set_studying_with_index(i)
            cv2.setWindowTitle("Chart", os.path.basename(charts.studying.file_path))

        studying_symbol = charts.studying.symbol

        new_frequency = None

        if k == 100:
            new_frequency = "d"
        elif k == 119:
            new_frequency = "w"
        elif k == 109:
            # new_frequency = "m"
            pass
        elif k == 104:
            # new_frequency = "h"
            pass

        if new_frequency:
            try:
                charts = Charts(symbols, charts.studying.year, new_frequency)
            except ValueError as err:
                pretty.color_print(colors.PAPER_RED_400, err)

        new_year = None

        if k == 81:
            new_year = charts.studying.year - 1
        if k == 83:
            new_year = charts.studying.year + 1

        if new_year:
            if new_year < config.START_YEAR:
                new_year = config.START_YEAR
            elif new_year > config.END_YEAR:
                new_year = config.END_YEAR

            try:
                charts = Charts(symbols, new_year, charts.studying.frequency)
            except ValueError as err:
                pretty.color_print(colors.PAPER_RED_400, err)

        if new_frequency or new_year:
            charts.set_studying_with_symbol(studying_symbol)
            cv2.setWindowTitle("Chart", os.path.basename(charts.studying.file_path))

        if cv2.getWindowProperty("Chart", cv2.WND_PROP_VISIBLE) < 1:
            break

        display = np.zeros(charts.studying.image.shape, np.uint8)
        cv2.subtract(charts.studying.image, cover.image, display)

        cv2.imshow("Chart", display)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
