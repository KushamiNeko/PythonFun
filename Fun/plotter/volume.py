import numpy as np
import pandas as pd
from Fun.plotter.plotter import Plotter
from matplotlib import axes, patches
from matplotlib.collections import PatchCollection


class Volume(Plotter):
    def __init__(
        self,
        quotes: pd.DataFrame,
        body_width: float,
        color_up: str,
        color_down: str,
        color_unchanged: str,
        alpha: float = 0.35,
        chart_height_ratio: float = 0.25,
        quantile_clamp_ratio: float = 0.95,
        plot_average: bool = False,
        average_n: int = 20,
        line_width: float = 1.5,
        line_alpha: float = 0.025,
    ):

        self._quotes = quotes

        self._body_width = body_width

        self._color_up = color_up
        self._color_down = color_down
        self._color_unchanged = color_unchanged
        self._alpha = alpha

        self._chart_height_ratio = chart_height_ratio
        self._quantile_clamp_ratio = quantile_clamp_ratio

        self._plot_average = plot_average
        self._average_n = average_n
        self._line_width = line_width
        self._line_alpha = line_alpha

    def plot(self, ax: axes.Axes) -> None:
        volumes = self._quotes.get("volume")
        if volumes is None:
            return

        mn, mx = ax.get_ylim()

        h = np.amax(self._quotes.loc[:, "high"])
        l = np.amin(self._quotes.loc[:, "low"])

        lh = np.amax(self._quotes.iloc[-30:].loc[:, "high"])
        ll = np.amin(self._quotes.iloc[-30:].loc[:, "low"])

        pos_top = False
        if abs(l - ll) > abs(h - lh):
            pos_top = False
        else:
            pos_top = True

        # max_height = (mx - mn) * self._chart_height_ratio

        nx, ny = ax.transData.inverted().transform_point(
            (0, int(1080 * self._chart_height_ratio))
        )
        ny = min(max(ny, mn), mx)

        max_height = ny - mn

        # volumes_max = volumes.max()
        volumes_max = volumes.quantile(self._quantile_clamp_ratio)
        volumes = volumes.clip(upper=volumes_max)

        volumes = ((volumes / volumes_max)) * max_height
        # volumes = ((volumes / volumes_max)) * (max_height - mn)
        # volumes += mn

        # interests = self._quotes.get("open interest")

        # if interests is not None:
        # interests = ((interests / interests.max())) * max_height

        length = len(self._quotes)

        bodies = np.ndarray(shape=length, dtype=object)

        xs = np.arange(length)

        for index, df in enumerate(self._quotes.itertuples()):

            p_open = df.open
            p_close = df.close

            color = self._color_unchanged

            if p_close > p_open:
                color = self._color_up
            elif p_close < p_open:
                color = self._color_down

            if not pos_top:
                body = patches.Rectangle(
                    xy=(index - (self._body_width / 2.0), mn),
                    width=self._body_width,
                    # height=volumes.iloc[index] - mn,
                    height=volumes.iloc[index],
                    facecolor=color,
                    edgecolor=color,
                    alpha=self._alpha,
                )

                if self._plot_average:
                    ax.plot(
                        xs,
                        (mn + volumes).rolling(self._average_n).mean(),
                        color=self._color_unchanged,
                        alpha=self._line_alpha,
                        linewidth=self._line_width,
                    )

                # ax.plot(
                # xs,
                # (mn + interests),
                # color="r",
                # alpha=self._alpha,
                # linewidth=self._line_width,
                # )

            else:
                body = patches.Rectangle(
                    xy=(index - (self._body_width / 2.0), mx),
                    width=self._body_width,
                    # height=volumes.iloc[index] - mn,
                    height=-volumes.iloc[index],
                    facecolor=color,
                    edgecolor=color,
                    alpha=self._alpha,
                )

                if self._plot_average:
                    ax.plot(
                        xs,
                        (mx - volumes).rolling(self._average_n).mean(),
                        color=self._color_unchanged,
                        alpha=self._line_alpha,
                        linewidth=self._line_width,
                    )

                # ax.plot(
                # xs,
                # (mx - interests),
                # color="r",
                # alpha=self._alpha,
                # linewidth=self._line_width,
                # )

            bodies[index] = body

        ax.add_collection(
            PatchCollection(
                bodies,
                match_original=True,
                zorder=3,
            ),
        )
