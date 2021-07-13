from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import NewType, cast

import pandas as pd
from Fun.futures.contract import Contract
from Fun.utils import colors, pretty

ADJUSTMENT_METHOD = NewType("ADJUSTMENT_METHOD", int)

RATIO = ADJUSTMENT_METHOD(0)
DIFFERENCE = ADJUSTMENT_METHOD(1)
NO_ADJUSTMENT = ADJUSTMENT_METHOD(2)


class RollingMethod(metaclass=ABCMeta):
    def __init__(self, adjustment_method: ADJUSTMENT_METHOD = RATIO) -> None:

        assert adjustment_method in (RATIO, DIFFERENCE, NO_ADJUSTMENT)

        self._adjustment_method = adjustment_method

        if adjustment_method == RATIO:
            self._adjustment = 1.0
        elif adjustment_method == DIFFERENCE:
            self._adjustment = 0.0
        elif adjustment_method == NO_ADJUSTMENT:
            self._adjustment = 0.0
        else:
            raise ValueError("invalid adjustment method")

    @abstractmethod
    def _rolling_date(self, front: Contract, back: Contract) -> datetime:
        raise NotImplementedError

    def rolling_date(self, front: Contract, back: Contract) -> datetime:
        rolling_date = self._rolling_date(front, back)

        bdf = back.dataframe()
        fdf = front.dataframe()

        if self._adjustment_method == RATIO:
            self._adjustment *= (
                bdf.loc[bdf.index == rolling_date, "close"]
                / fdf.loc[fdf.index == rolling_date, "close"]
            ).iloc[0]
        elif self._adjustment_method == DIFFERENCE:
            self._adjustment += (
                bdf.loc[bdf.index == rolling_date, "close"]
                - fdf.loc[fdf.index == rolling_date, "close"]
            ).iloc[0]
        elif self._adjustment_method == NO_ADJUSTMENT:
            pass
        else:
            raise ValueError("invalid adjustment method")

        return rolling_date

    def adjustment(self) -> float:
        return self._adjustment

    def adjust(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._adjustment_method == RATIO:
            return df * self._adjustment
        elif self._adjustment_method == DIFFERENCE:
            return df + self._adjustment
        elif self._adjustment_method == NO_ADJUSTMENT:
            return df
        else:
            raise ValueError("invalid adjustment method")


class LastNTradingDays(RollingMethod):
    def __init__(
        self, offset: int = 4, adjustment_method: ADJUSTMENT_METHOD = RATIO
    ) -> None:
        assert offset >= 0

        super().__init__(adjustment_method)
        self._offset = 4

    def _rolling_date(self, front: Contract, back: Contract) -> datetime:
        n = -self._offset if self._offset != 0 else 0
        return cast(datetime, front.dataframe().index[n].to_pydatetime())


class FirstOfMonth(RollingMethod):
    def _rolling_date(self, front: Contract, back: Contract) -> datetime:
        df = front.dataframe()
        selector = (df.index.month == df.index[-1].month) & (
            (df.index[-1] - df.index).days < 90
        )

        return cast(datetime, df.loc[selector].index[0].to_pydatetime())


class VolumeAndOpenInterest(RollingMethod):
    def __init__(
        self,
        backup: RollingMethod = FirstOfMonth(),
        adjustment_method: ADJUSTMENT_METHOD = RATIO,
    ) -> None:
        assert backup is not None

        super().__init__(adjustment_method)
        self._backup = backup

    def _rolling_date(self, front: Contract, back: Contract) -> datetime:
        fdf = front.dataframe()
        bdf = back.dataframe()

        volume = (
            (
                bdf.loc[bdf.index.isin(fdf.index), "volume"]
                >= fdf.loc[fdf.index.isin(bdf.index), "volume"]
            )
            & (bdf.loc[bdf.index.isin(fdf.index), "volume"] != 0)
            & (fdf.loc[fdf.index.isin(bdf.index), "volume"] != 0)
        )

        interest = (
            (
                bdf.loc[bdf.index.isin(fdf.index), "open interest"]
                >= fdf.loc[fdf.index.isin(bdf.index), "open interest"]
            )
            & (bdf.loc[bdf.index.isin(fdf.index), "open interest"] != 0)
            & (fdf.loc[fdf.index.isin(bdf.index), "open interest"] != 0)
        )

        union = None
        if volume.any() and interest.any():
            union = volume & interest
        elif volume.any() and not interest.any():
            union = volume
        elif not volume.any() and interest.any():
            union = interest
        else:
            pretty.color_print(
                colors.PAPER_AMBER_300,
                f"empty volume and open interest in contracts {front.code().upper()} and {back.code().upper()}"
                ", use backup rolling method instead",
            )

            return cast(datetime, self._backup.rolling_date(front, back))

        assert union is not None

        selector = (fdf.index.isin(bdf.index)) & ((fdf.index[-1] - fdf.index).days < 90)

        cross = fdf.loc[selector].loc[union]
        if len(cross) == 0:
            pretty.color_print(
                colors.PAPER_AMBER_300,
                f"no valid intersection in contracts {front.code().upper()} and {back.code().upper()}"
                ", use backup rolling method instead",
            )
            return cast(datetime, self._backup.rolling_date(front, back))

        return cast(
            datetime,
            cross.index[0].to_pydatetime(),
        )


if __name__ == "__main__":
    from Fun.data.source import (
        DAILY,
        FREQUENCY,
        INTRADAY_15MINUTES,
        INTRADAY_60MINUTES,
        INTRADAY_30MINUTES,
        MONTHLY,
        WEEKLY,
        DataSource,
    )

    from Fun.futures.contract import Contract, FINANCIAL_CONTRACT_MONTHS

    from Fun.data.barchart import BarchartContract
    from datetime import datetime

    bdfc = Contract("znh20", FINANCIAL_CONTRACT_MONTHS)
    fdfc = Contract("znz19", FINANCIAL_CONTRACT_MONTHS)

    bdf = bdfc.dataframe()
    fdf = fdfc.dataframe()

    # print(bdf["open interest"])
    # print(fdf["open interest"])

    # print(bdf.dataframe().dtypes)
    # print(type(bdf.dataframe().index))

    # print(fdf.dataframe().dtypes)
    # print(type(fdf.dataframe().index))

    print(
        (
            bdf.loc[bdf.index.isin(fdf.index), "volume"]
            >= fdf.loc[fdf.index.isin(bdf.index), "volume"]
        )
        & (bdf.loc[bdf.index.isin(fdf.index), "volume"] != 0)
        & (fdf.loc[fdf.index.isin(bdf.index), "volume"] != 0)
    )

    print(
        (
            bdf.loc[bdf.index.isin(fdf.index), "open interest"]
            >= fdf.loc[fdf.index.isin(bdf.index), "open interest"]
        )
        # & (bdf.loc[bdf.index.isin(fdf.index), "open interest"] != 0)
        # & (fdf.loc[fdf.index.isin(bdf.index), "open interest"] != 0)
    )

    # volume = (
    #         (
    #             bdf.loc[bdf.index.isin(fdf.index), "volume"]
    #             >= fdf.loc[fdf.index.isin(bdf.index), "volume"]
    #         )
    #         & (bdf.loc[bdf.index.isin(fdf.index), "volume"] != 0)
    #         & (fdf.loc[fdf.index.isin(bdf.index), "volume"] != 0)
    # )

    # start = datetime.strptime("20200101", "%Y%m%d")
    # end = datetime.strptime("20210101", "%Y%m%d")

    # src = BarchartContract()
    # bdf = src.read(start=start, end=end, symbol="znm21", frequency=DAILY)
    # fdf = src.read(start=start, end=end, symbol="znh21", frequency=DAILY)

    # print(VolumeAndOpenInterest()._rolling_date(fdf, bdf))
