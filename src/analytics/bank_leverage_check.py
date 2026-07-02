import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    f.company_id,
    s.broad_sector,
    f.debt_to_equity
FROM financial_ratios f
JOIN sectors s
ON f.company_id = s.company_id
"""

df = pd.read_sql(query, conn)

df["high_leverage_flag"] = (
    (df["debt_to_equity"] > 5) &
    (df["broad_sector"] != "Financials")
)

print(df[[
    "company_id",
    "broad_sector",
    "debt_to_equity",
    "high_leverage_flag"
]].head(20))

conn.close()