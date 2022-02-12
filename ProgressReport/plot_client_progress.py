# %%

import plotter

# %%

progress = [95, 95, 95, 95]
labels = ["Components", "Layouts", "Pages", "Services"]
color = "#1976D2"

# %%

plotter.plot_progress(
    progress=progress,
    labels=labels,
    color=color,
    fig_title="Client Coding",
    output_file="client_coding",
)

# %%

progress = [95, 95]
labels = ["View Models", "Processors"]
color = "#FFA000"

# %%

plotter.plot_progress(
    progress=progress,
    labels=labels,
    color=color,
    fig_title="Client Testing",
    output_file="client_testing",
)

# %%
