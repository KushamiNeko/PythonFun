from datetime import datetime

import pandas as pd
from Fun.data.barchart import Barchart
from Fun.data.source import FREQUENCY


class BarchartCumulativeSum(Barchart):
    def read(
        self, start: datetime, end: datetime, symbol: str, frequency: FREQUENCY
    ) -> pd.DataFrame:
        df = super(BarchartCumulativeSum, self).read(
            start=start, end=end, symbol=symbol, frequency=frequency
        )
        return df.cumsum()
