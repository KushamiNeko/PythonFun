# %%

import plotter

# %%

progress = [90, 90, 85, 85]
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

progress = [15]
labels = ["View Models"]
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
