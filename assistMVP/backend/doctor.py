import streamlit as st
import json
from datetime import datetime
from patient import patient_page
from pending_queries import load_pending_queries
from safety_evaluation import get_safety_score



def doctor_page():
    st.title("👨‍⚕️ Doctor Dashboard")
    
    # Call pending queries data function
    queries = load_pending_queries()
    
    for query in queries:
        st.write(f"**Patient Question:** {query['question']}")
        st.write(f"**AI Response:** {query['ai_response']}")
        # Call Person 4's evaluation function
        safety_score = get_safety_score(query['ai_response'])
        st.write(f"**Safety Score:** {safety_score}")
        
        if st.button(f"Approve Response {query['id']}"):
            st.success("Response approved!")
