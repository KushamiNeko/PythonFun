import io
import os
import re
from abc import ABCMeta, abstractmethod
from datetime import datetime, timedelta
from typing import NewType

import numpy as np
import pandas as pd
import requests
from fun.utils import colors, pretty

FREQUENCY = NewType("FREQUENCY", int)

DAILY = FREQUENCY(0)
WEEKLY = FREQUENCY(1)
MONTHLY = FREQUENCY(2)

# HOURLY = FREQUENCY(3)
INTRADAY_60MINUTES = FREQUENCY(3)
INTRADAY_30MINUTES = FREQUENCY(4)
INTRADAY_15MINUTES = FREQUENCY(5)


def daily_to_weekly(df: pd.DataFrame) -> pd.DataFrame:
    agg = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }

    if "open interest" in df.columns:
        agg["open interest"] = "sum"

    dfg = df.groupby(pd.Grouper(freq="W-MON", label="left", closed="left"))

    df = dfg.agg(agg)

    return df


def daily_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
    agg = {
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }

    if "open interest" in df.columns:
        agg["open interest"] = "sum"

    dfg = df.groupby(pd.Grouper(freq="MS", label="left", closed="left"))

    df = dfg.agg(agg)

    return df


class DataSource(metaclass=ABCMeta):
    @abstractmethod
    def _timestamp_preprocessing(self, x: str) -> datetime:
        raise NotImplementedError

    @abstractmethod
    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        raise NotImplementedError

    def _datafeed(self, url: str) -> io.BytesIO:
        resp = requests.get(url)
        resp.raise_for_status()

        data = io.BytesIO(resp.content)

        return data

    def _localfile(self, path: str) -> str:

        home = os.getenv("HOME")
        assert home is not None

        path = os.path.join(home, "Documents", "data_source", path)
        if not os.path.exists(path):
            # pretty.color_print(colors.PAPER_RED_400, f"file not found: {path}")
            raise FileNotFoundError(f"file not found: {path}")

        return path

    def _preload(self, freq: FREQUENCY) -> timedelta:
        preload = 30

        if (
            freq == INTRADAY_15MINUTES
            or freq == INTRADAY_30MINUTES
            or freq == INTRADAY_60MINUTES
        ):
            return timedelta(hours=preload * 3)
        elif freq == DAILY:
            return timedelta(days=preload)
        elif freq == WEEKLY:
            return timedelta(weeks=preload)
        elif freq == MONTHLY:
            return timedelta(days=preload * 31)
        else:
            raise ValueError(f"invalid frequency: {freq}")

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        return df.rename(columns=cols)

    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:

        assert frequency in (
            INTRADAY_15MINUTES,
            INTRADAY_30MINUTES,
            INTRADAY_60MINUTES,
            DAILY,
            WEEKLY,
            MONTHLY,
        )

        df = self._read_data(start, end, symbol, frequency)

        df = self._rename_columns(df)

        df.loc[:, "timestamp"] = (
            df.loc[:, "timestamp"].apply(self._timestamp_preprocessing)
            # .astype(np.datetime64)
        )

        df = df.set_index("timestamp")

        if (
            frequency != INTRADAY_15MINUTES
            and frequency != INTRADAY_30MINUTES
            and frequency != INTRADAY_60MINUTES
        ):
            unusual = df.index.hour != 0
            if unusual.any():
                pretty.color_print(
                    colors.PAPER_AMBER_300,
                    f"dropping {len(df.loc[unusual])} rows containing unusual timestamp from {symbol.upper()}",
                )
                df = df.drop(df.loc[unusual].index)

        df = df.sort_index()

        if frequency == WEEKLY:
            df = daily_to_weekly(df)
        elif frequency == MONTHLY:
            df = daily_to_monthly(df)

        length = len(df)

        na = df.isna().any(axis=1)
        if na.any():
            pretty.color_print(
                colors.PAPER_AMBER_300,
                f"dropping {len(df.loc[na])} rows containing nan from {symbol.upper()}",
            )

            dropped_length = len(df.loc[na])

            df = df.dropna()

            assert length == len(df) + dropped_length

        return df.astype(np.float)


