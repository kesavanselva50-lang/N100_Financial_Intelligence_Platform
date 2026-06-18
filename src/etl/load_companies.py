import sqlite3
import pandas as pd

# Connect database
conn = sqlite3.connect("nifty100.db")

# Read Excel
df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

# Load into SQLite
df.to_sql(
    "companies",
    conn,
    if_exists="append",
    index=False
)

print(f"Loaded {len(df)} rows into companies table")

conn.close()