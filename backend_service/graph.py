# backend_service/graph.py

import os
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END

from schemas import AgentState
from patient_db import get_patient_data, get_patient_context_for_ai

# --- Enhanced Helper Functions for Demo ---
def get_safety_score(ai_response: str) -> int:
    """Calculate safety score based on response content"""
    score = 100
    
    # Dangerous phrases that should never appear
    danger_phrases = [
        'you have', 'you are diagnosed with', 'stop taking', 
        'change your dose', 'you don\'t need', 'ignore your doctor'
    ]
    
    # Good safety phrases
    safety_phrases = [
        'consult your doctor', 'speak with your healthcare provider',
        'medical attention', 'emergency', 'call 911', 'seek immediate'
    ]
    
    response_lower = ai_response.lower()
    
    for phrase in danger_phrases:
        if phrase in response_lower:
            score -= 30
    
    for phrase in safety_phrases:
        if phrase in response_lower:
            score += 10
    
    return max(0, min(100, score))

def get_confidence_score(query: str, ai_response: str, patient_data: dict) -> int:
    """Calculate confidence based on query complexity and patient context"""
    score = 85  # Base score
    
    # Complex medical situations reduce confidence
    if patient_data:
        profile = patient_data.get('profile', {})
        if profile.get('patient_id') == 'P004':  # Pregnant patient
            score -= 15
        elif profile.get('patient_id') == 'P005':  # Elderly with complications
            score -= 10
    
    # Urgent symptoms reduce confidence
    urgent_keywords = ['chest pain', 'dizzy', 'unconscious', 'severe', 'emergency']
    if any(keyword in query.lower() for keyword in urgent_keywords):
        score -= 20
    
    # Well-structured response increases confidence
    if len(ai_response) > 100 and len(ai_response) < 500:
        score += 5
    
    return max(0, min(100, score))

def determine_urgency_level(query: str, ai_response: str) -> str:
    """Determine urgency level: high, medium, low"""
    query_lower = query.lower()
    
    high_urgency_keywords = [
        'chest pain', 'can\'t breathe', 'unconscious', 'severe pain',
        'blood sugar over 400', 'blood sugar under 50', 'vomiting',
        'confusion', 'blurred vision', 'emergency'
    ]
    
    medium_urgency_keywords = [
        'dizzy', 'nausea', 'headache', 'high blood sugar',
        'low blood sugar', 'infection', 'fever', 'swelling'
    ]
    
    if any(keyword in query_lower for keyword in high_urgency_keywords):
        return "high"
    elif any(keyword in query_lower for keyword in medium_urgency_keywords):
        return "medium"
    else:
        return "low"

def needs_urgent_review(query: str, ai_response: str, urgency_level: str) -> bool:
    """Determine if query needs immediate doctor attention"""
    return urgency_level in ["high", "medium"]

