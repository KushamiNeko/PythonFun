from __future__ import annotations

import re
from typing import Dict


class TransactionOrder:
    def __init__(
        # self, symbol: str, operation: str, leverage: float, price: float,
        self,
        symbol: str,
        account: str,
        operation: str,
        leverage: float,
        price: float,
    ) -> None:

        if not re.match(r"^[a-zA-Z]+$", symbol):
            raise ValueError("invalid transaction symbol")
        self._symbol = symbol.lower()

        if not re.match(r"^(?:trading|hedging)$", account):
            raise ValueError("invalid transaction account")
        self._account = account

        if not re.match(r"^[+-]$", operation):
            raise ValueError("invalid transaction operation")
        self._operation = operation

        if leverage <= 0:
            raise ValueError("invalid transaction leverage")
        self._leverage = leverage

        if price <= 0.0:
            raise ValueError("invalid transaction price")
        self._price = price

    def symbol(self) -> str:
        return self._symbol

    def account(self) -> str:
        return self._account

    def operation(self) -> str:
        return self._operation

    def leverage(self) -> float:
        return self._leverage

    def price(self) -> float:
        return self._price

    def to_entity(self) -> Dict[str, str]:
        return {
            "symbol": self._symbol,
            "account": self._account,
            "operation": self._operation,
            "leverage": f"{self._leverage}",
            "price": f"{self._price}",
        }

    @classmethod
    def from_entity(cls, entity: Dict[str, str]) -> TransactionOrder:
        return TransactionOrder(
            symbol=entity["symbol"],
            account=entity["account"],
            operation=entity["operation"],
            leverage=float(entity["leverage"]),
            price=float(entity["price"]),
        )
