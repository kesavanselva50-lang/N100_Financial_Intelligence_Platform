import sqlite3
import pandas as pd

# Connect database
conn = sqlite3.connect("nifty100.db")

# Read Excel file
df = pd.read_excel(
    "data/raw/companies.xlsx",
    header=1
)

# Create/replace companies table
df.to_sql(
    "companies",
    conn,
    if_exists="replace",
    index=False
)

# Verify row count
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM companies")
count = cursor.fetchone()[0]

print(f"Loaded {len(df)} rows into companies table")
print(f"Companies table count: {count}")

conn.close()