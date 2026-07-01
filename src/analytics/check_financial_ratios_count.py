import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM financial_ratios")
count = cursor.fetchone()[0]

print(f"Total rows in financial_ratios: {count}")

conn.close()