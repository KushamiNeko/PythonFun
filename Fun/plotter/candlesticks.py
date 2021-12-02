import numpy as np
import pandas as pd
from Fun.plotter.plotter import Plotter
from matplotlib import axes, patches
from matplotlib.collections import PatchCollection


class CandleSticks(Plotter):
    def __init__(
            self,
            quotes: pd.DataFrame,
            shadow_width: float,
            body_width: float,
            color_up: str,
            color_down: str,
            color_unchanged: str,
            zorder: int = 5,
    ):
        self._quotes = quotes
        self._shadow_width = shadow_width
        self._body_width = body_width

        self._minimum_height = self._minimum_height()

        self._color_up = color_up
        self._color_down = color_down
        self._color_unchanged = color_unchanged

        self._zorder = zorder

    def _minimum_height(self) -> float:
        ratio = 0.001
        mn = np.amin(self._quotes.loc[:, "low"])
        mx = np.amax(self._quotes.loc[:, "high"])
        r = mx - mn

        return r * ratio

    def plot(self, ax: axes.Axes) -> None:

        length = len(self._quotes)

        bodies = np.ndarray(shape=length, dtype=object)
        shadows = np.ndarray(shape=length, dtype=object)

        for index, df in enumerate(self._quotes.itertuples()):

            p_open = df.open
            p_high = df.high
            p_low = df.low
            p_close = df.close

            p_shadow_top = p_high
            p_shadow_bottom = p_low

            p_body_top: float
            p_body_bottom: float

            if p_open > p_close:
                p_body_top = p_open
                p_body_bottom = p_close
            else:
                p_body_top = p_close
                p_body_bottom = p_open

            assert p_body_top is not None
            assert p_body_bottom is not None

            if abs(p_open - p_close) < self._minimum_height:
                mid = (p_open + p_close) / 2.0
                mid_height = self._minimum_height / 2.0
                p_body_top = mid + mid_height
                p_body_bottom = mid - mid_height

            if abs(p_shadow_top - p_shadow_bottom) < self._minimum_height:
                mid = (p_shadow_top + p_shadow_bottom) / 2.0
                mid_height = self._minimum_height / 2.0
                p_shadow_top = mid + mid_height
                p_shadow_bottom = mid - mid_height

            color = self._color_unchanged

            if p_close > p_open:
                color = self._color_up
            elif p_close < p_open:
                color = self._color_down

            shadow = patches.Rectangle(
                    xy=(index - (self._shadow_width / 2.0), p_shadow_bottom),
                    width=self._shadow_width,
                    height=p_shadow_top - p_shadow_bottom,
                    facecolor=color,
                    edgecolor=color,
            )

            body = patches.Rectangle(
                    xy=(index - (self._body_width / 2.0), p_body_bottom),
                    width=self._body_width,
                    height=p_body_top - p_body_bottom,
                    facecolor=color,
                    edgecolor=color,
            )

            bodies[index] = body
            shadows[index] = shadow

        ax.add_collection(PatchCollection(bodies, match_original=True, zorder=self._zorder))
        ax.add_collection(PatchCollection(shadows, match_original=True, zorder=self._zorder))
