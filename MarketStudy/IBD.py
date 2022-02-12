# %%

with open("data/IBD/IBD.txt", "r") as f:
    content = f.read() 

symbols = content.split("\n")

# %%

symbols = [symbol.strip() for symbol in symbols]

# %%

with open("export/IBD/ibd.txt", "w") as f:
    f.write(",".join(set(symbols)))


# %%