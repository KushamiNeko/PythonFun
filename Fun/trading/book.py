from __future__ import annotations

import re
import time
from typing import Dict

from fun.utils import helper


class TradingBook:
    def __init__(self, title: str, index: str = "", last_modified: float = 0, ) -> None:

        if title == "":
            raise ValueError("invaild book title")
        self._title = title

        if last_modified is None or last_modified <= 0:
            self._last_modified = time.time()
        else:
            self._last_modified = last_modified

        if index is None or index == "":
            self._index = helper.random_string()
        else:
            if not re.match(r"^[0-9a-zA-Z]+$", index):
                raise ValueError("invalid book index")
            self._index = index

    def title(self) -> str:
        return self._title

    def index(self) -> str:
        return self._index

    def last_modified(self) -> float:
        return self._last_modified

    def update_last_modified(self) -> None:
        self._last_modified = time.time()

    def to_entity(self) -> Dict[str, str]:
        return {
            "title":         self._title,
            "index":         self._index,
            "last_modified": f"{self._last_modified}",
        }

    @classmethod
    def from_entity(cls, entity: Dict[str, str]) -> TradingBook:

        return TradingBook(
                title=entity["title"],
                index=entity.get("index", ""),
                last_modified=float(entity.get("last_modified", "0")),
        )
