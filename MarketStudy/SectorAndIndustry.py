# %%

import pandas as pd

# %%

df1 = pd.read_csv("data/SectorAndIndustry/100%/1.csv")
df2 = pd.read_csv("data/SectorAndIndustry/100%/2.csv")
df3 = pd.read_csv("data/SectorAndIndustry/100%/3.csv")
df = df1.append(df2).append(df3)

# df1 = pd.read_csv("data/SectorAndIndustry/200%/1.csv")
# df2 = pd.read_csv("data/SectorAndIndustry/200%/2.csv")
# df = df1.append(df2)

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

for sector in sectors:
    print(f"{sector}:")
    print()

    # filter = df.loc[:, "Sector"] == "Technology"
    filter = df.loc[:, "Sector"] == sector

    cols = [col for col in df.columns if "sales" in col.lower() or "eps" in col.lower()]
    cols.sort()

    cols.append("3-Year Return")

    data = df[filter][cols]

    for col in cols:
        d = data[col].transform(lambda x: x.replace("%", "").strip()).transform(lambda x: 0 if x == "-" else x).astype(float)
        median = d.median()
        mean = d.mean()

        print(f"    {col}:  {d.quantile(0.25):.2f}%  {median:.2f}%  {d.quantile(0.75):.2f}%")
    
    print()

# %%

group = df.groupby(["Sector", "Industry"])
count = group.count()["Ticker"].sort_values(ascending=False)

for sector in sectors:
    print(sector)
    print()

    for i, j in count.items():
        if i[0] == sector:
            print(f"{i[1]}:  {j}")

    print()


# %%
