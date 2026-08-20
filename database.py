import sqlite3

connection = sqlite3.connect("students.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    course TEXT NOT NULL,
    age INTEGER NOT NULL
)
""")

connection.commit()
connection.close()

print("Database created successfully!")