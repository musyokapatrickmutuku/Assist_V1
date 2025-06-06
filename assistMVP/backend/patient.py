import streamlit as st
import json
from datetime import datetime

# Patient Page
def patient_page():
    st.title("🩺 AI Health Assistant")
    
    query = st.text_area("What's your health question?")
    
    if st.button("Ask AI Assistant"):
        if query:
            # Call Person 2's AI function
            response = get_ai_response(query)
            # Call Person 3's storage function
            save_query(query, response)
            st.success("Your question has been sent for review!")
            st.write("AI Response:", response)
