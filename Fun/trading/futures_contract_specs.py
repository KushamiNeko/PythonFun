from __future__ import annotations

from typing import Dict


class FuturesContractSpecs:
    _ts_symbols_book: Dict[str, str] = {
        "es":  "es",
        "ym":  "ym",
        "nq":  "nq",
        "rty": "rty",
        "nk":  "nyd",
        "us":  "zb",
        "ty":  "zn",
        "fv":  "zf",
        "tu":  "zt",
        "ed":  "ge",
        "ec":  "6e",
        "jy":  "6j",
        "bp":  "6b",
        "ad":  "6a",
        "cd":  "6c",
        "sf":  "6s",
        "mp1": "6m",
        "ne1": "6n",
        "gc":  "gc",
        "si":  "si",
        "hg":  "hg",
        "pl":  "pl",
        "cl":  "cl",
        "ng":  "ng",
        "rb":  "rb",
        "ho":  "ho",
        "s":   "zs",
        "w":   "zw",
        "c":   "zc",
        "bo":  "zl",
        "sm":  "zm",
        "lc":  "le",
        "lh":  "he",
        "fc":  "gf",
    }

    _ibkr_symbols_book: Dict[str, str] = {}

    _contract_unit = {
        "es":  50.0,
        "ym":  5.0,
        "nq":  20.0,
        "rty": 50.0,
        "nyd": 5.0,
        "zb":  1000.0,
        "zn":  1000.0,
        "zf":  1000.0,
        "zt":  1000.0,
        "ge":  2500.0,
        "6e":  125000.0,
        "6j":  12500000.0,
        "6a":  100000.0,
        "6b":  62500.0,
        "6c":  100000.0,
        "6s":  125000.0,
        "6n":  100000.0,
        "6m":  500000.0,
        "gc":  100.0,
        "si":  5000.0,
        "hg":  25000.0,
        "pl":  50.0,
        "cl":  1000.0,
        "rb":  42000.0,
        "ng":  10000.0,
        "ho":  42000.0,
        "zs":  5000.0,
        "zc":  5000.0,
        "zw":  5000.0,
        "zl":  60000.0,
        "zm":  100.0,
        "le":  40000.0,
        "he":  40000.0,
        "gf":  50000.0,
    }

    @classmethod
    def _lookup_symbol(cls, symbol: str, broker: str) -> str:
        if broker == "TradeStation":
            return cls._ts_symbols_book[symbol]
        elif broker == "InteractiveBroker":
            return cls._ibkr_symbols_book[symbol]
        else:
            raise ValueError(f"unknown broker: {broker}")

    @classmethod
    def lookup_contract_unit(cls, symbol: str, broker: str = "TradeStation") -> float:
        contract_unit = cls._contract_unit.get(symbol, None)
        if contract_unit:
            return contract_unit
        else:
            cme_symbol = cls._lookup_symbol(symbol, broker=broker)
            return cls._contract_unit[cme_symbol]

    @classmethod
    def validate_symbol(cls, symbol: str, broker: str = "TradeStation") -> bool:
        if broker == "TradeStation":
            books = cls._ts_symbols_book
        elif broker == "InteractiveBroker":
            books = cls._ibkr_symbols_book
        else:
            raise ValueError(f"unknown broker: {broker}")

        if symbol not in books.keys() and symbol not in books.values():
            return False
        else:
            return True
