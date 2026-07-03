import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

cursor.execute(
    """
    SELECT COUNT(*)
    FROM financial_ratios
    """
)

print(
    "financial_ratios rows:",
    cursor.fetchone()[0]
)

cursor.execute(
    """
    SELECT COUNT(*)
    FROM companies
    """
)

print(
    "companies:",
    cursor.fetchone()[0]
)

conn.close()