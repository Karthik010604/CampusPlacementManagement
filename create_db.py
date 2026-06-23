# create_db.py

import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    rollno TEXT,
    branch TEXT,
    cgpa REAL,
    backlogs INTEGER,
    email TEXT
)
""")

conn.commit()
conn.close()

print("Database Created")