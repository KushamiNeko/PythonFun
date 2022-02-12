# %%

import pandas as pd

# %%

# folder = "Tech Focus"
folder = "Value Focus"

df1 = pd.read_csv(f"data/{folder}/1.csv")
df = df1

# df2 = pd.read_csv(f"data/{folder}/2.csv")
# df = df1.append(df2)

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

# df = df.sort_values("Sales 1-Year Chg (%)", ascending=False)
df = df.sort_values("Sales 1Y Chg (%)", ascending=False)
df

# %%

tickers = df.loc[:, "Ticker"]
exchanges = df.loc[:, "Exchange"]

symbols = []
for i in range(len(tickers)):
    ticker = tickers.iloc[i]
    exchange = exchanges.iloc[i]

    if exchange != "NYSE" and exchange != "NASDAQ":
        print(f"{exchange}:{ticker}")
        continue

    symbols.append(f"{exchanges.iloc[i]}:{tickers.iloc[i]}")

output = ",".join(symbols)

# output

# %%

with open(f"export/{folder}/output.txt", "w") as f:
    f.write(output)

# %%
