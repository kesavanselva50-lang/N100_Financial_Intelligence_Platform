import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT
    id,
    company_name,
    roce_percentage
FROM companies
ORDER BY company_name;
"""

df = pd.read_sql(query, conn)

print(df.head(10))

conn.close()