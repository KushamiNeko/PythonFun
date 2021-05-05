from __future__ import annotations

import re
from datetime import datetime
from typing import List, NewType, Tuple

import pandas as pd
from fun.data.barchart import BarchartContract, Barchart
from fun.data.source import DAILY, DataSource, FREQUENCY
from fun.utils import colors, pretty

CONTRACT_MONTHS = NewType("CONTRACT_MONTHS", str)

CONTRACT_MONTHS_REGEX = "^[fghjkmnquvxz]+$"

ALL_CONTRACT_MONTHS = CONTRACT_MONTHS("fghjkmnquvxz")
ODD_CONTRACT_MONTHS = CONTRACT_MONTHS("fhknux")
EVEN_CONTRACT_MONTHS = CONTRACT_MONTHS("gjmqvz")
FINANCIAL_CONTRACT_MONTHS = CONTRACT_MONTHS("hmuz")

# SOYBEAN_CONTRACT_MONTHS = CONTRACT_MONTHS("fhknqux")
# CORN_WHEAT_CONTRACT_MONTHS = CONTRACT_MONTHS("hknuz")
# SILVER_COPPER_CONTRACT_MONTHS = CONTRACT_MONTHS("hknuz")


CODE_FORMAT = NewType("CODE_FORMAT", int)
BARCHART = CODE_FORMAT(0)
QUANDL = CODE_FORMAT(1)


class Contract:
    _barchart_format: str = r"^(\w{2})([fghjkmnquvxz])(\d{2})$"
    _quandl_format: str = r"^([\d\w]+)([fghjkmnquvxz])(\d{4})$"

    @classmethod
    def _front_month_search(
        cls,
        months: CONTRACT_MONTHS,
        time: datetime,
    ) -> Tuple[int, str]:

        contract_now = time.year * 100 + time.month

        for y in range(time.year, time.year + 2):
            for cm in months:
                m = month_from_futures_month_code(cm)

                contract = y * 100 + m

                if contract > contract_now:
                    front_year = y
                    front_month = cm

                    return front_year, front_month

        raise AssertionError("impossible situation")

    @classmethod
    def front_month(
        cls,
        symbol: str,
        months: CONTRACT_MONTHS,
        fmt: CODE_FORMAT = BARCHART,
        read_data: bool = True,
        src: Barchart = BarchartContract(),
        frequency: FREQUENCY = DAILY,
        time: datetime = datetime.now(),
    ) -> Contract:
        assert fmt in (BARCHART, QUANDL)
        assert re.match(CONTRACT_MONTHS_REGEX, months) is not None
        # assert months in (
        # ALL_CONTRACT_MONTHS,
        # EVEN_CONTRACT_MONTHS,
        # FINANCIAL_CONTRACT_MONTHS,
        # )

        front_year = 0
        front_month = ""

        front_year, front_month = cls._front_month_search(months, time)

        # front_year = time.year

        # front_month = ""
        # if months == FINANCIAL_CONTRACT_MONTHS:
        #    offset = time.month
        # else:
        #    offset = time.month + 2

        # if offset >= 12:
        #    offset %= 12
        #    front_year += 1

        # for m in months:
        #    if month_from_futures_month_code(m) > offset:
        #        front_month = m
        #        break

        assert front_year != 0
        assert front_month != ""

        year_code = ""
        if fmt == BARCHART:
            front_year %= 100
            year_code = f"{front_year:02}"
        elif fmt == QUANDL:
            year_code = f"{front_year:04}"
        else:
            raise ValueError("invalid code format")

        assert year_code != ""

        c = Contract(
            code=f"{symbol}{front_month}{year_code}",
            fmt=fmt,
            months=months,
            read_data=read_data,
            src=src,
            frequency=frequency,
        )

        if symbol in ("zn", "zf", "zt", "zb", "ge", "gg", "tj"):
            # c = c.next_contract()
            pass
        elif symbol in ("cl",):
            c = c.next_contract()

        return c

    def __init__(
        self,
        code: str,
        months: CONTRACT_MONTHS,
        fmt: CODE_FORMAT = BARCHART,
        read_data: bool = True,
        src: DataSource = BarchartContract(),
        frequency: FREQUENCY = DAILY,
    ) -> None:

        assert fmt in (BARCHART, QUANDL)
        assert re.match(CONTRACT_MONTHS_REGEX, months) is not None
        # assert months in (
        # ALL_CONTRACT_MONTHS,
        # EVEN_CONTRACT_MONTHS,
        # FINANCIAL_CONTRACT_MONTHS,
        # )

        self._fmt = fmt
        self._months = months
        self._code = code

        self._src = src
        self._frequency = frequency

        symbol = ""
        year = 0
        month = 0

        match = None

        if self._fmt == BARCHART:
            match = re.match(self._barchart_format, self._code)
            if match is None:
                raise ValueError(
                    f"invalid contract code {self._code} for {self._fmt} format"
                )

            year = int(f"20{match.group(3)}")

        elif self._fmt == QUANDL:
            match = re.match(self._quandl_format, self._code)
            if match is None:
                raise ValueError(
                    f"invalid contract code {self._code} for {self._fmt} format"
                )

            year = int(match.group(3))

        else:
            raise ValueError("unknown contract code format: {self._fmt}")

        assert match is not None

        symbol = match.group(1)
        month = month_from_futures_month_code(match.group(2))

        assert symbol != ""
        assert year != 0
        assert month != 0

        if year > datetime.now().year + 1:
            year -= 100

        self._symbol = symbol
        self._year = year
        self._month = month

        if read_data:
            self.read_data()

    # def read_data(self, src=BarchartContract()) -> None:
    def read_data(self) -> None:
        self._df = self._src.read(
            start=datetime(1776, 7, 4),
            end=datetime.now(),
            symbol=self._code,
            frequency=self._frequency,
        )

        assert self._df is not None

    def code(self) -> str:
        return self._code

    def symbol(self) -> str:
        return self._symbol

    def year(self) -> int:
        return self._year

    def month(self) -> int:
        return self._month

    def dataframe(self) -> pd.DataFrame:
        assert self._df is not None
        return self._df

    def previous_contract(self, read_data: bool = True) -> Contract:
        p_year = self.year()
        mi = self._months.index(month_to_futures_month_code(self._month))
        if mi - 1 < 0:
            p_year -= 1

        p_month = month_from_futures_month_code(
            self._months[mi - 1 % len(self._months)]
        )

        year_code = ""
        if self._fmt == BARCHART:
            p_year %= 100
            year_code = f"{p_year:02}"
        elif self._fmt == QUANDL:
            year_code = f"{p_year:04}"
        else:
            raise ValueError("invalid code format")

        return Contract(
            code=f"{self._symbol}{month_to_futures_month_code(p_month)}{year_code}",
            months=self._months,
            fmt=self._fmt,
            read_data=read_data,
            src=self._src,
            frequency=self._frequency,
        )

    def next_contract(self, read_data: bool = True) -> Contract:
        year = self.year()
        month = self.month()

        c = year * 100 + month

        for y in range(year, year + 2):
            for cm in self._months:
                m = month_from_futures_month_code(cm)

                contract = y * 100 + m

                if contract > c:

                    year_code = ""
                    if self._fmt == BARCHART:
                        y %= 100
                        year_code = f"{y:02}"
                    elif self._fmt == QUANDL:
                        year_code = f"{y:04}"
                    else:
                        raise ValueError("invalid code format")

                    return Contract(
                        code=f"{self._symbol}{cm}{year_code}",
                        months=self._months,
                        fmt=self._fmt,
                        read_data=read_data,
                        src=self._src,
                        frequency=self._frequency,
                    )

        raise AssertionError("impossible situation")


