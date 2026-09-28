import sqlite3

conn = sqlite3.connect("database.db")

try:
    conn.execute("ALTER TABLE complaints ADD COLUMN latitude TEXT")
except:
    print("latitude column already exists")

try:
    conn.execute("ALTER TABLE complaints ADD COLUMN longitude TEXT")
except:
    print("longitude column already exists")

conn.commit()
conn.close()

print("Database updated successfully")