# backend_service/schemas.py
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class PatientQueryInput(BaseModel):
    patient_id: str
    query: str
    uploaded_file_name: Optional[str] = None

class AgentState(BaseModel):
    patient_id: str
    original_query: str
    uploaded_file_name: Optional[str] = None
    patient_data: Optional[Dict[str, Any]] = None
    ai_response: Optional[str] = None
    safety_score: Optional[int] = None
    confidence_score: Optional[int] = None
    urgency_level: Optional[str] = None  # Added field: high, medium, low
    needs_urgent_review: Optional[bool] = None
    final_response_to_patient: Optional[str] = None
    error_message: Optional[str] = None
    next_node: Optional[str] = None

class DoctorAction(BaseModel):
    new_status: str
    doctor_response: Optional[str] = None

class QueryResponse(BaseModel):
    id: str
    timestamp: str
    patient_id: str
    patient_name: Optional[str] = None
    original_query: str
    ai_response: Optional[str] = None
    doctor_final_response: Optional[str] = None
    status: str
    urgency_level: Optional[str] = None
    safety_score: Optional[int] = None
    confidence_score: Optional[int] = None