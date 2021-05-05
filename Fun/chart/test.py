from datetime import datetime

from fun.chart.base import MEDIUM_CHART
from fun.chart.setting import Setting
from fun.chart.static import TradingChart
from fun.data.source import DAILY
from fun.futures.continuous import ContinuousContract

if __name__ == "__main__":
    c = ContinuousContract()

    exs = datetime.strptime("20170101", "%Y%m%d")
    exe = datetime.strptime("20200101", "%Y%m%d")

    s = datetime.strptime("20180101", "%Y%m%d")
    e = datetime.strptime("20190101", "%Y%m%d")

    df = c.read(exs, exe, "es", DAILY)

    large = TradingChart(df.loc[s:e])
    medium = TradingChart(df.loc[s:e], setting=Setting(chart_size=MEDIUM_CHART))

    large.render("large.png")
    medium.render("medium.png")
