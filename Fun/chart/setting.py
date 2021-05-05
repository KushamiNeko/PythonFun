from Fun.chart.base import CHART_SIZE, LARGE_CHART, MEDIUM_CHART, SMALL_CHART


class Setting:
    def __init__(self, chart_size: CHART_SIZE = LARGE_CHART) -> None:
        self._chart_size = chart_size

    def chart_size(self) -> CHART_SIZE:
        return self._chart_size

    def set_chart_size(self, chart_size: CHART_SIZE) -> None:
        self._chart_size = chart_size

    def linewidth(self, multiplier: float = 1.0) -> float:
        if self._chart_size == SMALL_CHART:
            return 1.0 * multiplier
        elif self._chart_size == MEDIUM_CHART:
            return 1.2 * multiplier
        elif self._chart_size == LARGE_CHART:
            return 2.0 * multiplier
        else:
            raise ValueError("invalid chart size")

    def tick_fontsize(self, multiplier: float = 1.0) -> float:
        if self._chart_size == SMALL_CHART:
            return 5.4 * multiplier
        elif self._chart_size == MEDIUM_CHART:
            return 9.0 * multiplier
        elif self._chart_size == LARGE_CHART:
            return 15.0 * multiplier
        else:
            raise ValueError("invalid chart size")

    def text_fontsize(self, multiplier: float = 1.0) -> float:
        if self._chart_size == SMALL_CHART:
            return 5.4 * multiplier
        elif self._chart_size == MEDIUM_CHART:
            return 9 * multiplier
        elif self._chart_size == LARGE_CHART:
            return 15.0 * multiplier
        else:
            raise ValueError("invalid chart size")

    def shadow_width(self, multiplier: float = 1.0) -> float:
        # line plotter
        # if self._chart_size == SMALL_CHART:
        # return 0.72 * multiplier
        # elif self._chart_size == MEDIUM_CHART:
        # return 1.2 * multiplier
        # elif self._chart_size == LARGE_CHART:
        # return 2 * multiplier
        # else:
        # raise ValueError("invalid chart size")

        # rectangle plotter
        return 0.125

    def body_width(self, multiplier: float = 1.0) -> float:
        # line plotter
        # if self._chart_size == SMALL_CHART:
        #     return 2.34 * multiplier
        # elif self._chart_size == MEDIUM_CHART:
        #     return 3.9 * multiplier
        # elif self._chart_size == LARGE_CHART:
        #     return 6.5 * multiplier
        # else:
        #     raise ValueError("invalid chart size")

        # rectangle plotter
        return 0.6
