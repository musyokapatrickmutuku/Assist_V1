import openai

openai.api_key = "your-api-key-here"

def get_ai_response(query):
    prompt = f"""
    You are a helpful medical AI assistant. 
    IMPORTANT: Never diagnose or prescribe medication.
    Always recommend consulting healthcare providers.
    Be empathetic and helpful.
    
    Patient question: {query}
    
    Provide a safe, helpful response:
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        return response.choices[0].message.content
    except:
        return "I'm sorry, I'm having trouble right now. Please consult with a healthcare provider."

# Pre-made demo responses for reliability
DEMO_RESPONSES = {
    "headache": "I understand you're experiencing a headache. While occasional headaches are common, if they persist or worsen, please consult with your healthcare provider. In the meantime, staying hydrated and resting in a quiet, dark room may help.",
    "chest pain": "Chest pain can be serious and requires immediate medical attention. Please contact emergency services or visit the nearest emergency room right away. Don't wait or try to self-diagnose.",
}

def get_demo_response(query):
    # Use pre-made responses for demo reliability
    if "headache" in query.lower():
        return DEMO_RESPONSES["headache"]
    elif "chest pain" in query.lower():
        return DEMO_RESPONSES["chest pain"]
    else:
        return get_ai_response(query)
