# backend_service/pending_queries.py

import json
import uuid
import os
from datetime import datetime

# --- Correct, Robust File Path ---
# This locates queries.json inside the streamlit_app directory, making the path reliable.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QUERIES_FILE_PATH = os.path.join(BASE_DIR, "assistMVP", "streamlit_app", "queries.json")

def _load_queries():
    """Helper function to safely load all queries from the JSON file."""
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(QUERIES_FILE_PATH), exist_ok=True)
    try:
        with open(QUERIES_FILE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or is empty, return an empty list
        return []

def _save_queries(queries):
    """Helper function to safely save all queries to the JSON file."""
    with open(QUERIES_FILE_PATH, "w") as f:
        json.dump(queries, f, indent=4)

def save_query_for_review(agent_state_dict: dict):
    """Saves the agent state to queries.json with consistent keys."""
    queries = _load_queries()
    
    # Structure the data to be saved using consistent keys
    query_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "status": "pending_review",
        "patient_id": agent_state_dict.get("patient_id"),
        "original_query": agent_state_dict.get("original_query"),
        "ai_response": agent_state_dict.get("ai_response"),
        "safety_score": agent_state_dict.get("safety_score"),
        "confidence_score": agent_state_dict.get("confidence_score"),
        "needs_urgent_review": agent_state_dict.get("needs_urgent_review"),
    }
    
    queries.insert(0, query_data)  # Add new queries to the top of the list
    _save_queries(queries)
    
    print(f"--- Query {query_data['id']} saved for doctor review ---")
    return query_data

def load_pending_queries():
    """
    Loads queries that have a 'pending_review' status.
    This function name now correctly matches the import in main.py.
    """
    all_queries = _load_queries()
    return [q for q in all_queries if q.get("status") == "pending_review"]

def get_queries_by_patient_id(patient_id: str):
    """Loads all historical queries for a specific patient."""
    all_queries = _load_queries()
    return [q for q in all_queries if q.get("patient_id") == patient_id]

def update_query_status(query_id: str, new_status: str, doctor_response: str = None):
    """Updates a query's status and adds the doctor's final response."""
    queries = _load_queries()
    query_found = False
    
    for query in queries:
        if query.get("id") == query_id:
            query["status"] = new_status
            query["doctor_final_response"] = doctor_response
            query["reviewed_at"] = datetime.now().isoformat()
            query_found = True
            break
    
    if query_found:
        _save_queries(queries)
        return True, "Status updated successfully."
    
    return False, "Query ID not found."
