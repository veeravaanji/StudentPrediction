import sqlite3

# Connect to database (creates it if it doesn't exist)
conn = sqlite3.connect("student.db")

cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT,
    study_hours REAL,
    attendance REAL,
    past_exam_score REAL,
    parent_education TEXT,
    internet_access TEXT,
    extracurricular TEXT,
    prediction TEXT
)
""")

conn.commit()
conn.close()

print("Database and table created successfully!")