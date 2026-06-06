import sqlite3
from config import DATABASE

dataname=DATABASE

conn = sqlite3.connect(dataname)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS specialist_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        username TEXT,
        department TEXT,
        issue TEXT,
        status TEXT,
        created_at TEXT
    )
''')



conn.commit()
conn.close()
