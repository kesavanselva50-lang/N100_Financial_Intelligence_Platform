import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "ABB",
    "TCS",
    "INFY",
    "RELIANCE",
    "HDFCBANK"
]

for company in companies:

    print("=" * 60)

    print(company)

    df = pd.read_sql(
        f"""
        SELECT
            company_id,
            year,
            return_on_equity_pct,
            debt_to_equity,
            net_profit_margin_pct
        FROM financial_ratios
        WHERE company_id='{company}'
        LIMIT 5
        """,
        conn
    )

    print(df)

conn.close()