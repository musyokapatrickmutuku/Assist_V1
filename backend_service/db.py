
import sqlite3

def init_db():
    conn = sqlite3.connect('C:/Users/HP/Documents/GitHub/hackathon-demo-assist/backend_service/queries.db')
    cursor = conn.cursor()
    
    # Create table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS queries (
        id TEXT PRIMARY KEY,
        timestamp TEXT NOT NULL,
        patient_id TEXT NOT NULL,
        original_query TEXT NOT NULL,
        ai_response TEXT,
        doctor_final_response TEXT,
        status TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
