import os
import uuid
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

# Import your project's modules
from schemas import PatientQueryInput, AgentState
from graph import app as langgraph_app
from patient_db import get_db_connection

# --- Environment Variable Loading & App Setup ---
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

if not os.getenv("DEEPSEEK_API_KEY"): 
    raise ValueError("DEEPSEEK_API_KEY not found in environment variables.")
if not os.getenv("DEEPSEEK_API_BASE"): 
    raise ValueError("DEEPSEEK_API_BASE not found in environment variables.")

app = FastAPI(
    title="Assist AI Backend Service",
    description="Processes patient queries and provides endpoints for review.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DoctorAction(BaseModel):
    new_status: str
    doctor_response: Optional[str] = None

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "Backend service is operational."}

@app.post("/process_query/", response_model=dict, tags=["Agent Processing"])
async def process_query(query_input: PatientQueryInput) -> dict:
    try:
        initial_state = {
            "patient_id": query_input.patient_id,
            "original_query": query_input.query,
            "uploaded_file_name": query_input.uploaded_file_name,
            "patient_data": None, "ai_response": None, "error_message": None,
            "final_response_to_patient": None, "safety_score": None,
            "confidence_score": None, "needs_urgent_review": None
        }
        final_state = langgraph_app.invoke(initial_state)
        if final_state.get("error_message"):
            raise HTTPException(status_code=400, detail=final_state["error_message"])
        
        # Query is already saved by the LangGraph workflow in save_query_for_review()
        # No need to save it again here to avoid duplicates
        
        return final_state
    except Exception as e:
        print(f"FATAL ERROR in /process_query/ endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected server error occurred: {e}")

@app.get("/pending_queries/", response_model=List[dict], tags=["Doctor Dashboard"])
async def get_pending_queries_endpoint():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM queries WHERE status = 'pending_review'")
    queries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return queries

@app.post("/update_query/{query_id}", tags=["Doctor Dashboard"])
async def update_query_endpoint(query_id: str, action: DoctorAction):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE queries SET status = ?, doctor_final_response = ? WHERE id = ?", (action.new_status, action.doctor_response, query_id))
    conn.commit()
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Query not found")
    conn.close()
    return {"status": "success", "message": "Query updated successfully"}

@app.get("/queries/by_patient/{patient_id}", response_model=List[dict], tags=["Patient Portal"])
async def get_patient_queries_endpoint(patient_id: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM queries WHERE patient_id = ?", (patient_id,))
    queries = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return queries