# %%

import plotter

# %%

progress = [95, 95]
labels = ["DTOs", "Services"]
color = "#1976D2"

# %%

plotter.plot_progress(
    progress=progress,
    labels=labels,
    color=color,
    fig_title="Shared Coding",
    output_file="shared_coding",
)

# %%
