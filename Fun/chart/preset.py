import io
import os
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, cast

import pandas as pd

from Fun.chart.base import CHART_SIZE, MEDIUM_CHART
from Fun.chart.cache import QuotesCache
from Fun.chart.setting import Setting
from Fun.chart.static import TradingChart
from Fun.chart.theme import MagicalTheme, Theme
from Fun.data.barchart import Barchart
from Fun.data.source import (
    DAILY,
    FREQUENCY,
    INTRADAY_15MINUTES,
    INTRADAY_30MINUTES,
    INTRADAY_60MINUTES,
    MONTHLY,
    WEEKLY,
    CoinAPI,
    DataSource,
    InvestingCom,
    StockCharts,
    Yahoo,
)
from Fun.futures.continuous import ContinuousContract
from Fun.plotter.advance_decline import AdvanceDeclineLine
from Fun.plotter.background import BackgroundTimeRangeMark
from Fun.plotter.candlesticks import CandleSticks
from Fun.plotter.entry import EntryZone
from Fun.plotter.equal_weighted import EqualWeightedRelativeStrength
from Fun.plotter.ibd import DistributionsDay
from Fun.plotter.indicator import (
    BollingerBand,
    SimpleMovingAverage,
    ExponentialMovingAverage,
    ExponentialMovingAverageEnvelope,
)
from Fun.plotter.level import Level
from Fun.plotter.plotter import Plotter
from Fun.plotter.quote import LastQuote
from Fun.plotter.rates import InterestRatesSummary
from Fun.plotter.study import NoteMarker, StudyZone, read_notes
from Fun.plotter.volatility import VolatilityRealBodyContraction, VolatilitySummary
from Fun.plotter.volume import Volume
from Fun.plotter.zone import VolatilityZone


