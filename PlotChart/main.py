import argparse
import os
import re
import time
from datetime import datetime
from typing import List, Optional, cast

from fun.chart.base import LARGE_CHART
from fun.chart.preset import CandleSticksPreset
from fun.data.source import DAILY, WEEKLY
from fun.plotter.plotter import Plotter
from fun.plotter.records import LeverageRecords
from fun.trading.agent import TradingAgent
from fun.trading.transaction import FuturesTransaction
from fun.utils import colors, pretty


def read_records(title: str) -> Optional[List[FuturesTransaction]]:
    root = os.path.join(
            cast(str, os.getenv("HOME")), "Documents", "database", "testing", "json"
    )

    agent = TradingAgent(root=root, new_user=True)
    return agent.read_records(title)


def plot_chart(
        symbol: str, year: int, book: str, show_records: bool, outdir: Optional[str]
) -> None:
    date = datetime.strptime(f"{year + 1}0101", "%Y%m%d")

    for frequency in (DAILY, WEEKLY):
        fw = ""
        if frequency == DAILY:
            fw = "d"
        elif frequency == WEEKLY:
            fw = "w"

        assert fw != ""

        preset = CandleSticksPreset(date, symbol, frequency, chart_size=LARGE_CHART)

        plotters: List[Plotter] = [
        ]
        if show_records:
            ts = read_records(book)
            if ts is not None and len(ts) > 0:
                plotters.append(
                        LeverageRecords(
                                quotes=preset.quotes(),
                                frequency=frequency,
                                records=ts,
                                font_color=preset.theme().get_color("text"),
                                font_properties=preset.theme().get_font(
                                        preset.setting().text_fontsize()
                                ),
                        )
                )

        buffer = preset.render(additional_plotters=plotters)
        path = f"{year}_{symbol}_{fw}.png"

        pretty.color_print(colors.PAPER_CYAN_300, f"symbol: {symbol}")
        pretty.color_print(colors.PAPER_CYAN_300, f"year: {year}")
        pretty.color_print(colors.PAPER_CYAN_300, f"book: {book}")
        pretty.color_print(colors.PAPER_CYAN_300, f"records: {show_records}")
        pretty.color_print(colors.PAPER_CYAN_300, f"outdir: {outdir}")
        pretty.color_print(colors.PAPER_CYAN_300, f"file: {path}")

        if outdir is not None:
            assert os.path.exists(outdir)
            path = os.path.join(outdir, path)

            with open(path, "wb") as f:
                f.write(buffer.getbuffer())


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument("--symbols", metavar="", nargs="+", type=str, help="symbols")

    parser.add_argument("--year", metavar="", type=str, help="the year of the chart")

    parser.add_argument(
            "--book",
            metavar="",
            type=str,
            nargs="?",
            const="",
            default="",
            help="the book of the records",
    )

    parser.add_argument("--outdir", metavar="", type=str, help="output folder")

    parser.add_argument(
            "--records",
            metavar="",
            type=bool,
            nargs="?",
            const=True,
            default=False,
            help="whether to show trading records on the chart",
    )

    args = vars(parser.parse_args())

    assert args.get("symbols") is not None
    assert args.get("year") is not None
    assert args.get("book") is not None
    assert args.get("records") is not None

    symbols = cast(str, args.get("symbols"))
    year = cast(str, args.get("year"))
    book = cast(str, args.get("book"))
    show_records = args.get("records", False)
    outdir = args.get("outdir")

    start: str
    end: str

    match = re.match(r"^(\d{4})(?:-|~)?(\d{4})?$", year)
    if match is None:
        pretty.color_print(colors.PAPER_RED_400, f"invaid year: {year}")
        exit(1)
    else:
        start = match.group(1)
        end = match.group(2)

    assert start is not None

    if show_records is True:
        if len(book.strip()) == 0:
            pretty.color_print(colors.PAPER_RED_400, f"empty book")
            exit(1)

    pretty.color_print(colors.PAPER_INDIGO_300, f"symbols: {', '.join(symbols)}")
    pretty.color_print(colors.PAPER_INDIGO_300, f"year: {year}")
    pretty.color_print(colors.PAPER_INDIGO_300, f"book: {book}")
    pretty.color_print(colors.PAPER_INDIGO_300, f"records: {show_records}")
    pretty.color_print(colors.PAPER_INDIGO_300, f"outdir: {outdir}")

    pretty.color_print(colors.PAPER_AMBER_300, "chart plotting start...")
    process_start = time.time()

    for symbol in symbols:
        if end is None:
            plot_chart(
                    symbol=symbol,
                    year=int(start),
                    show_records=show_records,
                    outdir=outdir,
                    book=book,
            )

        else:
            for i in range(int(start), int(end) + 1):
                plot_chart(
                        symbol=symbol,
                        year=i,
                        show_records=show_records,
                        outdir=outdir,
                        book=book,
                )

    process_end = time.time()
    length = process_end - process_start

    pretty.color_print(colors.PAPER_AMBER_300, "chart plotting completed!!!")
    pretty.color_print(colors.PAPER_AMBER_300, f"processing time: {length} seconds")


if __name__ == "__main__":
    main()
