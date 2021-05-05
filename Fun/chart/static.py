import io
from typing import List, Optional, Tuple, Union

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from fun.chart import base
from fun.chart.base import LARGE_CHART, MEDIUM_CHART, SMALL_CHART
from fun.chart.setting import Setting
from fun.chart.theme import Theme
from fun.chart.ticker import StepTicker, Ticker, TimeTicker
from fun.plotter.plotter import Plotter
from matplotlib import axes, figure

matplotlib.use("agg")


class TradingChart(base.ChartFactory):
    def __init__(
        self,
        quotes: pd.DataFrame,
        theme: Theme = Theme(),
        scale: str = "log",
        setting: Setting = Setting(chart_size=LARGE_CHART),
        figsize: Tuple[float, float] = (16.0, 9.0),
    ) -> None:

        assert quotes is not None
        assert setting is not None
        assert setting.chart_size() in (LARGE_CHART, MEDIUM_CHART)

        super().__init__(quotes)

        if setting.chart_size() == SMALL_CHART:
            self._figsize = (figsize[0] * 1.0, figsize[1] * 1.0)
        elif setting.chart_size() == MEDIUM_CHART:
            self._figsize = (figsize[0] * 1.2, figsize[1] * 1.2)
        elif setting.chart_size() == LARGE_CHART:
            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)

        assert self._figsize is not None

        self._theme = theme
        self._scale = scale

        self._setting = setting

        self._figure: Optional[figure.Figure] = None
        self._ax: Optional[axes.Axes] = None

    def _setup_xticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_xticks(loc)
        ax.set_xticklabels(
            labels, fontproperties=self._theme.get_font(self._setting.tick_fontsize())
        )

    def _setup_yticks(self, ax: axes.Axes, ticker: Ticker) -> None:
        loc, labels = ticker.ticks()
        ax.set_yticks(loc)
        ax.set_yticklabels(
            labels, fontproperties=self._theme.get_font(self._setting.tick_fontsize())
        )

    def _setup_general(self, fig: figure.Figure, ax: axes.Axes) -> None:
        ax.spines["top"].set_visible(False)
        ax.spines["bottom"].set_visible(False)
        ax.spines["left"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.grid(
            True,
            color=self._theme.get_color("grid"),
            alpha=self._theme.get_alpha("grid"),
        )

        ax.set_axisbelow(True)

        fig.set_facecolor(self._theme.get_color("background"))
        ax.set_facecolor(self._theme.get_color("background"))

        ax.tick_params(
            axis="both",
            color=self._theme.get_color("ticks"),
            labelcolor=self._theme.get_color("ticks"),
            labelsize=self._setting.tick_fontsize(),
        )

        ax.yaxis.tick_right()

    def to_data_coordinates(self, x: float, y: float) -> Optional[Tuple[float, float]]:
        if self._figure is None or self._ax is None:
            return None

        dx, dy = self._figure.transFigure.transform_point((x, y))
        nx, ny = self._ax.transData.inverted().transform_point((dx, dy))

        min_y, max_y = self._ax.get_ylim()

        nx = int(min(max(round(nx), 0), len(self._quotes) - 1))
        ny = min(max(ny, min_y), max_y)

        return (nx, ny)

    def render(
        self,
        output: Optional[Union[str, io.BytesIO]] = None,
        plotters: Optional[List[Plotter]] = None,
        interactive: bool = False,
    ) -> None:

        fig, ax = plt.subplots(
            figsize=self._figsize,
            facecolor=self._theme.get_color("background"),
            tight_layout=False,
        )

        ax.set_yscale(self._scale)

        self._setup_general(fig, ax)
        self._setup_xticks(ax, TimeTicker(self._quotes))
        self._setup_yticks(ax, StepTicker(*self.chart_yrange()))

        self._figure = fig
        self._ax = ax

        ax.set_xlim(*self.chart_xrange())
        ax.set_ylim(*self.chart_yrange())

        if plotters is not None and len(plotters) > 0:
            for p in plotters:
                p.plot(ax)

        ax.autoscale_view()

        plt.tight_layout()

        if interactive:
            plt.show()
        else:
            assert output is not None
            plt.savefig(
                output,
                dpi=100,
                facecolor=self._theme.get_color("background"),
            )

        plt.close(fig)
