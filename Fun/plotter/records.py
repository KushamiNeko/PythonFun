from datetime import timedelta
from typing import List, Optional, Tuple
from datetime import datetime
import numpy as np
import pandas as pd
from Fun.data.source import FREQUENCY, WEEKLY, DAILY
from Fun.plotter.plotter import TextPlotter
from Fun.trading.transaction import FuturesTransaction
from Fun.trading.agent import TradingAgent
from Fun.utils import colors
from matplotlib import axes, font_manager as fm


class LeverageRecords(TextPlotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        # records: List[FuturesTransaction],
        book_title: str,
        agent: TradingAgent,
        flip_position: bool = False,
        font_color: str = "w",
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._quotes = quotes
        self._frequency = frequency

        # self._records = records
        self._records = agent.read_records(title=book_title)

        self._flip_position = flip_position

    def plot(self, ax: axes.Axes) -> None:
        if len(self._quotes) == 0:
            return

        if self._records is None or len(self._records) == 0:
            return

        assert ax is not None

        if self._frequency != DAILY and self._frequency != WEEKLY:
            return

        dates = self._quotes.index
        ops = np.add.accumulate(
            [float(f"{r.operation()}{r.leverage()}") for r in self._records]
        )

        ops_s = -1
        ops_e = -1

        loc = []
        for i, r in enumerate(self._records):
            tar = r.datetime()
            if self._frequency == WEEKLY:
                tar = tar - timedelta(days=tar.weekday())

            if ops_s == -1 and tar >= dates[0]:
                ops_s = i
            if ops_e == -1 and tar > dates[-1]:
                ops_e = i

            where = np.argwhere(dates == tar).flatten()
            if where.size != 0:
                loc.append(where.min())

        if ops_s == -1:
            return

        if ops_e == -1:
            ops_e = len(self._records)

        ops = ops[ops_s:ops_e]

        if len(ops) == 0:
            return

        loc = np.array(loc)

        unique, count = np.unique(loc, return_counts=True)
        labels = np.where(
            ops == 0,
            "X",
            np.vectorize(lambda v: f"{v[0].strip()}\n{v[1:].strip()}")(
                np.vectorize(lambda v: f"L{abs(v):.0f}" if v > 0 else f"S{abs(v):.0f}")(
                    ops
                )
            ),
        )

        highs = self._quotes.loc[:, "high"]
        lows = self._quotes.loc[:, "low"]

        mx = highs.max()
        mn = lows.min()
        mr = mx - mn

        middle = (mx + mn) / 2.0

        offset = mr * 0.0075

        for x in unique:
            h = highs.iloc[x]
            l = lows.iloc[x]
            m = (h + l) / 2.0

            va = "top" if m > middle else "bottom"
            if self._flip_position:
                va = "bottom" if va == "top" else "top"

            # y = l - offset if m > middle else h + offset
            y = l - offset if va == "top" else h + offset

            text = "\n".join([labels[j] for j in np.argwhere(loc == x).flatten()])

            ax.text(
                x,
                y,
                text,
                color=self._font_color,
                fontproperties=self._font_properties,
                ha="center",
                va=va,
            )


# class LongShortLeverageRecords(TextPlotter):
class TradingHedgingLeverageRecords(TextPlotter):
    def __init__(
        self,
        dtime: datetime,
        virtual_close: float,
        quotes: pd.DataFrame,
        frequency: FREQUENCY,
        trading_book_title: str,
        hedging_book_title: str,
        agent: TradingAgent,
        trading_font_color: str = "#ffffff",
        hedging_font_color: str = colors.PAPER_DEEP_PURPLE_A100,
        font_size: float = 10.0,
        font_src: Optional[str] = None,
        font_properties: Optional[fm.FontProperties] = None,
        info_font_color: str = "w",
        info_font_size: float = 10.0,
        info_font_src: Optional[str] = None,
        info_font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        assert quotes is not None

        super().__init__(
            font_color=trading_font_color,
            font_size=font_size,
            font_src=font_src,
            font_properties=font_properties,
        )

        self._font_size = font_size
        self._font_src = font_src

        self._trading_font_color = trading_font_color
        self._hedging_font_color = hedging_font_color

        self._info_font_color = info_font_color
        self._info_font_size = info_font_size
        self._info_font_src = info_font_src

        if info_font_properties is None:
            if info_font_src is None:
                self._info_font_properties = fm.FontProperties(size=font_size)
            else:
                self._info_font_properties = fm.FontProperties(
                    fname=info_font_src, size=info_font_size
                )
        else:
            self._info_font_properties = info_font_properties

        self._dtime = dtime
        self._virtual_close = virtual_close
        self._quotes = quotes
        self._frequency = frequency

        self._trading_book_title = trading_book_title
        self._hedging_book_title = hedging_book_title

        self._agent = agent

    def plot(self, ax: axes.Axes) -> None:
        trading_leverage = self._agent.open_positions_leverage(
            title=self._trading_book_title, dtime=self._dtime
        )

        trading_operation = self._agent.open_positions_operation(
            title=self._trading_book_title, dtime=self._dtime
        )

        trading_virtual_pl = self._agent.open_positions_virtual_pl(
            title=self._trading_book_title,
            dtime=self._dtime,
            virtual_close=self._virtual_close,
        )

        plotter = LeverageRecords(
            quotes=self._quotes,
            frequency=self._frequency,
            book_title=self._trading_book_title,
            agent=self._agent,
            font_color=self._trading_font_color,
            font_size=self._font_size,
            font_src=self._font_src,
            font_properties=self._font_properties,
        )

        plotter.plot(ax)

        hedging_leverage = self._agent.open_positions_leverage(
            title=self._hedging_book_title,
            dtime=self._dtime,
        )

        hedging_operation = self._agent.open_positions_operation(
            title=self._hedging_book_title, dtime=self._dtime
        )

        hedging_virtual_pl = self._agent.open_positions_virtual_pl(
            title=self._hedging_book_title,
            dtime=self._dtime,
            virtual_close=self._virtual_close,
        )

        plotter = LeverageRecords(
            quotes=self._quotes,
            frequency=self._frequency,
            book_title=self._hedging_book_title,
            agent=self._agent,
            flip_position=True,
            font_color=self._hedging_font_color,
            font_size=self._font_size,
            font_src=self._font_src,
            font_properties=self._font_properties,
        )

        plotter.plot(ax)

        trading_leverage = trading_leverage if trading_leverage is not None else 0
        hedging_leverage = hedging_leverage if hedging_leverage is not None else 0

        trading_operation = trading_operation if trading_operation is not None else ""
        hedging_operation = hedging_operation if hedging_operation is not None else ""

        nominal_trading_vpl = (
            trading_virtual_pl[0] if trading_virtual_pl is not None else 0
        )
        leveraged_trading_vpl = (
            trading_virtual_pl[1] if trading_virtual_pl is not None else 0
        )

        nominal_hedging_vpl = (
            hedging_virtual_pl[0] if hedging_virtual_pl is not None else 0
        )
        leveraged_hedging_vpl = (
            hedging_virtual_pl[1] if hedging_virtual_pl is not None else 0
        )

        nominal_balance = nominal_trading_vpl + nominal_hedging_vpl
        leveraged_balance = leveraged_trading_vpl + leveraged_hedging_vpl

        text = "\n".join(
            [
                "Trading : Hedging",
                "==============",
                f"{trading_operation}{trading_leverage}  :  {hedging_operation}{hedging_leverage}",
                "==============",
                f"{nominal_trading_vpl: .2f}%  :  {nominal_hedging_vpl: .2f}%",
                f"{leveraged_trading_vpl: .2f}%  :  {leveraged_hedging_vpl: .2f}%",
                "==============",
                f"{nominal_balance: .2f}%",
                f"{leveraged_balance: .2f}%",
            ]
        )

        length = len(self._quotes.index)
        start = (length // 2) - ((length // 12) // 2)
        end = (length // 2) + ((length // 12) // 2)

        lh = np.amax(self._quotes.iloc[start:end].loc[:, "high"])
        ll = np.amin(self._quotes.iloc[start:end].loc[:, "low"])

        mn, mx = ax.get_ylim()

        y = mn
        va = "bottom"
        if (mx - lh) > (ll - mn):
            y = mx
            va = "top"

        ax.text(
            len(self._quotes.index) // 2,
            y,
            # ax.get_ylim()[0],
            text,
            color=self._info_font_color,
            fontproperties=self._info_font_properties,
            ha="center",
            va=va,
            # va="bottom",
        )
