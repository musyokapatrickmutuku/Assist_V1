
def get_safety_score(response):
    """Simple safety scoring based on keywords"""
    danger_words = [
        'diagnose', 'diagnosis', 'you have', 'take this medication',
        'prescribed', 'dosage', 'treatment plan'
    ]
    
    emergency_words = [
        'emergency', 'call 911', 'hospital', 'immediately'
    ]
    
    safe_words = [
        'consult', 'healthcare provider', 'doctor', 'medical professional'
    ]
    
    score = 100
    
    # Reduce score for dangerous language
    for word in danger_words:
        if word in response.lower():
            score -= 30
    
    # Increase score for emergency escalation
    for word in emergency_words:
        if word in response.lower():
            score += 20
    
    # Increase score for safe language
    for word in safe_words:
        if word in response.lower():
            score += 10
    
    return max(0, min(100, score))

def get_confidence_score(query, response):
    """Simple confidence scoring"""
    base_score = 70
    
    # Longer responses might be more complete
    if len(response) > 100:
        base_score += 10
    
    # Questions about serious symptoms should have lower confidence
    serious_symptoms = ['chest pain', 'difficulty breathing', 'severe']
    if any(symptom in query.lower() for symptom in serious_symptoms):
        base_score -= 20
    
    # Empathetic language increases confidence
    empathy_words = ['understand', 'sorry', 'help', 'care']
    empathy_count = sum(1 for word in empathy_words if word in response.lower())
    base_score += empathy_count * 5
    
    return max(0, min(100, base_score))

def needs_urgent_review(query, response):
    """Flag queries that need immediate doctor attention"""
    urgent_keywords = [
        'chest pain', 'can\'t breathe', 'severe pain', 'emergency',
        'suicide', 'overdose', 'accident', 'bleeding'
    ]
    
    return any(keyword in query.lower() for keyword in urgent_keywords)
