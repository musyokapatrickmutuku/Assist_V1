# backend_service/main_simple.py
# Simplified backend for MVP demo - removes LangGraph complexity

import os
import uuid
import sqlite3
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# Simple models
class SimpleQuery(BaseModel):
    patient_id: str
    query: str
    urgency: Optional[str] = "low"

class DoctorResponse(BaseModel):
    question_id: str
    doctor_response: str
    status: str

# Initialize FastAPI app
app = FastAPI(
    title="Assist AI - Simplified Backend",
    description="Simple backend for MVP demo",
    version="1.0.0-simple"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
def get_simple_db():
    """Get database connection with simple schema"""
    conn = sqlite3.connect('simple_queries.db')
    conn.row_factory = sqlite3.Row
    
    # Create simple table if not exists
    conn.execute("""
        CREATE TABLE IF NOT EXISTS simple_queries (
            id TEXT PRIMARY KEY,
            patient_id TEXT NOT NULL,
            patient_name TEXT,
            question TEXT NOT NULL,
            doctor_response TEXT,
            status TEXT DEFAULT 'pending',
            urgency TEXT DEFAULT 'low',
            date TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn

# Patient name mapping for demo
PATIENT_NAMES = {
    "P001": "Sarah Johnson",
    "P002": "Michael Thompson", 
    "P003": "Carlos Rodriguez",
    "P004": "Priya Patel",
    "P005": "Eleanor Williams"
}

# API Endpoints
@app.get("/")
async def root():
    return {"message": "Simplified Assist AI Backend is running"}

@app.post("/simple_query/")
async def submit_simple_query(query: SimpleQuery):
    """Submit a simple patient query"""
    try:
        conn = get_simple_db()
        cursor = conn.cursor()
        
        query_id = str(uuid.uuid4())
        patient_name = PATIENT_NAMES.get(query.patient_id, "Unknown Patient")
        
        cursor.execute("""
            INSERT INTO simple_queries 
            (id, patient_id, patient_name, question, status, urgency, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            query_id,
            query.patient_id,
            patient_name,
            query.query,
            'pending',
            query.urgency,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": "Question submitted successfully",
            "query_id": query_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error submitting query: {str(e)}")

@app.get("/patient_queries/{patient_id}")
async def get_patient_queries(patient_id: str):
    """Get all queries for a specific patient"""
    try:
        conn = get_simple_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM simple_queries 
            WHERE patient_id = ? 
            ORDER BY date DESC
        """, (patient_id,))
        
        queries = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return queries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching queries: {str(e)}")

@app.get("/pending_questions/")
async def get_pending_questions():
    """Get all pending questions for doctors"""
    try:
        conn = get_simple_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM simple_queries 
            WHERE status = 'pending' 
            ORDER BY 
                CASE urgency 
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2 
                    ELSE 3 
                END,
                date ASC
        """)
        
        questions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return questions
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pending questions: {str(e)}")

@app.post("/send_response/")
async def send_doctor_response(response: DoctorResponse):
    """Doctor sends response to patient question"""
    try:
        conn = get_simple_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE simple_queries 
            SET doctor_response = ?, status = ?
            WHERE id = ?
        """, (response.doctor_response, response.status, response.question_id))
        
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Question not found")
        
        conn.commit()
        conn.close()
        
        return {
            "status": "success",
            "message": "Response sent to patient"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending response: {str(e)}")

@app.get("/doctor_stats/")
async def get_doctor_stats():
    """Get simple doctor statistics"""
    try:
        conn = get_simple_db()
        cursor = conn.cursor()
        
        # Count today's questions
        today = datetime.now().date().isoformat()
        cursor.execute(
            "SELECT COUNT(*) FROM simple_queries WHERE date LIKE ?", 
            (f"{today}%",)
        )
        today_count = cursor.fetchone()[0]
        
        # Count responses
        cursor.execute(
            "SELECT COUNT(*) FROM simple_queries WHERE status = 'answered' AND date LIKE ?", 
            (f"{today}%",)
        )
        responses_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "today": today_count,
            "responses": responses_count,
            "avg_time": "2.1 hrs"  # Static for demo
        }
        
    except Exception as e:
        return {"today": 0, "responses": 0, "avg_time": "N/A"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0-simple"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
