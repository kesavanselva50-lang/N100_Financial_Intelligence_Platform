import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    c.id,
    c.company_name,
    s.broad_sector,
    s.sub_sector
FROM companies c
JOIN sectors s
ON c.id = s.company_id
WHERE s.broad_sector = 'Financials'
ORDER BY c.company_name;
"""

df = pd.read_sql(query, conn)

print(df)

print(f"\nTotal Financial Companies: {len(df)}")

conn.close()