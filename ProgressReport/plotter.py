import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm

from typing import List, Tuple


_FONTS = sorted(fm.findSystemFonts(fontpaths=None), key=lambda x: os.path.basename(x))

_FONT_FILE = "Roboto-Light"

_FONT_SRC = None
for font in _FONTS:
    if _FONT_FILE in font:
        _FONT_SRC = font
        break


def get_font(font_size: float) -> fm.FontProperties:
    return fm.FontProperties(fname=_FONT_SRC, size=font_size)


def plot_progress(
    progress: List[float],
    labels: List[str],
    color: str,
    fig_title: str = None,
    bar_width: float = 0.5,
    y_text_offset: float = 1.0,
    figsize: Tuple[int, int] = (8, 6),
    output_file: str = "output.png"
) -> None:

    assert len(progress) == len(labels)

    fig, ax = plt.subplots(
        figsize=figsize,
        facecolor="w",
        tight_layout=True,
    )

    for i in range(len(progress)):
        x = i
        y = progress[i] + y_text_offset
        s = progress[i]

        ax.text(
            x,
            y,
            f"{s}%",
            ha="center",
            va="bottom",
            fontproperties=get_font(12),
        )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_xlim(left=-1, right=len(progress))
    ax.set_ylim(bottom=0, top=110)

    ax.set_xticks(range(len(progress)), labels=labels, fontproperties=get_font(14))

    ys = [y for y in range(101) if y % 20 == 0]
    ax.set_yticks(ys, labels=[f"{y}%" for y in ys], fontproperties=get_font(14))

    # ax.set_ylabel("Progress(%)", fontproperties=get_font(14))

    ax.bar(np.arange(len(progress)), progress, width=bar_width, color=color)

    ax.autoscale_view()

    if fig_title is not None:
        plt.title(fig_title, fontproperties=get_font(24))

    plt.savefig(output_file, facecolor="w", dpi=300)

