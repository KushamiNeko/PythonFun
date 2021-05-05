from abc import ABCMeta, abstractmethod
from typing import Optional

from matplotlib import axes, font_manager as fm


class Plotter(metaclass=ABCMeta):
    @abstractmethod
    def plot(self, ax: axes.Axes) -> None:
        raise NotImplementedError


class LinePlotter(Plotter, metaclass=ABCMeta):
    def __init__(
            self, line_color: str = "k", line_alpha: float = 1.0, line_width: float = 10.0
    ) -> None:
        self._line_color = line_color
        self._line_alpha = line_alpha
        self._line_width = line_width


class TextPlotter(Plotter, metaclass=ABCMeta):
    def __init__(
            self,
            font_color: str = "k",
            font_size: float = 10.0,
            font_src: Optional[str] = None,
            font_properties: Optional[fm.FontProperties] = None,
    ) -> None:
        self._font_color = font_color

        if font_properties is None:
            if font_src is None:
                self._font_properties = fm.FontProperties(size=font_size)
            else:
                self._font_properties = fm.FontProperties(
                        fname=font_src, size=font_size
                )
        else:
            self._font_properties = font_properties
