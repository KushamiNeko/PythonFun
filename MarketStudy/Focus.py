# %%

import pandas as pd

# %%

df1 = pd.read_csv("data/Focus/1.csv")
df2 = pd.read_csv("data/Focus/2.csv")

df = df1.append(df2)
df = df.reset_index()

df

# %%

filter = df["Industry"].isna()

df = df[~filter]
df

# %%

filter = df.loc[:, "Industry"].transform(lambda x: x.strip()) == ""

df = df[~filter]
df

# %%

df = df.reset_index()
df

# %%

symbols = df.loc[:, "Ticker"]
output = ",".join(symbols)

output

# %%

with open("export/Focus/output.txt", "w") as f:
    f.write(output)
