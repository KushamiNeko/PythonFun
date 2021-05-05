from __future__ import annotations

import re
import time
from datetime import datetime
from typing import Dict

from Fun.utils import helper


class FuturesTransaction:
    def __init__(
        self,
        dtime: datetime,
        symbol: str,
        operation: str,
        leverage: float,
        price: float,
        index: str = "",
        time_stamp: float = 0,
    ) -> None:

        if index is None or index == "":
            self._index = helper.random_string(length=16)
        else:
            if not re.match(r"[0-9a-zA-Z]+", index):
                raise ValueError("invalid transaction index")
            self._index = index

        if time_stamp is None or time_stamp <= 0:
            self._time_stamp = time.time()
        else:
            self._time_stamp = time_stamp

        if type(dtime) is not datetime:
            raise ValueError("invalid transaction time")
        self._datetime = dtime

        if not re.match(r"^[a-zA-Z]+$", symbol):
            raise ValueError("invalid transaction symbol")
        self._symbol = symbol.lower()

        if not re.match(r"^[+-]$", operation):
            raise ValueError("invalid transaction operation")
        self._operation = operation

        if leverage <= 0:
            raise ValueError("invalid transaction leverage")
        self._leverage = leverage

        if price <= 0.0:
            raise ValueError("invalid transaction price")
        self._price = price

    def index(self) -> str:
        return self._index

    def time_stamp(self) -> float:
        return self._time_stamp

    def datetime(self) -> datetime:
        return self._datetime

    def symbol(self) -> str:
        return self._symbol

    def operation(self) -> str:
        return self._operation

    def leverage(self) -> float:
        return self._leverage

    def price(self) -> float:
        return self._price

    def to_entity(self) -> Dict[str, str]:
        return {
            "index": self._index,
            "time_stamp": f"{self._time_stamp}",
            "datetime": self._datetime.strftime("%Y%m%d"),
            "symbol": self._symbol,
            "operation": self._operation,
            "leverage": f"{self._leverage}",
            "price": f"{self._price}",
        }

    @classmethod
    def from_entity(cls, entity: Dict[str, str]) -> FuturesTransaction:
        return FuturesTransaction(
            dtime=datetime.strptime(entity["datetime"], "%Y%m%d"),
            symbol=entity["symbol"],
            operation=entity["operation"],
            leverage=float(entity["leverage"]),
            price=float(entity["price"]),
            index=entity.get("index", ""),
            time_stamp=float(entity.get("time_stamp", 0)),
        )

