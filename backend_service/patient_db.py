
import sqlite3

DB_PATH = 'C:/Users/HP/Documents/GitHub/hackathon-demo-assist/backend_service/queries.db'

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
