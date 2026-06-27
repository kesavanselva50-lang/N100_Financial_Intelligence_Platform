import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT
company_id,
year,
sales,
operating_profit,
opm_percentage
FROM profitandloss
""", conn)

logs = []

for _, row in df.iterrows():

    if row["sales"] == 0:
        continue

    calculated = (
        row["operating_profit"] /
        row["sales"]
    ) * 100

    difference = abs(
        calculated -
        row["opm_percentage"]
    )

    if difference > 1:

        logs.append([
            row["company_id"],
            row["year"],
            round(calculated, 2),
            row["opm_percentage"],
            round(difference, 2)
        ])

log_df = pd.DataFrame(
    logs,
    columns=[
        "company_id",
        "year",
        "calculated_opm",
        "source_opm",
        "difference"
    ]
)

log_df.to_csv(
    "output/opm_mismatch.csv",
    index=False
)

print(
    f"Logged {len(log_df)} OPM mismatches"
)

conn.close()