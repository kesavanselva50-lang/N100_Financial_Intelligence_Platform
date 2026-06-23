import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = [
    "ABB",
    "ADANIENT",
    "ADANIPORTS",
    "APOLLOHOSP",
    "ASIANPAINT"
]

for company in companies:

    print("\n" + "=" * 50)
    print(company)
    print("=" * 50)

    company_count = pd.read_sql_query(
        f"SELECT COUNT(*) AS cnt FROM companies WHERE id='{company}'",
        conn
    )

    pnl_count = pd.read_sql_query(
        f"SELECT COUNT(*) AS cnt FROM profitandloss WHERE company_id='{company}'",
        conn
    )

    bs_count = pd.read_sql_query(
        f"SELECT COUNT(*) AS cnt FROM balancesheet WHERE company_id='{company}'",
        conn
    )

    cf_count = pd.read_sql_query(
        f"SELECT COUNT(*) AS cnt FROM cashflow WHERE company_id='{company}'",
        conn
    )

    print("Companies:", company_count["cnt"][0])
    print("Profit & Loss:", pnl_count["cnt"][0])
    print("Balance Sheet:", bs_count["cnt"][0])
    print("Cash Flow:", cf_count["cnt"][0])

conn.close()