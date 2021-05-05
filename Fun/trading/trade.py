from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, List

from Fun.trading.transaction import FuturesTransaction


class FuturesTrade:
    _float_decimals = 4

    def __init__(self, orders: List[FuturesTransaction]) -> None:
        if orders is None or len(orders) == 0:
            raise ValueError("empty trade orders")

        assert orders is not None and len(orders) > 0

        self._orders = sorted(
                orders, key=lambda x: x.datetime() + timedelta(seconds=x.time_stamp())
        )

        self._open_orders: List[FuturesTransaction]
        self._close_orders: List[FuturesTransaction]
        self._validate_orders()

    def _validate_orders(self) -> None:
        if (self._orders[0].operation() not in ("+", "-")) or (
                self._orders[-1].operation() not in ("-", "+")
        ):
            raise ValueError("invalid trade orders operation")

        open_orders: List[FuturesTransaction] = []
        close_orders: List[FuturesTransaction] = []

        open_leverage = 0.0
        close_leverage = 0.0

        for o in self._orders:
            if o.symbol() != self.symbol():
                raise ValueError(
                        f"mismatch symbol in orders: {o.symbol}, {self.symbol}"
                )

            if o.operation() == self.operation():
                open_leverage += o.leverage()
                open_orders.append(o)
            else:
                close_leverage += o.leverage()
                close_orders.append(o)

        if open_leverage != close_leverage:
            raise ValueError(
                    f"leverage of open and close contracts do not match\nopen: {open_leverage}, close: {close_leverage}"
            )

        self._open_orders = open_orders
        self._close_orders = close_orders

    def operation(self) -> str:
        return self._orders[0].operation()

    def leverage(self) -> float:
        q = 0.0
        for o in self._open_orders:
            q += o.leverage()

        return q

    def symbol(self) -> str:
        return self._orders[0].symbol()

    def open_time(self) -> datetime:
        return self._orders[0].datetime()

    def close_time(self) -> datetime:
        return self._orders[-1].datetime()

    def open_time_stamp(self) -> float:
        return self._orders[0].time_stamp()

    def close_time_stamp(self) -> float:
        return self._orders[-1].time_stamp()

    def _average_price(self, orders: List[FuturesTransaction]) -> float:
        leverage = 0.0
        total_price = 0.0

        for order in orders:
            total_price += order.price() * order.leverage()
            leverage += order.leverage()

        return total_price / float(leverage)

    def average_open(self) -> float:
        average_open = self._average_price(self._open_orders)

        if self.operation() == "+":
            average_open *= -1

        return average_open

    def average_close(self) -> float:
        average_close = self._average_price(self._close_orders)

        if self.operation() == "-":
            average_close *= -1

        return average_close

    def nominal_pl(self) -> float:
        return (self.average_close() + self.average_open()) / abs(self.average_open())

    def leveraged_pl(self) -> float:
        return self.nominal_pl() * self.leverage()

    def to_entity(self) -> Dict[str, str]:
        return {
            "symbol":        self.symbol(),
            "operation":     self.operation(),
            "leverage":      f"{self.leverage()}",
            "open_time":     self.open_time().strftime("%Y%m%d"),
            "close_time":    self.close_time().strftime("%y%m%d"),
            "average_open":  f"{self.average_open()}",
            "average_close": f"{self.average_close()}",
            "nominal_pl":    f"{self.nominal_pl() * 100.0:.{self._float_decimals}f}%",
            "leveraged_pl":  f"{self.leveraged_pl() * 100.0:.{self._float_decimals}f}%",
        }
