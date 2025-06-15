# backend_service/schemas.py
from typing import List, Dict, Optional, Any
from pydantic import BaseModel

class PatientQueryInput(BaseModel):
    patient_id: str
    query: str
    uploaded_file_name: Optional[str] = None

# This is the final shape of the data returned by the API
class AgentState(BaseModel):
    patient_id: str
    original_query: str
    uploaded_file_name: Optional[str] = None
    patient_data: Optional[Dict[str, Any]] = None
    ai_response: Optional[str] = None
    # Add the evaluation fields back in
    safety_score: Optional[int] = None
    confidence_score: Optional[int] = None
    needs_urgent_review: Optional[bool] = None
    final_response_to_patient: Optional[str] = None
    error_message: Optional[str] = None
    # This field was also missing
    next_node: Optional[str] = None