class CandleSticksPreset:
    def __init__(
        self,
        dtime: datetime,
        symbol: str,
        frequency: FREQUENCY,
        chart_range: Optional[str] = None,
        chart_size: CHART_SIZE = MEDIUM_CHART,
    ) -> None:
        assert re.match(r"^[a-zA-Z0-9]+$", symbol) is not None

        self._symbol = symbol

        assert frequency in (
            INTRADAY_15MINUTES,
            INTRADAY_30MINUTES,
            INTRADAY_60MINUTES,
            DAILY,
            WEEKLY,
            MONTHLY,
        )

        self._frequency = frequency

        self._chart_range = chart_range

        self._stime, self._etime = self._time_range(dtime)
        self._exstime, self._exetime = self._extime_range()

        self._frequency = frequency

        self._chart_size = chart_size
        self._cache = self._read_chart_data()

        self._theme = None
        self._setting = None

        self._controller = None
        self._chart = None

    def _time_range(self, dtime: datetime) -> Tuple[datetime, datetime]:

        etime = dtime
        stime: datetime

        if self._chart_range is not None:
            regex = re.compile(r"^(\d+)([dmy])$")
            match = regex.findall(self._chart_range.lower())

            num = int(match[0][0])
            unit = match[0][1]

            days = -1
            if unit == "d":
                days = 1
            if unit == "w":
                days = 7
            if unit == "m":
                days = 31
            elif unit == "y":
                days = 365

            assert days > 0

            total_days = days * num

            if self._frequency == INTRADAY_15MINUTES and (
                total_days < 1 or total_days > 1
            ):
                total_days = 1
                self._chart_range = "1D"

            elif self._frequency == INTRADAY_30MINUTES and (
                total_days < 2 or total_days > 6
            ):
                total_days = 2
                self._chart_range = "2D"

            elif self._frequency == INTRADAY_60MINUTES and (
                total_days < 6 or total_days > 16
            ):
                total_days = 7
                self._chart_range = "7D"

            elif self._frequency == DAILY and (total_days < 90 or total_days > 365):
                total_days = 31 * 6
                self._chart_range = "6M"

            elif self._frequency == WEEKLY and (
                total_days < 365 * 2 or total_days > 365 * 5
            ):
                total_days = 365 * 3
                self._chart_range = "3Y"

            elif self._frequency == MONTHLY and (
                total_days < 365 * 10 or total_days > 365 * 20
            ):
                total_days = 365 * 12
                self._chart_range = "12Y"

            stime = etime - timedelta(days=total_days)

        else:
            if self._frequency == INTRADAY_15MINUTES:
                stime = etime - timedelta(days=1)
                self._chart_range = "1D"

            elif self._frequency == INTRADAY_30MINUTES:
                stime = etime - timedelta(days=2)
                self._chart_range = "2D"

            elif self._frequency == INTRADAY_60MINUTES:
                stime = etime - timedelta(days=7)
                self._chart_range = "7D"

            elif self._frequency == DAILY:
                stime = etime - timedelta(days=31 * 6)
                self._chart_range = "6M"

            elif self._frequency == WEEKLY:
                stime = etime - timedelta(days=365 * 3)
                self._chart_range = "3Y"

            elif self._frequency == MONTHLY:
                stime = etime - timedelta(days=365 * 12)
                self._chart_range = "12Y"

            else:
                raise ValueError("invalid frequency")

        if (
            self._frequency == INTRADAY_15MINUTES
            or self._frequency == INTRADAY_30MINUTES
            or self._frequency == INTRADAY_60MINUTES
        ):
            etime = etime.replace(hour=16)

        return stime, etime

    def _extime_range(self) -> Tuple[datetime, datetime]:
        exetime = self._etime + timedelta(days=500)
        exstime = self._stime - timedelta(days=500)

        now = datetime.now()
        if exetime > now:
            exetime = now

        return exstime, exetime

    def _read_chart_data(self) -> QuotesCache:
        print("network")

        src: Optional[DataSource] = None

        if self._symbol in ("vix", "vxn", "ovx", "gvz"):
            src = Yahoo()

        elif self._symbol in ("rut", "sml", "dji"):
            src = Yahoo()

        elif self._symbol in (
            # "vstx",
            "jniv",
            "vhsi",
            "vxfxi",
            "nk400",
        ):
            src = InvestingCom()

        elif self._symbol in (
            # "usd",
            "vstx",
            "dxy",
            "jpyusd",
            "usdjpy",
            "eurusd",
            "gbpusd",
            "chfusd",
            "usdchf",
            "audusd",
            "cadusd",
            "usdcad",
            "nzdusd",
            "eurjpy",
            "eurgbp",
            "euraud",
            "eurcad",
            "eurchf",
            "gbpjpy",
            "audjpy",
            "cadjpy",
            "nzdjpy",
        ):
            src = Barchart()

        elif self._symbol in (
            "btcusd",
            "ethusd",
            "ltcusd",
            "xrpusd",
            "bchusd",
            "usdcusd",
        ):
            src = CoinAPI()

        elif self._symbol in (
            "linkusd",
            "adausd",
            "dotusd",
            "xlmusd",
            "eosusd",
            "trxusd",
            "uniusd",
        ):
            src = CoinAPI()

        elif self._symbol in ("vle", "rvx", "tyvix"):
            src = StockCharts()

        elif self._symbol in (
            "spx",
            "ndx",
            "compq",
            "nya",
            "nikk",
            "ezu",
            "eem",
            "hsi",
            "fxi",
            "ndxew",
        ):
            src = Yahoo()

        elif self._symbol in (
            "spxew",
            "smlew",
            "midew",
            "topix",
        ):
            src = Barchart()

        elif self._symbol in (
            "icsh",
            "jpst",
            "gsy",
            "near",
            "shv",
            "flot",
            "hylb",
            "ushy",
            "faln",
            "shyg",
            "hyg",
            "sjnk",
            "jnk",
            "bkln",
            "srln",
            "emb",
            "pcy",
            "emhy",
            "lqd",
            "mbb",
            "mub",
            "igsb",
            "igib",
            "shy",
            "iei",
            "ief",
            "tlh",
            "tlt",
            "govt",
            "iyr",
            "reet",
            "rem",
        ):
            # src = AlphaVantage()
            src = Yahoo()

        elif self._symbol in (
            "pff",
            "pgx",
            "pgf",
            "hdv",
            "dvy",
            "dvye",
            "idv",
            "spyd",
            "sphd",
            "schd",
            "vym",
            "sdy",
            "dgro",
        ):
            src = Yahoo()

        elif self._symbol in (
            "fedfunds",
            "ustm1",
            "ustm3",
            "ustm6",
            "usty2",
            "usty5",
            "usty10",
            "usty30",
        ):
            src = Barchart()

        df: pd.DataFrame
        if src is None:
            df = ContinuousContract().read(
                start=self._exstime,
                end=self._exetime,
                symbol=self._symbol,
                frequency=self._frequency,
            )
        else:
            # if type(src) is not CoinAPI:
            assert self._frequency in (DAILY, WEEKLY, MONTHLY)

            df = src.read(
                start=self._exstime,
                end=self._exetime,
                symbol=self._symbol,
                frequency=self._frequency,
            )

        assert df is not None

        cache = QuotesCache(df, self._stime, self._etime, minimum_bars=130)
        return cache

    def _read_note(self, dt: str) -> Optional[str]:

        root = os.path.join(
            os.getenv("HOME"),
            "Documents",
            "TRADING_NOTES",
            "notes",
        )

        notes_root = None
        for r in os.listdir(root):
            pattern = r"[&_,|]"

            targets = re.split(pattern, r)
            targets = list(map(lambda x: x.strip(), targets))

            if self._symbol.lower() in targets:
                path = os.path.join(root, r)
                if os.path.exists(path):
                    notes_root = path
                break

        if notes_root is None:
            return None

        notes = ["\n"]
        max_lenght = 0

        def append_notes(filename, note_dt, pattern, content):
            nonlocal notes
            nonlocal max_lenght
            nonlocal dt

            if dt == note_dt.strftime("%Y%m%dT%H:%M"):
                for c in content.split("\n"):
                    lc = len(c.strip())
                    max_lenght = max(lc, max_lenght)

                notes.append(f"{filename.replace('.txt', '')}\n\n{content.strip()}")

                return True

        read_notes(
            notes_root,
            self._frequency,
            lambda filename, note_dt, pattern, content: append_notes(
                filename=filename,
                note_dt=note_dt,
                pattern=pattern,
                content=content,
            ),
        )

        if len(notes) > 0:
            notes.append("\n")
            return f"\n\n{'='*max_lenght}\n\n".join(notes).strip()

        return None

    def cache(self) -> QuotesCache:
        return self._cache

    def full_quotes(self) -> pd.DataFrame:
        return self._cache.full_quotes()

    def quotes(self) -> pd.DataFrame:
        return self._cache.quotes()

    def chart_range(self) -> str:
        return self._chart_range if self._chart_range is not None else ""

    def theme(self) -> Theme:
        assert self._theme is not None
        return self._theme

    def setting(self) -> Setting:
        assert self._setting is not None
        return self._setting

    def last_quote(self) -> Dict[str, Any]:
        df = self._cache.quotes().iloc[-1]
        return {
            "date": self._cache.quotes().index[-1].strftime("%Y%m%d"),
            "time": self._cache.quotes().index[-1].strftime("%H:%M"),
            "open": df.get("open"),
            "high": df.get("high"),
            "low": df.get("low"),
            "close": df.get("close"),
            "volume": df.get("volume", 0),
            "interest": df.get("open interest", 0),
        }

    def time_slice(self, dtime: datetime, chart_range: Optional[str] = None) -> None:
        if chart_range is not None:
            self._chart_range = chart_range

        stime, etime = self._time_range(dtime)

        if (
            stime <= self._exstime
            or stime >= self._exetime
            or etime <= self._exstime
            or etime >= self._exetime
        ):
            self._stime = stime
            self._etime = etime
            self._exstime, self._exetime = self._extime_range()
            self._cache = self._read_chart_data()
        else:
            self._cache.time_slice(stime, etime)

    def stime(self) -> datetime:
        return cast(datetime, self._cache.stime().to_pydatetime())

    def etime(self) -> datetime:
        return cast(datetime, self._cache.etime().to_pydatetime())

    def exstime(self) -> datetime:
        return cast(datetime, self._cache.exstime().to_pydatetime())

    def exetime(self) -> datetime:
        return cast(datetime, self._cache.exetime().to_pydatetime())

    def forward(self) -> bool:
        return self._cache.forward()

    def backward(self) -> bool:
        return self._cache.backward()

    def make_controller(
        self,
        parameters: Optional[Dict[str, str]],
        preset_key: str = "Preset",
    ) -> None:
        if parameters is None:
            self._controller = KushamiNekoController(
                cache=self._cache,
                symbol=self._symbol,
                frequency=self._frequency,
                chart_size=self._chart_size,
                parameters=parameters,
            )

            self._theme = self._controller.get_theme()
            self._setting = self._controller.get_setting()

            return

        preset = parameters.get(preset_key, "").strip()
        if preset == "" or preset == "KushamiNeko":
            self._controller = KushamiNekoController(
                cache=self._cache,
                symbol=self._symbol,
                frequency=self._frequency,
                chart_size=self._chart_size,
                parameters=parameters,
            )
        elif preset == "Magical":
            self._controller = MagicalController(
                cache=self._cache,
                symbol=self._symbol,
                frequency=self._frequency,
                chart_size=self._chart_size,
                parameters=parameters,
            )

        assert self._controller is not None

        self._theme = self._controller.get_theme()
        self._setting = self._controller.get_setting()

    def render(self, additional_plotters: Optional[List[Plotter]] = None) -> io.BytesIO:
        buf = io.BytesIO()

        plotters = []

        if self._controller is None:
            self.make_controller(parameters={"MovingAverages": "true"})

        assert self._controller is not None

        plotters.extend(self._controller.get_plotters())

        if additional_plotters is not None and len(additional_plotters) > 0:
            plotters.extend(additional_plotters)

        self._chart = TradingChart(
            quotes=self._cache.quotes(),
            theme=self._theme,
            setting=self._setting,
        )

        self._chart.render(buf, plotters=plotters)

        buf.seek(0)

        return buf

    def inspect(
        self,
        x: float,
        y: float,
        ax: Optional[float] = None,
        ay: Optional[float] = None,
        quote_decimals: int = 5,
        diff_decimals: int = 3,
    ) -> Tuple[Optional[Dict[str, str]], Optional[str]]:

        if self._chart is None:
            return None, None

        n = self._chart.to_data_coordinates(x, y)

        if n is None:
            return None, None

        nx, ny = n

        df = self._cache.quotes()

        info = {
            "CST D": self._cache.quotes().index[nx].strftime("%Y-%m-%d"),
        }

        ja = self._cache.quotes().index[nx]

        if (
            self._frequency == INTRADAY_15MINUTES
            or self._frequency == INTRADAY_30MINUTES
            or self._frequency == INTRADAY_60MINUTES
        ):
            info["CST T"] = self._cache.quotes().index[nx].strftime("%H:%M")

            offset = 6

            gmt = self._cache.quotes().index[nx] + timedelta(hours=offset)
            info["GMT D"] = gmt.strftime("%Y-%m-%d")
            info["GMT T"] = gmt.strftime("%H:%M")

            offset = 15
            if self._cache.quotes().index[nx].month in range(3, 11):
                offset = 14

            jst = self._cache.quotes().index[nx] + timedelta(hours=offset)
            info["JST D"] = jst.strftime("%Y-%m-%d")
            info["JST T"] = jst.strftime("%H:%M")

            info[""] = ""

        info["Price"] = f"{ny:,.{quote_decimals}f}"
        info["Open"] = f"{df.iloc[nx].get('open'):,.{quote_decimals}f}"
        info["High"] = f"{df.iloc[nx].get('high'):,.{quote_decimals}f}"
        info["Low"] = f"{df.iloc[nx].get('low'):,.{quote_decimals}f}"
        info["Close"] = f"{df.iloc[nx].get('close'):,.{quote_decimals}f}"
        info["Volume"] = f"{df.iloc[nx].get('volume', 0):,.0f}"
        info["Interest"] = f"{df.iloc[nx].get('open interest', 0):,.0f}"

        note = self._read_note(self._cache.quotes().index[nx].strftime("%Y%m%dT%H:%M"))

        if ax is None or ay is None:
            if nx != 0:
                base = self._cache.quotes().iloc[nx - 1].get("close")
                info[
                    "Diff($)"
                ] = f"{df.iloc[nx].get('close') - base:,.{quote_decimals}f}"

                info[
                    "Diff(%)"
                ] = f"{((df.iloc[nx].get('close') - base) / base) * 100.0:,.{diff_decimals}f}"

        else:
            an = self._chart.to_data_coordinates(ax, ay)
            assert an is not None

            ax, ay = an

            base_date = self._cache.quotes().index[ax]

            info["Diff(B)"] = f"{nx-ax}"

            if (
                self._frequency == DAILY
                or self._frequency == WEEKLY
                or self._frequency == MONTHLY
            ):
                info["Diff(D)"] = f"{(df.index[nx] - base_date).days}"
                info["Diff(W)"] = f"{(df.index[nx] - base_date).days / 7:.2f}"
                info["Diff(M)"] = f"{(df.index[nx] - base_date).days / 30:.2f}"

            info["Diff($)"] = f"{ny - ay:,.{quote_decimals}f}"
            info["Diff(%)"] = f"{((ny - ay) / ay) * 100.0:,.{diff_decimals}f}"

        return info, note


