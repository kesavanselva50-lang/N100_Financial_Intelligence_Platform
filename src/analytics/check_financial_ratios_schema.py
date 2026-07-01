import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(financial_ratios)")

print("\nfinancial_ratios table schema:\n")

for column in cursor.fetchall():
    print(column)

conn.close()