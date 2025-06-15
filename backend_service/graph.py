# backend_service/graph.py

import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from .schemas import AgentState # Make sure this is the Pydantic BaseModel
from .patient_db import get_patient_data

# --- Placeholder Helper Functions ---
def get_safety_score(ai_response: str) -> int: return 95
def get_confidence_score(query: str, ai_response: str) -> int: return 88
def needs_urgent_review(query: str, ai_response: str) -> bool:
    return "dizzy" in query.lower() or "low" in query.lower()
def save_query_for_review(state_dict: dict):
    return {"id": f"query_{hash(state_dict['original_query'])}", "status": "pending_review"}

# --- Node Definitions ---
# Using the robust state.copy() pattern

def fetch_patient_data_node(state: AgentState):
    """Fetches patient data and returns the full, updated state."""
    print("---NODE: FETCHING PATIENT DATA---")
    new_state = state.copy(deep=True)
    patient_data = get_patient_data(new_state.patient_id)
    if not patient_data:
        new_state.error_message = f"Patient ID '{new_state.patient_id}' not found."
    else:
        new_state.patient_data = patient_data
    return new_state

def generate_ai_response_node(state: AgentState):
    """Generates an AI response and returns the full, updated state."""
    print("---NODE: GENERATING AI RESPONSE---")
    new_state = state.copy(deep=True)
    if new_state.error_message: return new_state
    
    prompt_query = (f"Context: Patient with {new_state.patient_data['profile']['Type of Diabetes']}. Query: {new_state.original_query}")
    llm = ChatOpenAI(model_name="deepseek/deepseek-r1-0528", openai_api_key=os.getenv("DEEPSEEK_API_KEY"), openai_api_base=os.getenv("DEEPSEEK_API_BASE"))
    try:
        new_state.ai_response = llm.invoke(prompt_query).content
    except Exception as e:
        new_state.error_message = f"Error generating AI response: {e}"
    return new_state

# =====================================================================
# THE FIX IS HERE: We need to add the evaluation node back into the graph
# =====================================================================
def evaluate_response_node(state: AgentState):
    """Evaluates the AI response and adds scores to the state."""
    print("---NODE: EVALUATING RESPONSE---")
    new_state = state.copy(deep=True)
    if new_state.error_message or not new_state.ai_response:
        return new_state

    new_state.safety_score = get_safety_score(new_state.ai_response)
    new_state.confidence_score = get_confidence_score(new_state.original_query, new_state.ai_response)
    new_state.needs_urgent_review = needs_urgent_review(new_state.original_query, new_state.ai_response)
    return new_state

def prepare_for_doctor_review_node(state: AgentState):
    """Saves the query and prepares the final user-facing message."""
    print("---NODE: PREPARING FOR DOCTOR REVIEW---")
    new_state = state.copy(deep=True)
    if new_state.error_message:
        return new_state
    
    try:
        save_query_for_review(new_state.model_dump())
        new_state.final_response_to_patient = "Your query has been processed and is now awaiting review by your doctor."
    except Exception as e:
        new_state.error_message = f"Failed to save query for review: {e}"
    return new_state


# --- Graph Assembly ---
workflow = StateGraph(AgentState)

# Add all nodes back into the workflow
workflow.add_node("fetch_patient_data", fetch_patient_data_node)
workflow.add_node("generate_ai_response", generate_ai_response_node)
workflow.add_node("evaluate_response", evaluate_response_node) # Add this node
workflow.add_node("prepare_for_doctor_review", prepare_for_doctor_review_node)

# Define the full sequence of edges
workflow.set_entry_point("fetch_patient_data")
workflow.add_edge("fetch_patient_data", "generate_ai_response")
workflow.add_edge("generate_ai_response", "evaluate_response") # Connect to the evaluation node
workflow.add_edge("evaluate_response", "prepare_for_doctor_review") # Connect to the final node
workflow.add_edge("prepare_for_doctor_review", END)

app = workflow.compile()