class PresetController(metaclass=ABCMeta):
    def __init__(
        self,
        cache: QuotesCache,
        symbol: str,
        frequency: FREQUENCY,
        chart_size: CHART_SIZE,
        parameters: Optional[Dict[str, str]],
    ) -> None:
        self._cache = cache
        self._symbol = symbol
        self._frequency = frequency

        self._chart_size = chart_size
        self._setting = Setting(chart_size=chart_size)

        self._parameters = parameters

    def get_setting(self) -> Setting:
        return self._setting

    @abstractmethod
    def get_theme(self) -> Theme:
        raise NotImplementedError

    @abstractmethod
    def get_plotters(self) -> List[Plotter]:
        raise NotImplementedError


class KushamiNekoController(PresetController):
    def get_theme(self) -> Theme:
        return Theme()

    def get_plotters(
        self,
    ) -> List[Plotter]:
        market = "US"
        if self._symbol in ("gg", "hr", "hf", "gx", "fn"):
            market = "EU"

        plotters = [
            BackgroundTimeRangeMark(
                quotes=self._cache.quotes(),
                frequency=self._frequency,
                market=market,
            ),
            LastQuote(
                quotes=self._cache.quotes(),
                frequency=self._frequency,
                font_color=self.get_theme().get_color("text"),
                font_properties=self.get_theme().get_font(
                    self._setting.text_fontsize(multiplier=1.5)
                ),
            ),
        ]

        if self._parameters is not None:

            if self._parameters.get("CandleSticks", "").lower() == "true":
                plotters.append(
                    CandleSticks(
                        quotes=self._cache.quotes(),
                        shadow_width=self._setting.shadow_width(),
                        body_width=self._setting.body_width(),
                        color_up=self.get_theme().get_color("up"),
                        color_down=self.get_theme().get_color("down"),
                        color_unchanged=self.get_theme().get_color("unchanged"),
                    ),
                )

            moving_average_multiplier = 1

            if (
                self._frequency == INTRADAY_15MINUTES
                or self._frequency == INTRADAY_30MINUTES
            ):
                if self._parameters.get("IntradayAdjustment", "").lower() == "true":
                    if self._frequency == INTRADAY_15MINUTES:
                        moving_average_multiplier = 4
                    elif self._frequency == INTRADAY_30MINUTES:
                        moving_average_multiplier = 2
                    else:
                        moving_average_multiplier = 1

            moving_average_class = SimpleMovingAverage
            if self._parameters.get("EXMovingAverages", "").lower() == "true":
                moving_average_class = ExponentialMovingAverage

            if self._parameters.get("MovingAverages", "").lower() == "true":
                plotters.extend(
                    [
                        moving_average_class(
                            n=5 * moving_average_multiplier,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("sma0"),
                            line_alpha=self.get_theme().get_alpha("sma"),
                            line_width=self._setting.linewidth() * 1.5,
                        ),
                        moving_average_class(
                            n=20 * moving_average_multiplier,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("sma1"),
                            line_alpha=self.get_theme().get_alpha("sma"),
                            line_width=self._setting.linewidth() * 1.5,
                        ),
                        moving_average_class(
                            n=60 * moving_average_multiplier,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("sma2"),
                            line_alpha=self.get_theme().get_alpha("sma"),
                            line_width=self._setting.linewidth() * 1.5,
                        ),
                    ]
                )

            if self._parameters.get("MovingAverages10", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=10 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma6"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth() * 1.5,
                    ),
                )

            if self._parameters.get("EXMovingAverages10", "").lower() == "true":
                plotters.append(
                    ExponentialMovingAverage(
                        n=10 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma6"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth() * 1.5,
                    ),
                )

            if self._parameters.get("MovingAverages40", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=40 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma6"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth() * 1.5,
                    ),
                )

            if self._parameters.get("MovingAverages100", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=100 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma3"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth(),
                    )
                )

            if self._parameters.get("MovingAverages125", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=125 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma3"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth(),
                    )
                )

            if self._parameters.get("MovingAverages300", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=300 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma4"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth(),
                    )
                )

            if self._parameters.get("MovingAverages250", "").lower() == "true":
                plotters.append(
                    moving_average_class(
                        n=250 * moving_average_multiplier,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color("sma4"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth(),
                    )
                )

            if self._parameters.get("EXEnvelope10", "").lower() == "true":
                m = 0.001

                if self._symbol in ("es", "nq", "qr", "ym"):
                    m = 0.002
                elif self._symbol in ("e6", "j6", "b6", "a6", "d6", "s6", "n6"):
                    m = 0.002

                plotters.extend(
                    [
                        ExponentialMovingAverageEnvelope(
                            n=10 * moving_average_multiplier,
                            m=m,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb0"),
                            line_alpha=1.0,
                            line_width=self._setting.linewidth(),
                        ),
                        ExponentialMovingAverageEnvelope(
                            n=10 * moving_average_multiplier,
                            m=m * (1 + 0.25),
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb2"),
                            line_alpha=0.4,
                            line_width=self._setting.linewidth(),
                        ),
                        ExponentialMovingAverageEnvelope(
                            n=10 * moving_average_multiplier,
                            m=m * (1 - 0.25),
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb2"),
                            line_alpha=0.5,
                            line_width=self._setting.linewidth(),
                        ),
                        ExponentialMovingAverageEnvelope(
                            n=10 * moving_average_multiplier,
                            m=m * (1 - 0.5),
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb3"),
                            line_alpha=0.6,
                            line_width=self._setting.linewidth(),
                        ),
                        ExponentialMovingAverageEnvelope(
                            n=10 * moving_average_multiplier,
                            m=m * (1 - 0.75),
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb3"),
                            line_alpha=0.4,
                            line_width=self._setting.linewidth(),
                        ),
                    ]
                )

            if self._parameters.get("Studies", "").lower() == "true":
                if self._frequency in (
                    INTRADAY_15MINUTES,
                    INTRADAY_30MINUTES,
                    INTRADAY_60MINUTES,
                ):
                    plotters.append(
                        NoteMarker(
                            symbol=self._symbol,
                            quotes=self._cache.quotes(),
                            frequency=self._frequency,
                        ),
                    )

            if self._parameters.get("InterestRates", "").lower() == "true":
                plotters.append(
                    InterestRatesSummary(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                    ),
                )

            if self._parameters.get("StudyZone", "").lower() == "true":
                plotters.append(
                    StudyZone(
                        symbol=self._symbol,
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        candlesticks_body_width=self._setting.body_width(),
                    ),
                )

            if self._parameters.get("BollingerBands", "").lower() == "true":
                plotters.extend(
                    [
                        BollingerBand(
                            n=20 * moving_average_multiplier,
                            m=1.5,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb0"),
                            line_alpha=self.get_theme().get_alpha("bb"),
                            line_width=self._setting.linewidth(),
                        ),
                        BollingerBand(
                            n=20 * moving_average_multiplier,
                            m=2.0,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb1"),
                            line_alpha=self.get_theme().get_alpha("bb"),
                            line_width=self._setting.linewidth(),
                        ),
                        BollingerBand(
                            n=20 * moving_average_multiplier,
                            m=2.5,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb2"),
                            line_alpha=self.get_theme().get_alpha("bb"),
                            line_width=self._setting.linewidth(),
                        ),
                        BollingerBand(
                            n=20 * moving_average_multiplier,
                            m=3.0,
                            quotes=self._cache.full_quotes(),
                            slice_start=self._cache.quotes().index[0],
                            slice_end=self._cache.quotes().index[-1],
                            line_color=self.get_theme().get_color("bb3"),
                            line_alpha=self.get_theme().get_alpha("bb"),
                            line_width=self._setting.linewidth(),
                        ),
                    ]
                )

            if self._parameters.get("Volume", "").lower() == "true":
                plotters.append(
                    Volume(
                        quotes=self._cache.quotes(),
                        body_width=self._setting.body_width(),
                        color_up=self.get_theme().get_color("up"),
                        color_down=self.get_theme().get_color("down"),
                        color_unchanged=self.get_theme().get_color("unchanged"),
                    ),
                )

            if self._parameters.get("TradingLevel", "").lower() == "true":
                plotters.append(
                    Level(
                        full_quotes=self._cache.full_quotes(),
                        quotes=self._cache.quotes(),
                        symbol=self._symbol,
                        frequency=self._frequency,
                        font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize(multiplier=1.5)
                        ),
                    )
                )

            if self._parameters.get("VolatilityZone", "").lower() == "true":
                if self._symbol in (
                    "vix",
                    "vxn",
                    "rvx",
                    "jniv",
                    "vstx",
                    "vhsi",
                    "vxfxi",
                ):

                    reference = self._parameters.get("VixReferenceDate", "").strip()
                    op = self._parameters.get("VixOp", "").strip()

                    if reference != "" and op != "":
                        plotters.append(
                            VolatilityZone(
                                quotes=self._cache.quotes(),
                                dtime=datetime.strptime(reference, "%Y%m%d"),
                                op=op,
                            )
                        )

            if self._parameters.get("EntryZone", "").lower() == "true":
                notice = self._parameters.get("EntryNoticeDate", "").strip()
                prepare = self._parameters.get("EntryPrepareDate", "").strip()
                op = self._parameters.get("EntryOp", "").strip()

                notice_date = (
                    datetime.strptime(notice, "%Y%m%d") if notice != "" else None
                )
                prepare_date = (
                    datetime.strptime(prepare, "%Y%m%d") if prepare != "" else None
                )

                if op != "":
                    plotters.append(
                        EntryZone(
                            quotes=self._cache.quotes(),
                            frequency=self._frequency,
                            operation=op,
                            notice_signal=notice_date,
                            prepare_signal=prepare_date,
                        ),
                    )

            if self._parameters.get("EWRelativeStrength", "").lower() == "true":
                plotters.append(
                    EqualWeightedRelativeStrength(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        symbol=self._symbol,
                    )
                )

            if self._parameters.get("AdvanceDecline", "").lower() == "true":
                plotters.append(
                    AdvanceDeclineLine(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        symbol=self._symbol,
                    )
                )

            if self._parameters.get("AdvanceDeclineVolume", "").lower() == "true":
                plotters.append(
                    AdvanceDeclineLine(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        symbol=self._symbol,
                        volume_diff=True,
                    )
                )

            if self._parameters.get("DistributionDays", "").lower() == "true":
                plotters.append(
                    DistributionsDay(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        font_color=self.get_theme().get_color("text"),
                        font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize()
                        ),
                        info_font_properties=self.get_theme().get_font(
                            self._setting.text_fontsize(multiplier=1.5)
                        ),
                    )
                )

            if self._parameters.get("VolatilityBodySize", "").lower() == "true":
                plotters.append(
                    VolatilityRealBodyContraction(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        symbol=self._symbol,
                    )
                )

            if self._parameters.get("VolatilitySummary", "").lower() == "true":
                plotters.append(
                    VolatilitySummary(
                        quotes=self._cache.quotes(),
                        frequency=self._frequency,
                        symbol=self._symbol,
                    )
                )

        return plotters


