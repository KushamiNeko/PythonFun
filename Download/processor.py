import os
import subprocess
from abc import ABCMeta, abstractmethod
from typing import Iterable, cast

from fun.utils import colors, pretty


class Processor(metaclass=ABCMeta):
    def __init__(self) -> None:
        self._src = os.path.join(cast(str, os.getenv("HOME")), "Downloads")
        self._tar = os.path.join(
            cast(str, os.getenv("HOME")), "Documents", "data_source"
        )

        self._download_count = 0
        self._rename_count = 0

        assert os.path.exists(self._src)
        assert os.path.exists(self._tar)

    @abstractmethod
    def _urls(self) -> Iterable[str]:
        raise NotImplementedError

    def download(self) -> None:
        count = 0
        for url in self._urls():
            # subprocess.Popen(["google-chrome", url])
            subprocess.Popen(["firefox", url])
            count += 1

        self._download_count = count

        pretty.color_input(
            colors.PAPER_LIGHT_GREEN_A200,
            f"download {self._download_count} files",
        )

        pretty.color_input(
            colors.PAPER_LIME_300,
            "download completed, press any key to rename the files",
        )

    @abstractmethod
    def rename(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def check(self) -> None:
        raise NotImplementedError
