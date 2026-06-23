import pandas as pd

df = pd.read_excel(
    "data/raw/profitandloss.xlsx",
    header=1
)

adani = df[df["company_id"] == "ADANIPORTS"]

print(adani[["company_id", "year"]])

print("\nTotal rows:", len(adani))