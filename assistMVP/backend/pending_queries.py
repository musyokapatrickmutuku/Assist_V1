import json
import uuid
from datetime import datetime

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
