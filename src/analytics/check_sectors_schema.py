import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(sectors)")

for row in cursor.fetchall():
    print(row)

conn.close()