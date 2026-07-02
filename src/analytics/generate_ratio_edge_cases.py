import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

companies = pd.read_sql("""
SELECT
    id,
    company_name,
    roce_percentage,
    roe_percentage
FROM companies
""", conn)

ratios = pd.read_sql("""
SELECT
    company_id,
    return_on_equity_pct
FROM financial_ratios
GROUP BY company_id
""", conn)

df = companies.merge(
    ratios,
    left_on="id",
    right_on="company_id",
    how="left"
)

with open("output/ratio_edge_cases.log", "w") as f:

    for _, row in df.iterrows():

        if pd.isna(row["return_on_equity_pct"]):
            continue

        diff = abs(
            row["roe_percentage"] -
            row["return_on_equity_pct"]
        )

        if diff > 5:

            f.write(
                f"{row['id']} - {row['company_name']}\n"
            )

            f.write(
                f"Source ROE : {row['roe_percentage']}\n"
            )

            f.write(
                f"Computed ROE : {row['return_on_equity_pct']}\n"
            )

            f.write(
                f"Difference : {diff:.2f}%\n"
            )

            f.write(
                "Category : Formula Difference\n"
            )

            f.write("-" * 50 + "\n")

print("ratio_edge_cases.log generated")

conn.close()