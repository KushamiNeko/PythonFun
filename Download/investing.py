import os
from typing import Iterable

from fun.utils import colors, pretty
from happy.download.processor import Processor


class InvestingProcessor(Processor):
    def __init__(self) -> None:
        super().__init__()

        # self._symbols = [
        #     "vstx",
        #     "jniv",
        # ]

    def _urls(self) -> Iterable[str]:
        for url in [
            r"https://www.investing.com/indices/stoxx-50-volatility-vstoxx-eur-historical-data",
            r"https://www.investing.com/indices/jpx-nikkei-400-historical-data",
            r"https://www.investing.com/indices/nikkei-volatility-historical-data",
            r"https://www.investing.com/indices/hsi-volatility-historical-data",
            # r"https://www.investing.com/indices/cboe-china-etf-volatility-historical-data",
        ]:

            pretty.color_print(
                colors.PAPER_CYAN_300,
                f"downloading: {url.split('/')[-1].split('-')[0]}",
            )

            yield url

    def download(self) -> None:
        super().download()

        if self._download_count != len(list(self._urls())):
            pretty.color_print(
                colors.PAPER_RED_400, "download operation miss some files"
            )

    def rename(self) -> None:

        table = {
            "STOXX 50 Volatility VSTOXX EUR Historical Data.csv": "vstx",
            "JPX-Nikkei 400 Historical Data.csv": "nk400",
            "Nikkei Volatility Historical Data.csv": "jniv",
            "HSI Volatility Historical Data.csv": "vhsi",
            # "CBOE China Etf Volatility Historical Data.csv": "vxfxi",
        }

        for fs in os.listdir(self._src):
            symbol = table.get(fs, None)
            if symbol is None:
                continue

            src = os.path.join(self._src, fs)
            tar = os.path.join(self._tar, "investing.com", f"{symbol}.csv")

            assert os.path.exists(os.path.dirname(tar))

            pretty.color_print(
                colors.PAPER_DEEP_PURPLE_200, f"move file: {src} => {tar}"
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
        pass
