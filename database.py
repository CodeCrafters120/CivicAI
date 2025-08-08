import sqlite3
import os

# Safe path for deployment (inside app directory)
DB_PATH = os.path.join(os.path.dirname(__file__), "complaints.db")

# Connect to SQLite database
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    complaint TEXT,
    category TEXT,
    language TEXT,
    status TEXT
)
""")
conn.commit()

# Function to insert a complaint
def insert_complaint(complaint, category, language, status="Pending"):
    cursor.execute("""
    INSERT INTO complaints (complaint, category, language, status)
    VALUES (?, ?, ?, ?)
    """, (complaint, category, language, status))
    conn.commit()