def month_to_futures_month_code(month: int) -> str:
    if month == 1:
        return "f"
    elif month == 2:
        return "g"
    elif month == 3:
        return "h"
    elif month == 4:
        return "j"
    elif month == 5:
        return "k"
    elif month == 6:
        return "m"
    elif month == 7:
        return "n"
    elif month == 8:
        return "q"
    elif month == 9:
        return "u"
    elif month == 10:
        return "v"
    elif month == 11:
        return "x"
    elif month == 12:
        return "z"
    else:
        raise ValueError(f"unknown month: {month}")


def month_from_futures_month_code(code: str) -> int:
    if code == "f":
        return 1
    elif code == "g":
        return 2
    elif code == "h":
        return 3
    elif code == "j":
        return 4
    elif code == "k":
        return 5
    elif code == "m":
        return 6
    elif code == "n":
        return 7
    elif code == "q":
        return 8
    elif code == "u":
        return 9
    elif code == "v":
        return 10
    elif code == "x":
        return 11
    elif code == "z":
        return 12
    else:
        raise ValueError(f"unknonw month code: {code}")


def contract_list(
    start: datetime,
    end: datetime,
    symbol: str,
    months: CONTRACT_MONTHS,
    fmt: CODE_FORMAT,
    read_data: bool = True,
    src: DataSource = BarchartContract(),
    frequency: FREQUENCY = DAILY,
) -> List[Contract]:
    try:
        cur = Contract.front_month(
            symbol=symbol,
            months=months,
            fmt=fmt,
            time=end,
            read_data=read_data,
            src=src,
            frequency=frequency,
        )
    except FileNotFoundError:
        msg = "empty contract list"
        pretty.color_print(colors.PAPER_AMBER_300, msg)
        raise ValueError(msg)

    contracts = [cur]
    while not (
        (cur.year() * 10000 + cur.month() * 100)
        < (start.year * 10000 + start.month * 100)
    ):

        try:
            cur = cur.previous_contract(read_data=read_data)
            contracts.append(cur)
        except FileNotFoundError as err:
            pretty.color_print(colors.PAPER_AMBER_300, str(err))
            break

    assert len(contracts) != 0

    return contracts
