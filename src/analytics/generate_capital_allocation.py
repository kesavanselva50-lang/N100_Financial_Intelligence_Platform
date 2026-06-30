import sqlite3
import pandas as pd

from src.analytics.cashflow_kpis import capital_allocation_pattern

# Connect to database
conn = sqlite3.connect("nifty100.db")

# Read cashflow table
df = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

output = []

for _, row in df.iterrows():

    label = capital_allocation_pattern(
        row["operating_activity"],
        row["investing_activity"],
        row["financing_activity"]
    )

    output.append({
        "company_id": row["company_id"],
        "year": row["year"],
        "cfo_sign": "+" if row["operating_activity"] >= 0 else "-",
        "cfi_sign": "+" if row["investing_activity"] >= 0 else "-",
        "cff_sign": "+" if row["financing_activity"] >= 0 else "-",
        "pattern_label": label
    })

result = pd.DataFrame(output)

result.to_csv(
    "output/capital_allocation.csv",
    index=False
)

print(f"Generated {len(result)} rows")
print("Saved to output/capital_allocation.csv")

conn.close()