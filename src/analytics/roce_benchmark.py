import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    c.company_name,
    c.roce_percentage,
    s.broad_sector
FROM companies c
JOIN sectors s
ON c.id = s.company_id
"""

df = pd.read_sql(query, conn)

for _, row in df.iterrows():

    if row["broad_sector"] == "Financials":
        benchmark = "Sector Relative"

    elif row["roce_percentage"] >= 15:
        benchmark = "Good"

    else:
        benchmark = "Needs Improvement"

    print(
        f"{row['company_name']} -> {benchmark}"
    )

conn.close()