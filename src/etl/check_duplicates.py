import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

query = """
SELECT company_id, year, COUNT(*) as cnt
FROM profitandloss
GROUP BY company_id, year
HAVING cnt > 1
LIMIT 20;
"""

df = pd.read_sql_query(query, conn)

print(df)

conn.close()