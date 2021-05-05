import os
import re
from datetime import datetime
from typing import Iterable, NewType, Optional

from fun.futures.contract import (
    ALL_CONTRACT_MONTHS,
    CONTRACT_MONTHS,
    EVEN_CONTRACT_MONTHS,
    FINANCIAL_CONTRACT_MONTHS,
    month_from_futures_month_code,
)
from fun.utils import colors, pretty
from happy.download.processor import Processor

BARCHART_PAGE = NewType("BARCHART_PAGE", int)
HISTORICAL_PAGE = BARCHART_PAGE(0)
INTERACTIVE_PAGE = BARCHART_PAGE(1)


class BarchartFuturesProcessor(Processor):
    def __init__(
        self,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None,
        # start: Optional[int] = None,
        # end: Optional[int] = None,
        page: BARCHART_PAGE = HISTORICAL_PAGE,
    ) -> None:
        super().__init__()

        assert page in (HISTORICAL_PAGE, INTERACTIVE_PAGE)

        self._page = page

        if start_year is None or end_year is None:
            # if start is None or end is None:
            self._start = datetime.now().year

            if datetime.now().month > 10:
                self._end = datetime.now().year + 1
            else:
                self._end = datetime.now().year
        else:
            self._start = start_year
            self._end = end_year

            # self._start = start
            # self._end = end

        pretty.color_print(
            colors.PAPER_BROWN_300,
            f"Barchart Processor\nstart year: {self._start}, end year: {self._end}",
        )

        self._symbols = [
            "es",
            "nq",
            "qr",
            "ym",
            # "nl",
            "np",
            # "no",
            "fx",
            "zn",
            "ge",
            "tj",
            "gg",
            "dx",
            "j6",
            "e6",
            "b6",
            "a6",
            "n6",
            "d6",
            "s6",
            "gc",
            "cl",
        ]

    def _urls(self) -> Iterable[str]:
        months: CONTRACT_MONTHS

        month_table = {
            "cl": ALL_CONTRACT_MONTHS,
            "gc": EVEN_CONTRACT_MONTHS,
        }

        for symbol in self._symbols:
            months = month_table.get(symbol, FINANCIAL_CONTRACT_MONTHS)
            # if symbol == "cl":
            #     months = ALL_CONTRACT_MONTHS
            # elif symbol == "gc":
            #     months = EVEN_CONTRACT_MONTHS
            # else:
            #     months = FINANCIAL_CONTRACT_MONTHS

            for y in range(self._start, self._end + 1):
                for m in months:
                    code = f"{symbol}{m}{y % 100:02}"

                    pretty.color_print(colors.PAPER_CYAN_300, f"downloading: {code}")

                    if self._page == HISTORICAL_PAGE:
                        yield f"https://www.barchart.com/futures/quotes/{code}/historical-download"
                    elif self._page == INTERACTIVE_PAGE:
                        yield f"https://www.barchart.com/futures/quotes/{code}/interactive-chart"
                    else:
                        raise ValueError("unknown barchart page")

                input()

    def download(self) -> None:
        super().download()

        if self._download_count != len(self._symbols):
            pretty.color_print(
                colors.PAPER_RED_400, "download operation miss some files"
            )

    def rename(self) -> None:
        for fs in os.listdir(self._src):
            match = re.match(
                r"^([\w\d]{5})_([^_-]+)(?:-[^_-]+)*_[^_-]+-[^_-]+-\d{2}-\d{2}-\d{4}.csv$",
                fs,
            )
            if match is None:
                match = re.match(
                    r"^([\w\d]{5})_[^_]+_[^_]+_[^_]+_([^_]+)(?:_[^_]+)*_\d{2}_\d{2}_\d{4}.csv$",
                    fs,
                )

                if match is None:
                    continue

            if match is not None:
                code = match.group(1).lower()

                src = os.path.join(self._src, fs)
                tar = os.path.join(self._tar, "continuous", code[:2], f"{code}.csv")

                assert os.path.exists(os.path.dirname(tar))

                pretty.color_print(
                    colors.PAPER_DEEP_PURPLE_300, f"move file: {src} => {tar}"
                )

                os.rename(src, tar)

                self._rename_count += 1

        pretty.color_print(
            colors.PAPER_LIGHT_GREEN_A200, f"rename {self._rename_count} files"
        )

        if self._download_count != self._rename_count:
            pretty.color_print(
                colors.PAPER_RED_400, "rename operation miss some downloaded files"
            )

    def check(self) -> None:
        months: CONTRACT_MONTHS
        for symbol in self._symbols:
            if symbol == "cl":
                months = ALL_CONTRACT_MONTHS
            elif symbol == "gc":
                months = EVEN_CONTRACT_MONTHS
            else:
                months = FINANCIAL_CONTRACT_MONTHS

            for y in range(self._start, self._end + 1):
                for m in months:
                    code = f"{symbol}{m}{y % 100:02}"

                    tar = os.path.join(self._tar, "continuous", code[:2], f"{code}.csv")

                    if not os.path.exists(tar):
                        pretty.color_print(
                            colors.PAPER_PINK_300, f"missing files: {tar}"
                        )


