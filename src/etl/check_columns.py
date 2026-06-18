import pandas as pd

files = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
]

for file in files:

    print("\n")
    print("=" * 60)
    print(file)
    print("=" * 60)

    df = pd.read_excel(
        f"data/raw/{file}",
        header=1
    )

    print(df.columns.tolist())