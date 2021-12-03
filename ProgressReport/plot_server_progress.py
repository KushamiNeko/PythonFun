# %%

import plotter

# %%

progress = [85, 95, 95, 95]
labels = ["Controllers", "services", "Repositories", "Models"]
color = "#1976D2"

# %%

plotter.plot_progress(
    progress=progress,
    labels=labels,
    color=color,
    fig_title="Server Coding",
    output_file="server_coding",
)

# %%

progress = [10, 95, 95, 95]
labels = ["Controllers", "services", "Repositories", "Models"]
color = "#FFA000"

# %%

plotter.plot_progress(
    progress=progress,
    labels=labels,
    color=color,
    fig_title="Server Testing",
    output_file="server_testing",
)

# %%
