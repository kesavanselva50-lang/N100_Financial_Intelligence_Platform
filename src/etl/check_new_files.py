import pandas as pd

files = [
    "sectors.xlsx",
    "stock_prices.xlsx",
    "financial_ratios.xlsx",
    "peer_groups.xlsx",
    "market_cap.xlsx"
]

for file in files:

    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = pd.read_excel(
        f"data/raw/{file}",
        header=None
    )

    print(df.head(5))