class BarchartStocksProcessor(Processor):
    def __init__(
        self,
        page: BARCHART_PAGE = HISTORICAL_PAGE,
    ) -> None:
        super().__init__()

        assert page in (HISTORICAL_PAGE, INTERACTIVE_PAGE)

        self._page = page

        pretty.color_print(
            colors.PAPER_BROWN_300,
            "Barchart Stocks Processor",
        )

        self._symbols_table = {
            # "$iqx": "spxew",
            # "$slew": "smlew",
            # "$sdew": "midew",
            # "$topx": "topix",
            # "$addn": "addn",
            # "$addq": "addq",
            # "$avdn": "avdn",
            # "$avdq": "avdq",
            # "$addt": "addt",
            # "$avdt": "avdt",
            "^btcusd": "btcusd",
            "^ethusd": "ethusd",
            "^ltcusd": "ltcusd",
            "^xrpusd": "xrpusd",
            "$dxy": "dxy",
            "^eurusd": "eurusd",
            "^usdjpy": "usdjpy",
            # "^jpyusd": "jpyusd",
            "^gbpusd": "gbpusd",
            "^audusd": "audusd",
            "^usdcad": "usdcad",
            # "^cadusd": "cadusd",
            "^usdchf": "usdchf",
            "^nzdusd": "nzdusd",
            # "^chfusd": "chfusd",
            "^eurjpy": "eurjpy",
            "^eurgbp": "eurgbp",
            "^euraud": "euraud",
            "^eurcad": "eurcad",
            "^eurchf": "eurchf",
            "^gbpjpy": "gbpjpy",
            "^audjpy": "audjpy",
            "^cadjpy": "cadjpy",
            # "^nzdjpy": "nzdjpy",
        }

    def _urls(self) -> Iterable[str]:
        months: CONTRACT_MONTHS
        for symbol in self._symbols_table.keys():
            pretty.color_print(colors.PAPER_CYAN_300, f"downloading: {symbol}")

            if self._page == HISTORICAL_PAGE:
                yield f"https://www.barchart.com/futures/quotes/{symbol}/historical-download"
            elif self._page == INTERACTIVE_PAGE:
                yield f"https://www.barchart.com/futures/quotes/{symbol}/interactive-chart"
            else:
                raise ValueError("unknown barchart page")

    def rename(self) -> None:
        for fs in os.listdir(self._src):
            match = re.match(
                # r"^(\$[\w]+)_([^_-]+)(?:-[^_-]+)*_[^_-]+-[^_-]+-\d{2}-\d{2}-\d{4}.csv$",
                r"^([\$\^][\w]+)_([^_-]+)(?:-[^_-]+)*_[^_-]+-[^_-]+-\d{2}-\d{2}-\d{4}.csv$",
                fs,
            )
            if match is None:
                continue
            else:
                symbol = match.group(1).lower()

                symbol = self._symbols_table.get(symbol, None)
                if symbol is None:
                    continue

                src = os.path.join(self._src, fs)
                tar = os.path.join(self._tar, "barchart", f"{symbol}.csv")

                assert os.path.exists(os.path.dirname(tar))

                pretty.color_print(
                    colors.PAPER_DEEP_PURPLE_300, f"move file: {src} => {tar}"
                )

                os.rename(src, tar)

                self._rename_count += 1

        pretty.color_print(
            colors.PAPER_LIGHT_GREEN_A200, f"rename {self._rename_count} files"
        )

        if self._download_count != self._rename_count:
            pretty.color_print(
                colors.PAPER_RED_400, "rename operation miss some downloaded files"
            )

    def check(self) -> None:
        for symbol in self._symbols_table.keys():
            tar = os.path.join(self._tar, "barchart", symbol, f"{symbol}.csv")

            if not os.path.exists(tar):
                pretty.color_print(colors.PAPER_PINK_300, f"missing files: {tar}")
