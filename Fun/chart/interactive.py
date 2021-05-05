#import io
#from typing import List, Optional, Tuple, Union, cast
#
#import numpy as np
#import pandas as pd
#from bokeh.core.properties import value
#from bokeh.embed import file_html
#
## from bokeh.layouts import column
#from bokeh.models.tools import CrosshairTool, HoverTool, SaveTool
#from bokeh.plotting import ColumnDataSource, figure, output_file, save, show
#from bokeh.resources import CDN
#
#from Fun.chart import base
#from Fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART  # SMALL_CHART,
#from Fun.chart.theme import InteractiveTheme
#from Fun.chart.ticker import StepTicker, Ticker, TimeTicker
#from Fun.trading.transaction import FuturesTransaction
#
#
#class CandleSticks(base.CandleSticks):
#    def __init__(
#        self,
#        quotes: pd.DataFrame,
#        figsize: Tuple[float, float] = (1920.0, 1080.0),
#        chart_size: CHART_SIZE = LARGE_CHART,
#    ):
#        super().__init__(quotes, chart_size)
#
#        assert self._chart_size in (MEDIUM_CHART, LARGE_CHART)
#
#        if self._chart_size == MEDIUM_CHART:
#            self._figsize = (figsize[0] * 1.0, figsize[1] * 1.0)
#        elif self._chart_size == LARGE_CHART:
#            self._figsize = (figsize[0] * 2.0, figsize[1] * 2.0)
#
#        self._theme = InteractiveTheme()
#
#    def _size_multiplier(self) -> float:
#        if self._chart_size == MEDIUM_CHART:
#            return 1.0
#        elif self._chart_size == LARGE_CHART:
#            return 2.0
#        else:
#            raise ValueError(f"invalid chart size")
#
#    # candlesticks settings
#    def _shadow_width(self) -> float:
#        if self._chart_size == MEDIUM_CHART:
#            return 0.25
#        elif self._chart_size == LARGE_CHART:
#            return 0.275
#        else:
#            raise ValueError(f"invalid chart size")
#
#    def _body_width(self) -> float:
#        if self._chart_size == MEDIUM_CHART:
#            return 0.65
#        elif self._chart_size == LARGE_CHART:
#            return 0.7
#        else:
#            raise ValueError(f"invalid chart size")
#
#    # general chart settings
#    def _linewidth(self) -> float:
#        return 1.5 * self._size_multiplier()
#
#    def _crosshair_linewidth(self) -> float:
#        return 2.0 * self._size_multiplier()
#
#    def _tick_fontsize(self) -> str:
#        return f"{8.0 * self._size_multiplier()}pt"
#
#    def _text_fontsize(self) -> str:
#        return f"{8.0 * self._size_multiplier()}pt"
#
#    def _text_fontweigth(self) -> str:
#        return "bold"
#
#    def _setup_xticks(self, p: figure.Figure, ticker: Ticker) -> None:
#        loc, labels = ticker.ticks()
#
#        p.xaxis.ticker = loc
#        p.xaxis.major_label_overrides = {k: v for k, v in zip(loc, labels)}
#
#        p.xgrid.ticker = loc
#
#    def _setup_yticks(self, p: figure.Figure, ticker: Ticker) -> None:
#        loc, labels = ticker.ticks()
#
#        p.yaxis.ticker = loc
#        p.yaxis.major_label_overrides = {k: v for k, v in zip(loc, labels)}
#
#        p.ygrid.ticker = loc
#
#    def _setup_general(self, p: figure.Figure) -> None:
#        p.outline_line_color = None
#
#        p.axis.major_label_text_color = self._theme.get_color("ticks")
#        p.axis.major_label_text_font_size = self._tick_fontsize
#
#        p.grid.grid_line_color = self._theme.get_color("grid")
#        p.grid.grid_line_alpha = self._theme.get_alpha("grid")
#
#    def _calculate_candlesticks_body_top_bottom(self) -> Tuple[np.ndarray, np.ndarray]:
#        dec = self._quotes.loc[:, "open"] > self._quotes.loc[:, "close"]
#
#        r = np.abs(self._quotes.loc[:, "open"] - self._quotes.loc[:, "close"])
#        avg = (self._quotes.loc[:, "open"] + self._quotes.loc[:, "close"]) / 2.0
#
#        mini = r < self._minimum_body_height()
#
#        top = np.copy(self._quotes.loc[:, "close"])
#        bottom = np.copy(self._quotes.loc[:, "open"])
#
#        top[dec] = self._quotes.loc[dec, "open"]
#        bottom[dec] = self._quotes.loc[dec, "close"]
#
#        top[mini] = avg[mini] + (self._minimum_body_height() / 2.0)
#        bottom[mini] = avg[mini] - (self._minimum_body_height() / 2.0)
#
#        return (top, bottom)
#
#    def _plot_candlesticks(self, p: figure.Figure) -> None:
#        source = ColumnDataSource(
#            data=dict(
#                x=np.arange(len(self._quotes)),
#                t=self._quotes.index.strftime("%Y-%m-%d"),
#                o=self._quotes.loc[:, "open"],
#                h=self._quotes.loc[:, "high"],
#                l=self._quotes.loc[:, "low"],
#                c=self._quotes.loc[:, "close"],
#                sma5=self._quotes.loc[:, "sma5"],
#                sma20=self._quotes.loc[:, "sma20"],
#            )
#        )
#
#        tools = [
#            CrosshairTool(
#                line_width=self._crosshair_linewidth(),
#                line_color=self._theme.get_color("crosshair"),
#                line_alpha=self._theme.get_alpha("crosshair"),
#            ),
#            HoverTool(
#                tooltips=[
#                    ("time", "@t"),
#                    ("high", "@h{%0.2f}"),
#                    ("low", "@l{%0.2f}"),
#                    ("open", "@o{%0.2f}"),
#                    ("close", "@c{%0.2f}"),
#                    ("sma 5", "@sma5{%0.2f}"),
#                    ("sma 20", "@sma20{%0.2f}"),
#                ],
#                formatters={
#                    "o": "printf",
#                    "h": "printf",
#                    "l": "printf",
#                    "c": "printf",
#                    "sma5": "printf",
#                    "sma20": "printf",
#                },
#                names=["hover"],
#            ),
#            SaveTool(),
#        ]
#
#        p.add_tools(*tools)
#
#        self._setup_general(p)
#        self._setup_xticks(p, TimeTicker(self._quotes))
#        self._setup_yticks(p, StepTicker(*self._ylim_from_price_range()))
#
#        p.vbar(
#            x="x",
#            width=self._body_width(),
#            top=self._ylim_from_price_range()[1],
#            bottom=self._ylim_from_price_range()[0],
#            fill_color="#ff0000",
#            line_color="#000000",
#            fill_alpha=0,
#            line_alpha=0,
#            source=source,
#            name="hover",
#        )
#
#        inc = self._quotes.loc[:, "close"] > self._quotes.loc[:, "open"]
#        dec = self._quotes.loc[:, "open"] > self._quotes.loc[:, "close"]
#        unc = self._quotes.loc[:, "open"] == self._quotes.loc[:, "close"]
#
#        top, bottom = self._calculate_candlesticks_body_top_bottom()
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[inc].values],
#            width=self._body_width(),
#            top=top[inc],
#            bottom=bottom[inc],
#            fill_color=self._theme.get_color("up"),
#            line_color=self._theme.get_color("up"),
#        )
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[inc].values],
#            width=self._shadow_width(),
#            top=self._quotes.loc[inc, "high"],
#            bottom=self._quotes.loc[inc, "low"],
#            fill_color=self._theme.get_color("up"),
#            line_color=self._theme.get_color("up"),
#        )
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[dec].values],
#            width=self._body_width(),
#            top=top[dec],
#            bottom=bottom[dec],
#            fill_color=self._theme.get_color("down"),
#            line_color=self._theme.get_color("down"),
#        )
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[dec].values],
#            width=self._shadow_width(),
#            top=self._quotes.loc[dec, "high"],
#            bottom=self._quotes.loc[dec, "low"],
#            fill_color=self._theme.get_color("down"),
#            line_color=self._theme.get_color("down"),
#        )
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[unc].values],
#            width=self._body_width(),
#            top=top[unc],
#            bottom=bottom[unc],
#            fill_color=self._theme.get_color("unchanged"),
#            line_color=self._theme.get_color("unchanged"),
#        )
#
#        p.vbar(
#            x=[self._quotes.index.get_loc(i) for i in self._quotes.index[unc].values],
#            width=self._shadow_width(),
#            top=self._quotes.loc[unc, "high"],
#            bottom=self._quotes.loc[unc, "low"],
#            fill_color=self._theme.get_color("unchanged"),
#            line_color=self._theme.get_color("unchanged"),
#        )
#
#    # def futures_price(
#    def plot(
#        self,
#        output: Union[str, io.BytesIO, io.StringIO],
#        records: Optional[List[FuturesTransaction]] = None,
#        show_quote: bool = True,
#        interactive: bool = False,
#    ) -> None:
#        p = figure(
#            tools=[],
#            plot_width=int(self._figsize[0]),
#            plot_height=int(self._figsize[1]),
#            y_axis_type="log",
#            x_range=(
#                0 - self._body_width(),
#                (len(self._quotes) - 1) + self._body_width(),
#            ),
#            y_range=self._ylim_from_price_range(),
#            background_fill_color="#000000",
#            border_fill_color="#000000",
#        )
#
#        self._plot_candlesticks(p)
#        self._plot_indicators(
#            lambda col, cl, al: p.line(
#                np.arange(len(self._quotes)),
#                self._quotes.loc[:, col],
#                line_width=self._linewidth(),
#                line_color=self._theme.get_color(cl),
#                line_alpha=self._theme.get_alpha(al),
#            )
#        )
#
#        if records is not None:
#            self._plot_trading_records(
#                records,
#                lambda x, y, t, ha, va: p.text(
#                    x,
#                    y,
#                    text=value(t),
#                    text_align=ha,
#                    text_baseline=va,
#                    text_color=self._theme.get_color("text"),
#                    text_font_size=self._text_fontsize(),
#                    text_font_style=self._text_fontweigth(),
#                ),
#            )
#
#        if interactive:
#            show(p)
#        else:
#            assert type(output) in (str, io.BytesIO, io.StringIO)
#            if type(output) is io.BytesIO:
#                html = file_html(p, CDN, "futures price")
#                cast(io.BytesIO, output).write(html.encode("utf-8"))
#            elif type(output) is io.StringIO:
#                html = file_html(p, CDN, "stocks price")
#                cast(io.StringIO, output).write(html)
#            elif type(output) is str:
#                output_file(output)
#                save(p)
#
#    # def stocks_price(
#    # self,
#    # output: Union[str, io.BytesIO, io.StringIO],
#    # records: Optional[List[FuturesTransaction]] = None,
#    # interactive: bool = False,
#    # ) -> None:
#    # indicator_range = (np.amin(self._quotes["rs"]), np.amax(self._quotes["rs"]))
#
#    # p_indicator = figure(
#    # tools=[],
#    # plot_width=int(self._figsize[0]),
#    # plot_height=int(self._figsize[1] * 2.0 / 12.0),
#    # x_range=(
#    # 0 - self._body_width,
#    # (len(self._quotes.index) - 1) + self._body_width,
#    # ),
#    # y_range=indicator_range,
#    # background_fill_color="#000000",
#    # border_fill_color="#000000",
#    # )
#
#    # self._setup_general(p_indicator)
#    # self._setup_xticks(p_indicator, TimeTicker(self._quotes.index))
#    # self._setup_yticks(
#    # p_indicator,
#    # StepTicker(indicator_range[0], indicator_range[1], nbins=5, steps=None),
#    # )
#
#    # p_indicator.line(
#    # np.arange(len(self._quotes.index)),
#    # self._quotes["rs"],
#    # line_width=self._linewidth,
#    # line_color=self._theme.get_color("in0"),
#    # )
#
#    # p_price = figure(
#    # tools=[],
#    # plot_width=int(self._figsize[0]),
#    # plot_height=int(self._figsize[1] * 10.0 / 12.0),
#    # y_axis_type="log",
#    # x_range=(
#    # 0 - self._body_width,
#    # (len(self._quotes.index) - 1) + self._body_width,
#    # ),
#    # y_range=self._ylim_from_price_range(),
#    # background_fill_color="#000000",
#    # border_fill_color="#000000",
#    # )
#
#    # self._plot_candlesticks(p_price, records=records)
#    # self._plot_indicators(
#    # lambda col, cl, al: p_price.line(
#    # np.arange(len(self._quotes.index)),
#    # self._quotes[col],
#    # line_width=self._linewidth,
#    # line_color=self._theme.get_color(cl),
#    # line_alpha=self._theme.get_alpha(al),
#    # )
#    # )
#
#    # if interactive:
#    # show(column(p_indicator, p_price))
#    # else:
#    # assert type(output) in (str, io.BytesIO, io.StringIO)
#    # if type(output) is io.BytesIO:
#    # html = file_html(column(p_indicator, p_price), CDN, "stocks price")
#    # cast(io.BytesIO, output).write(html.encode("utf-8"))
#    # elif type(output) is io.StringIO:
#    # html = file_html(column(p_indicator, p_price), CDN, "stocks price")
#    # cast(io.StringIO, output).write(html)
#    # elif type(output) is str:
#    # output_file(output)
#    # save(column(p_indicator, p_price))
