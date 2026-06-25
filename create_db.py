import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rollno TEXT UNIQUE NOT NULL,
    branch TEXT NOT NULL,
    cgpa REAL NOT NULL,
    backlogs INTEGER NOT NULL,
    email TEXT UNIQUE NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT UNIQUE NOT NULL,
    required_cgpa REAL NOT NULL,
    allowed_backlogs INTEGER NOT NULL,
    job_role TEXT NOT NULL,
    package_offered REAL NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS applications(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    company_id INTEGER,
    status TEXT DEFAULT 'Applied'
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")