class AlphaVantage(DataSource):
    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:

        if not re.match(r"^[a-zA-Z]+$", symbol):
            raise ValueError(f"invalid symbol: {symbol}")

        if os.getenv("ALPHA_VANTAGE") is None:
            raise ValueError("empty ALPHA_VANTAGE environment variable")

        root = r"https://www.alphavantage.co/query"

        queries = [
            f"apikey={os.getenv('ALPHA_VANTAGE', '')}",
            f"symbol={symbol}",
            f"function={self._frequency(frequency)}",
            "interval=60min",
            "outputsize=full",
            "datatype=csv",
        ]

        url = f"{root}?{'&'.join(queries)}"
        return url

    def _timestamp_preprocessing(self, x: str) -> datetime:
        pattern = r"^\d{4}-\d{2}-\d{2}$"

        if re.match(pattern, x):
            return datetime.strptime(x, "%Y-%m-%d")
        else:
            return datetime.strptime(x, "%Y-%m-%d %H:%M:%S")

    def _frequency(self, freq: FREQUENCY) -> str:
        if freq == INTRADAY_60MINUTES:
            return "TIME_SERIES_INTRADAY"
        elif freq == DAILY:
            return "TIME_SERIES_DAILY"
        elif freq == WEEKLY:
            return "TIME_SERIES_WEEKLY"
        elif freq == MONTHLY:
            return "TIME_SERIES_MONTHLY"
        else:
            raise ValueError(f"invalid frequency: {freq}")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        df = pd.read_csv(self._datafeed(self._url(start, end, symbol, DAILY)))
        return df