class MagicalController(PresetController):
    def get_theme(self) -> Theme:
        return MagicalTheme()

    def get_plotters(self) -> List[Plotter]:
        plotters = [
            BackgroundTimeRangeMark(
                quotes=self._cache.quotes(),
                frequency=self._frequency,
            ),
            CandleSticks(
                quotes=self._cache.quotes(),
                shadow_width=self._setting.shadow_width(),
                body_width=self._setting.body_width(),
                color_up=self.get_theme().get_color("up"),
                color_down=self.get_theme().get_color("down"),
                color_unchanged=self.get_theme().get_color("unchanged"),
            ),
            LastQuote(
                quotes=self._cache.quotes(),
                frequency=self._frequency,
                font_color=self.get_theme().get_color("text"),
                font_properties=self.get_theme().get_font(
                    self._setting.text_fontsize(multiplier=1.5)
                ),
            ),
        ]

        for key, value in self._parameters.items():
            # match = re.match(r"^SMA\s*(\d+)$", key)
            match = re.match(r"^MovingAverages\s*(\d+)$", key)
            if match is not None:
                if value.lower() != "true":
                    continue

                n = int(match.group(1))
                plotters.append(
                    SimpleMovingAverage(
                        n=n,
                        quotes=self._cache.full_quotes(),
                        slice_start=self._cache.quotes().index[0],
                        slice_end=self._cache.quotes().index[-1],
                        line_color=self.get_theme().get_color(f"sma{n}"),
                        line_alpha=self.get_theme().get_alpha("sma"),
                        line_width=self._setting.linewidth(),
                    ),
                )

        return plotters
