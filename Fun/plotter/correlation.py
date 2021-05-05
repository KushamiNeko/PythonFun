from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
from matplotlib import axes, font_manager as fm


def label_simplify(label: str, length_limit: int = 50) -> str:
    if len(label) > length_limit:
        return (
            f"{label[: int(length_limit / 2.0)]}.....{label[-int(length_limit / 2.0):]}"
        )
    else:
        return label


def correlation(
    xs: np.ndarray,
    ys: np.ndarray,
    ax: Optional[axes.Axes] = None,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    labelsize: int = 14,
    label_length_limit: int = 50,
    pointsize: int = 50,
    linewidth: int = 2,
    font_src: Optional[str] = None,
) -> None:
    if font_src is not None:
        prop = fm.FontProperties(fname=font_src, size=labelsize)
    else:
        prop = fm.FontProperties(size=labelsize)

    maxy = ys.max()
    miny = ys.min()

    ry = maxy - miny
    ryratio = 0.2

    mask = ~np.isnan(xs.reset_index(drop=True)) & ~np.isnan(ys.reset_index(drop=True))

    tau, p = stats.kendalltau(
        xs[mask].astype(np.float),
        ys[mask].astype(np.float),
    )

    s, i, _, _, _ = stats.linregress(xs[mask], ys[mask])
    xl = np.linspace(xs.min(), xs.max())

    if ax is None:
        ax = plt.gca()

    ax.scatter(xs.values, ys.values, s=pointsize, color="k")
    ax.plot(xl, xl * s + i, color="k", linewidth=linewidth)

    if maxy != miny and maxy > miny:
        ax.set_ylim(
            top=maxy + (ry * ryratio),
            bottom=min(miny, (xs.min() * s) + i) - (ry * (ryratio / 2.0)),
        )

    ylim_min, ylim_max = ax.get_ylim()
    ylim_mean = (ylim_max + ylim_min) / 2.0
    ylim_range = ylim_max - ylim_min

    minx, maxx = ax.get_xlim()
    rx = maxx - minx
    rxratio = 0.05

    tx = maxx - (rx * rxratio)
    ha = "right"
    if (
        ys[xs < ((xs.max() + xs.min()) / 2.0)].max()
        < ys[xs > ((xs.max() + xs.min()) / 2.0)].max()
    ):
        tx = minx + (rx * rxratio)
        ha = "left"

    ax.text(
        tx,
        max(maxy + (ry * (ryratio / 2.0)), ylim_mean + (ylim_range * 0.4)),
        s=f"P: {p:.3f}\nTAU: {tau:.3f}",
        color="k",
        ha=ha,
        va="bottom",
        fontproperties=prop,
    )

    if xlabel is not None:
        ax.set_xlabel(label_simplify(xlabel, label_length_limit), fontproperties=prop)

    if ylabel is not None:
        ax.set_ylabel(label_simplify(ylabel, label_length_limit), fontproperties=prop)