class Yahoo(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%Y-%m-%d")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join("yahoo", f"{symbol}.csv")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        df = pd.read_csv(self._localfile(self._url(start, end, symbol, DAILY)))
        df = df.drop("Adj Close", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        return df.rename(columns=cols)


class StockCharts(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%m-%d-%Y")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join("stockcharts", f"{symbol}.txt")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        with open(self._localfile(self._url(start, end, symbol, DAILY)), "r") as f:
            lines = f.readlines()

        content = "\n".join([re.subn(r"\s+", ",", l.strip())[0] for l in lines])
        data = io.StringIO(content)

        df = pd.read_csv(data)

        df = df.drop(0)
        df = df.drop("Day", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        return df.rename(columns=cols)


class InvestingCom(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        return datetime.strptime(x, "%b %d, %Y")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join("investing.com", f"{symbol}.csv")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        df = pd.read_csv(self._localfile(self._url(start, end, symbol, DAILY)))
        df = df.drop("Change %", axis=1)

        df.loc[:, "Vol."] = df.loc[:, "Vol."].apply(
            lambda x: 0 if x == "-" or type(x) is str else x
        )

        df.loc[:, "Price"] = df.loc[:, "Price"].apply(
            lambda x: x.replace(",", "") if type(x) is str and "," in x else x
        )

        df.loc[:, "Open"] = df.loc[:, "Open"].apply(
            lambda x: x.replace(",", "") if type(x) is str and "," in x else x
        )

        df.loc[:, "High"] = df.loc[:, "High"].apply(
            lambda x: x.replace(",", "") if type(x) is str and "," in x else x
        )

        df.loc[:, "Low"] = df.loc[:, "Low"].apply(
            lambda x: x.replace(",", "") if type(x) is str and "," in x else x
        )

        df.loc[:, ["Price", "Open", "High", "Low", "Vol."]] = df.loc[
            :, ["Price", "Open", "High", "Low", "Vol."]
        ].astype(np.float)

        selector = df.loc[:, "Open"] <= 0
        df.loc[selector, "Open"] = df.loc[selector, "Price"]

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["Date"] = "timestamp"
        cols["Vol."] = "volume"
        cols["Price"] = "close"
        return df.rename(columns=cols)


class CryptoData(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        m = re.match(r"(\d{4}-\d{2}-\d{2})(\s\d{2}:\d{2}:\d{2})*", x)
        assert m is not None

        if m.group(2) is not None:
            return datetime.strptime(x, r"%Y-%m-%d %H:%M:%S")
        else:
            return datetime.strptime(x, r"%Y-%m-%d")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        return os.path.join("cryptodata", f"{symbol}.csv")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        df = pd.read_csv(
            self._localfile(self._url(start, end, symbol, DAILY)), header=1
        )
        df = df.drop("unix", axis=1)
        df = df.drop("symbol", axis=1)

        if "vwap" in df.columns:
            df = df.drop("vwap", axis=1)

        if "tradecount" in df.columns:
            df.loc[:, "tradecount"].fillna(0, inplace=True)

        opens = df.loc[:, "open"]
        highs = df.loc[:, "high"]
        lows = df.loc[:, "low"]
        closes = df.loc[:, "close"]

        rows = df.loc[(opens <= 0) | (highs <= 0) | (lows <= 0) | (closes <= 0)].index

        if len(rows) > 0:
            pretty.color_print(
                colors.PAPER_AMBER_300,
                f"CryptoData {symbol.upper()} contains 0 in open, high, low, or close. Dropping {len(rows)} rows",
            )
        df = df.drop(rows)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}
        cols["date"] = "timestamp"
        cols["Volume USD"] = "volume"
        return df.rename(columns=cols)


class CoinAPI(DataSource):
    def _timestamp_preprocessing(self, x: str) -> datetime:
        # 2020-12-02T00:00:00.0000000Z
        m = re.match(r"^(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\.[0]+Z$", x)
        assert m is not None

        return datetime.strptime(m.group(1), r"%Y-%m-%dT%H:%M:%S")

    def _url(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> str:
        if frequency in (DAILY, WEEKLY, MONTHLY):
            return os.path.join("coinapi", symbol)
        elif frequency == INTRADAY_15MINUTES:
            return os.path.join("coinapi", f"{symbol}@15m")
        elif frequency == INTRADAY_30MINUTES:
            return os.path.join("coinapi", f"{symbol}@30m")
        elif frequency == INTRADAY_60MINUTES:
            return os.path.join("coinapi", f"{symbol}@60m")

    def _read_data(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:

        root = self._localfile(self._url(start, end, symbol, frequency))

        files = os.listdir(root)
        files.sort()

        df = None
        for f in files:
            path = os.path.join(root, f)
            if df is None:
                df = pd.read_json(path)
            else:
                df = df.append(pd.read_json(path))

        if df is None:
            raise ValueError(f"no files for symbol: {symbol}")

        assert df is not None

        assert (
            len(df.loc[:, "time_period_start"])
            == df.loc[:, "time_period_start"].nunique()
        )

        assert (
            len(df.loc[:, "time_period_end"]) == df.loc[:, "time_period_end"].nunique()
        )

        df = df.drop("time_period_end", axis=1)
        df = df.drop("time_open", axis=1)
        df = df.drop("time_close", axis=1)

        return df

    def _rename_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        cols = {k: k.lower() for k in df.columns}

        for k in cols.keys():
            if "price" in k:
                cols[k] = k.replace("price_", "", -1)

        cols["time_period_start"] = "timestamp"
        cols["volume_traded"] = "volume"
        return df.rename(columns=cols)


# if __name__ == "__main__":
# c = CoinAPI()

# s = datetime.strptime("20190101", "%Y%m%d")
# e = datetime.strptime("20201201", "%Y%m%d")

# df = c.read(s, e, "ltcusd", DAILY)
# print(df.head(100))
# print(df.tail(95))
# print(df.index.nunique())
