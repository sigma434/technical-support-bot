import sqlite3
from config import DATABASE

dataname='qa.db'

def save_to_db(user_id, username, issue):
    conn = sqlite3.connect(dataname)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            issue TEXT
        )
    ''')
    
    # Сохраняем
    cursor.execute('''
        INSERT INTO messages (user_id, username, issue)
        VALUES (?, ?, ?)
    ''', (user_id, username, issue))
    
    conn.commit()
    conn.close()
