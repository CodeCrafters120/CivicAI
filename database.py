import sqlite3
import uuid

def store_complaint(user_id, text, category, department):
    conn = sqlite3.connect("complaints.db")
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS complaints (
        id TEXT, user_id TEXT, text TEXT, category TEXT, department TEXT, status TEXT
    )""")
    complaint_id = str(uuid.uuid4())[:8]
    cur.execute("INSERT INTO complaints VALUES (?, ?, ?, ?, ?, ?)", 
                (complaint_id, user_id, text, category, department, "Received"))
    conn.commit()
    conn.close()
    return complaint_id
