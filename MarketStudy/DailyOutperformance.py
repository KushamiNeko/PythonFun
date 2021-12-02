# %%

import pandas as pd

# %%

df1 = pd.read_csv("data/DailyOutperformance/1.csv")
df2 = pd.read_csv("data/DailyOutperformance/2.csv")
df3 = pd.read_csv("data/DailyOutperformance/3.csv")

df = df1.append(df2).append(df3)
df = df.reset_index()
df

# %%

filter = df["Industry"].isna() & df["Sector"].isna()

df = df[~filter]
df

# %%

filter = df.loc[:, "Sector"].transform(lambda x: x.strip()) == ""

df = df[~filter]
df

# %%

sectors = df["Sector"].unique()
sectors

# %%

group = df.groupby(["Sector", "Industry"])
count = group.count()["Ticker"].sort_values(ascending=False)

for sector in sectors:
    filter = df.loc[:, "Sector"] == sector
    length = len(df[filter])

    print(f"{sector}:  {length}")
    print()

    for i, j in count.items():
        if i[0] == sector:
            print(f"    {i[1]}:  {j}")

    print()

# %%
