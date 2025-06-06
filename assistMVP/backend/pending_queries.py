import json
import uuid
from datetime import datetime

def generate_response(query):
    if not query.strip():
        return "Please enter a valid question about diabetes."

    query_lower = query.lower()

    if "blood sugar" in query_lower or "glucose" in query_lower:
        return "To manage your blood sugar, monitor regularly, eat balanced meals low in refined sugar, and follow your treatment plan. If readings are consistently high or low, contact your healthcare provider."
    elif "insulin" in query_lower:
        return "Insulin helps regulate blood sugar. Always follow your prescribed dosage, store insulin properly, and monitor for signs of hypoglycemia (like dizziness or sweating)."
    elif "hypoglycemia" in query_lower or "low sugar" in query_lower:
        return "If you experience low blood sugar: eat or drink something with fast-acting sugar (like juice or glucose tablets). Recheck levels in 15 minutes. If symptoms persist, seek medical help."
    elif "diet" in query_lower or "food" in query_lower:
        return "A diabetes-friendly diet includes whole grains, lean proteins, non-starchy vegetables, and healthy fats. Avoid sugary drinks and limit processed carbs."
    elif "exercise" in query_lower or "workout" in query_lower:
        return "Exercise can help control blood sugar. Aim for 30 minutes most days. Check your levels before and after activity, and carry a quick snack in case of hypoglycemia."
    else:
        return f"Thank you for your question: '{query}'. While this assistant provides general diabetes advice, please consult a healthcare provider for personalized care."


def save_query(question, ai_response):
    query_data = {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "ai_response": ai_response,
        "status": "pending_review"
    }
    
    try:
        with open("queries.json", "r") as f:
            queries = json.load(f)
    except:
        queries = []
    
    queries.append(query_data)
    
    with open("queries.json", "w") as f:
        json.dump(queries, f)
    
    return query_data

def load_pending_queries():
    try:
        with open("queries.json", "r") as f:
            queries = json.load(f)
        return [q for q in queries if q["status"] == "pending_review"]
    except:
        return []

def approve_query(query_id):
    try:
        with open("queries.json", "r") as f:
            queries = json.load(f)
        
        for query in queries:
            if query["id"] == query_id:
                query["status"] = "approved"
                query["approved_at"] = datetime.now().isoformat()
        
        with open("queries.json", "w") as f:
            json.dump(queries, f)
    except:
        pass
