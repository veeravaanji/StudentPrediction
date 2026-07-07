#import sqlite3

#conn = sqlite3.connect("student.db")
#cursor = conn.cursor()

#cursor.execute("""
#CREATE TABLE IF NOT EXISTS predictions (

 #   id INTEGER PRIMARY KEY AUTOINCREMENT,

  #  student_name TEXT,
   # student_id TEXT,

    #gender TEXT,

    #study_hours REAL,
    #attendance REAL,
    #sleep_hours REAL,

    #past_exam_score REAL,

    #internet_access TEXT,
    #extracurricular TEXT,

   # prediction TEXT,
    #confidence REAL,

    #date TEXT,
    #time TEXT

#)
#""")

#conn.commit()
#conn.close()

#print("Database Created Successfully")