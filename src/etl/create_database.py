import sqlite3

conn = sqlite3.connect("nifty100.db")

print("Database created successfully")

conn.close()