def save_query_for_review(state_dict: dict):
    """Save query to database for doctor review"""
    import sqlite3
    import uuid
    from datetime import datetime
    from patient_db import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if this query already exists (prevent duplicates)
    cursor.execute("""
        SELECT id FROM queries 
        WHERE patient_id = ? AND original_query = ? 
        AND status = 'pending_review'
        ORDER BY timestamp DESC LIMIT 1
    """, (state_dict['patient_id'], state_dict['original_query']))
    
    existing = cursor.fetchone()
    if existing:
        print(f"Query already exists with ID: {existing[0]} - skipping duplicate save")
        conn.close()
        return {"id": existing[0], "status": "pending_review"}
    
    query_id = str(uuid.uuid4())
    
    cursor.execute("""
        INSERT INTO queries (
            id, timestamp, patient_id, original_query, 
            ai_response, status, urgency_level, 
            safety_score, confidence_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        query_id,
        datetime.now().isoformat(),
        state_dict['patient_id'],
        state_dict['original_query'],
        state_dict.get('ai_response'),
        'pending_review',
        state_dict.get('urgency_level', 'low'),
        state_dict.get('safety_score'),
        state_dict.get('confidence_score')
    ))
    
    conn.commit()
    conn.close()
    
    return {"id": query_id, "status": "pending_review"}

# --- Node Definitions ---
def fetch_patient_data_node(state: AgentState):
    """Fetches patient data and returns the full, updated state."""
    print("---NODE: FETCHING PATIENT DATA---")
    new_state = state.copy(deep=True)
    
    patient_data = get_patient_data(new_state.patient_id)
    if not patient_data:
        new_state.error_message = f"Patient ID '{new_state.patient_id}' not found."
    else:
        new_state.patient_data = patient_data
        print(f"Found patient: {patient_data['profile']['name']}")
    
    return new_state

def generate_ai_response_node(state: AgentState):
    """Generates an AI response with patient context."""
    print("---NODE: GENERATING AI RESPONSE---")
    new_state = state.copy(deep=True)
    
    if new_state.error_message:
        return new_state
    
    # Get patient context for the AI
    patient_context = get_patient_context_for_ai(new_state.patient_id)
    
    # Create a comprehensive prompt
    prompt = f"""You are a medical AI assistant helping with diabetes management. 
    IMPORTANT RULES:
    - Never diagnose conditions or prescribe medications
    - Always recommend consulting with healthcare providers for medical decisions
    - Be empathetic and supportive
    - Provide educational information when appropriate
    - For urgent symptoms, strongly recommend immediate medical attention
    
    Patient Context:
    {patient_context}
    
    Patient Question: {new_state.original_query}
    
    Please provide a helpful, safe response that:
    1. Addresses their specific concern
    2. Considers their medical history
    3. Provides general guidance
    4. Recommends appropriate medical consultation when needed
    
    Response:"""
    
    try:
        # For demo reliability, use pre-crafted responses for common queries
        query_lower = new_state.original_query.lower()
        
        # Demo responses based on specific scenarios
        if "blood sugar" in query_lower and ("high" in query_lower or "250" in query_lower):
            new_state.ai_response = """I understand your concern about your elevated blood sugar reading. A reading of 250 mg/dL is indeed higher than target range.

Based on your current management plan with Metformin and other medications, here are some immediate steps you can consider:

1. **Check for ketones** if you have testing strips available
2. **Stay well hydrated** - drink plenty of water
3. **Light activity** like a short walk can help if you're feeling well enough
4. **Review recent factors** - unusual meals, missed medications, stress, or illness

Given your good overall control (HbA1c 6.9%), this may be a temporary spike. However, if readings remain elevated or you experience symptoms like excessive thirst, frequent urination, or nausea, please contact your healthcare provider promptly.

Continue monitoring and keep a log to discuss with Dr. Chen at your next visit."""

        elif "dizzy" in query_lower or "low" in query_lower:
            if new_state.patient_id == "P001":  # Type 2 patient
                new_state.ai_response = """Dizziness with low blood sugar requires immediate attention. If your glucose is below 70 mg/dL:

**Immediate Actions:**
1. Follow the 15-15 rule: Consume 15g of fast-acting carbs (like 4 glucose tablets, 1/2 cup juice, or 1 tablespoon honey)
2. Recheck your blood sugar in 15 minutes
3. If still low, repeat the treatment
4. Once normalized, have a small snack with protein

**Safety Note:** Given your Empagliflozin medication, which can sometimes contribute to low blood sugar when combined with other factors, this is important to address.

If symptoms persist or worsen, don't hesitate to call emergency services. Please inform Dr. Chen about this episode at your next appointment to potentially adjust your medication regimen."""
            
        elif "pregnancy" in query_lower or "pregnant" in query_lower:
            if new_state.patient_id == "P004":
                new_state.ai_response = """Congratulations on your pregnancy! Managing diabetes during pregnancy requires special attention, and I see you're already in your first trimester.

Since you've discontinued Metformin (as is standard practice), blood sugar management is especially important. Here are key points:

1. **Frequent monitoring**: Check blood sugar 4-6 times daily
2. **Target ranges**: Fasting <95 mg/dL, 1-hour post-meal <140 mg/dL
3. **Diet focus**: Small, frequent meals with balanced carbs and protein
4. **Stay active**: Continue your prenatal yoga, it's excellent for blood sugar control

Your current HbA1c of 6.2% is good, but pregnancy can affect glucose levels. If you notice any unusual patterns or have concerns, please contact your healthcare team immediately. They may need to start insulin if diet and exercise aren't maintaining targets.

Remember, you successfully managed GDM in your first pregnancy - you've got this!"""
        
        else:
            # Use LLM for other queries
            llm = ChatOpenAI(
                model_name="deepseek/deepseek-r1-0528",
                openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
                openai_api_base=os.getenv("DEEPSEEK_API_BASE"),
                temperature=0.7,
                max_tokens=300
            )
            new_state.ai_response = llm.invoke(prompt).content
            
    except Exception as e:
        # Fallback response
        new_state.ai_response = """I understand your concern. While I cannot provide specific medical advice, I recommend:

1. Monitor your symptoms closely
2. Follow your current treatment plan
3. Contact your healthcare provider if symptoms persist or worsen
4. In case of emergency symptoms, seek immediate medical attention

Your healthcare team is best equipped to provide personalized guidance based on your complete medical history."""
        print(f"Error generating AI response: {e}")
    
    return new_state

def evaluate_response_node(state: AgentState):
    """Evaluates the AI response for safety and urgency."""
    print("---NODE: EVALUATING RESPONSE---")
    new_state = state.copy(deep=True)
    
    if new_state.error_message or not new_state.ai_response:
        return new_state

    new_state.safety_score = get_safety_score(new_state.ai_response)
    new_state.confidence_score = get_confidence_score(
        new_state.original_query, 
        new_state.ai_response,
        new_state.patient_data
    )
    new_state.urgency_level = determine_urgency_level(
        new_state.original_query,
        new_state.ai_response
    )
    new_state.needs_urgent_review = needs_urgent_review(
        new_state.original_query,
        new_state.ai_response,
        new_state.urgency_level
    )
    
    print(f"Evaluation: Safety={new_state.safety_score}, Confidence={new_state.confidence_score}, Urgency={new_state.urgency_level}")
    
    return new_state

def prepare_for_doctor_review_node(state: AgentState):
    """Saves the query and prepares the final user-facing message."""
    print("---NODE: PREPARING FOR DOCTOR REVIEW---")
    new_state = state.copy(deep=True)
    
    if new_state.error_message:
        return new_state
    
    try:
        save_query_for_review(new_state.model_dump())
        
        # Customize message based on urgency
        if new_state.urgency_level == "high":
            new_state.final_response_to_patient = """⚠️ Your query has been marked as URGENT and forwarded to your doctor for immediate review. 

If you're experiencing severe symptoms, please don't wait - contact emergency services or visit the nearest emergency room.

Your doctor will respond as soon as possible."""
        
        elif new_state.urgency_level == "medium":
            new_state.final_response_to_patient = """Your query has been received and marked for priority review by your doctor. 

You can expect a response within a few hours. If your symptoms worsen, please seek immediate medical attention."""
        
        else:
            new_state.final_response_to_patient = """Thank you for your query. It has been received and will be reviewed by your doctor.

You'll receive a personalized response within 24 hours. For urgent matters, please contact your healthcare provider directly."""
            
    except Exception as e:
        new_state.error_message = f"Failed to save query for review: {e}"
    
    return new_state

# --- Graph Assembly ---
workflow = StateGraph(AgentState)

# Add all nodes to the workflow
workflow.add_node("fetch_patient_data", fetch_patient_data_node)
workflow.add_node("generate_ai_response", generate_ai_response_node)
workflow.add_node("evaluate_response", evaluate_response_node)
workflow.add_node("prepare_for_doctor_review", prepare_for_doctor_review_node)

# Define the sequence of edges
workflow.set_entry_point("fetch_patient_data")
workflow.add_edge("fetch_patient_data", "generate_ai_response")
workflow.add_edge("generate_ai_response", "evaluate_response")
workflow.add_edge("evaluate_response", "prepare_for_doctor_review")
workflow.add_edge("prepare_for_doctor_review", END)

# Compile the workflow
app = workflow.compile()