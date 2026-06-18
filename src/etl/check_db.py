import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

cursor.execute(
    "SELECT COUNT(*) FROM companies"
)

count = cursor.fetchone()[0]

print("Companies:", count)

conn.close()