import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("nifty100.db")

tables = {
    "profitandloss": ("profitandloss.xlsx", 1),
    "balancesheet": ("balancesheet.xlsx", 1),
    "cashflow": ("cashflow.xlsx", 1),
    "analysis": ("analysis.xlsx", 1),
    "documents": ("documents.xlsx", 1),
    "prosandcons": ("prosandcons.xlsx", 1),

    "sectors": ("sectors.xlsx", 0),
    "stock_prices": ("stock_prices.xlsx", 0),
    "financial_ratios": ("financial_ratios.xlsx", 0),
    "peer_groups": ("peer_groups.xlsx", 0),
    "market_cap": ("market_cap.xlsx", 0)
}

audit = []

for table, (file, header_row) in tables.items():

    print(f"\nLoading {table}...")

    df = pd.read_excel(
        f"data/raw/{file}",
        header=header_row
    )

    original_rows = len(df)

    # Remove duplicate company-year records
    if (
        table in [
            "profitandloss",
            "balancesheet",
            "cashflow"
        ]
        and "company_id" in df.columns
        and "year" in df.columns
    ):
        df = df.drop_duplicates(
            subset=["company_id", "year"]
        )

    rows_loaded = len(df)
    rows_rejected = original_rows - rows_loaded

    # Load table
    df.to_sql(
        table,
        conn,
        if_exists="replace",
        index=False
    )

    audit.append([
        table,
        rows_loaded,
        rows_rejected
    ])

    print(
        f"Loaded: {rows_loaded} | Rejected: {rows_rejected}"
    )

# Create audit report
audit_df = pd.DataFrame(
    audit,
    columns=[
        "table_name",
        "rows_loaded",
        "rows_rejected"
    ]
)

audit_df.to_csv(
    "output/load_audit.csv",
    index=False
)

print("\nload_audit.csv generated successfully")

conn.close()

print("\nAll tables loaded successfully")