# %%

import pandas as pd

# %%

df = pd.read_csv("data/WeeklyScreen/1.csv")
df

# %%

symbols = df.loc[0:249, "Ticker"]
output = ",".join(symbols)

output

# %%

with open("export/WeeklyScreen/output.txt", "w") as f:
    f.write(output)
