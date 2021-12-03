# %%

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager as fm


# %%

_FONTS = sorted(fm.findSystemFonts(fontpaths=None), key=lambda x: os.path.basename(x))

_FONT_FILE = "Roboto-Light"

_FONT_SRC = None
for font in _FONTS:
    if _FONT_FILE in font:
        _FONT_SRC = font
        break


def get_font(font_size: float) -> fm.FontProperties:
    return fm.FontProperties(fname=_FONT_SRC, size=font_size)


_FONTS

# %%

# progress = [85, 95, 95, 95]
progress = [10, 95, 95, 95]

labels = ["Controllers", "services", "Repositories", "Models"]

# color = "#1976D2"
color = "#FFA000"

# assert len(progress) == len(test_progress)
assert len(progress) == len(labels)

width = 0.425
text_offset_y = 1

fig, ax = plt.subplots(
    figsize=(8, 6),
    facecolor="w",
    tight_layout=True,
)

for i in range(len(progress)):
    x_progress = i
    # x_progress = i - (width / 2)
    # x_test_progress = i + (width / 2)

    y_progress = progress[i] + text_offset_y
    # y_test_progress = test_progress[i] + text_offset_y

    ax.text(
        x_progress,
        y_progress,
        f"{progress[i]}%",
        ha="center",
        va="bottom",
        fontproperties=get_font(12),
    )
    # ax.text(
    #     x_test_progress,
    #     y_test_progress,
    #     f"{test_progress[i]}%",
    #     ha="center",
    #     va="bottom",
    #     fontproperties=get_font(12),
    # )

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

ax.set_xlim(left=-1, right=len(progress))
ax.set_ylim(bottom=0, top=110)

ax.set_xticks(range(len(progress)), labels=labels, fontproperties=get_font(14))

ys = [y for y in range(101) if y % 20 == 0]
ax.set_yticks(ys, labels=[f"{y}%" for y in ys], fontproperties=get_font(14))

# ax.set_ylabel("Progress(%)", fontproperties=get_font(14))

ax.bar(np.arange(len(progress)), progress, width=width, color=color)

# ax.bar(np.arange(len(progress)) - (width / 2), progress, width=width, label="coding")

# ax.bar(
#     np.arange(len(test_progress)) + (width / 2),
#     test_progress,
#     width=width,
#     label="testing",
# )

# plt.legend(prop=get_font(12), frameon=False, loc="upper left")
plt.savefig("test.png", facecolor="w", dpi=300)

ax.autoscale_view()

# %%
