# frontend/streamlit_app/patient_simple.py
# Simplified patient portal for MVP demo

import streamlit as st
import requests
from datetime import datetime
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8002")

def patient_portal_simple():
    """Simplified patient portal for MVP demo"""
    # Get patient info from session
    patient_id = st.session_state.get("patient_id", "P001")
    patient_name = st.session_state.get("patient_name", "Demo Patient")
    
    st.title(f"🏥 Welcome, {patient_name}!")
    st.subheader("Submit Your Medical Question")
    
    # Simple query form
    with st.form("simple_query_form"):
        st.write("Ask your doctor a question about your diabetes care:")
        
        question = st.text_area(
            "Your Question:",
            height=150,
            placeholder="Example: My blood sugar has been high lately. What should I do?",
            help="Be specific about your symptoms or concerns"
        )
        
        urgency = st.radio(
            "How urgent is this?",
            ["Routine (can wait)", "Soon (few hours)", "Urgent (immediate)"],
            index=0
        )
        
        submit = st.form_submit_button("📤 Send to Doctor", type="primary", use_container_width=True)
        
        if submit and question:
            # Map urgency
            urgency_map = {
                "Routine (can wait)": "low",
                "Soon (few hours)": "medium", 
                "Urgent (immediate)": "high"
            }
            
            # Simple payload
            payload = {
                "patient_id": patient_id,
                "query": question,
                "urgency": urgency_map[urgency]
            }
            
            try:
                with st.spinner("Sending your question..."):
                    # Direct database insert instead of complex processing
                    response = requests.post(f"{BACKEND_URL}/simple_query/", json=payload)
                    
                if response.status_code == 200:
                    st.success("✅ Your question has been sent to your doctor!")
                    st.balloons()
                    st.info("You will receive a response within 24 hours. Check 'My Questions' below to track status.")
                else:
                    st.error("❌ Failed to send question. Please try again.")
                    
            except Exception as e:
                st.error(f"❌ Connection error: {str(e)}")
    
    st.markdown("---")
    
    # Show patient's questions
    st.subheader("📋 My Questions")
    
    try:
        response = requests.get(f"{BACKEND_URL}/patient_queries/{patient_id}")
        if response.status_code == 200:
            queries = response.json()
            
            if not queries:
                st.info("No questions submitted yet.")
            else:
                for i, query in enumerate(queries):
                    status_icons = {
                        "pending": "⏳ Waiting for doctor",
                        "answered": "✅ Doctor responded"
                    }
                    
                    status = query.get('status', 'pending')
                    status_text = status_icons.get(status, status)
                    
                    with st.expander(f"Question {i+1} - {status_text}", expanded=i==0):
                        st.write(f"**Asked:** {query.get('date', 'Recently')}")
                        st.write(f"**Your question:** {query.get('question', 'N/A')}")
                        
                        if query.get('doctor_response'):
                            st.success(f"**Doctor's response:** {query['doctor_response']}")
                        else:
                            st.info("Waiting for doctor to respond...")
        else:
            st.error("Could not load your questions.")
            
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
    
    # Simple metrics
    st.sidebar.markdown("### Quick Stats")
    st.sidebar.metric("Patient ID", patient_id)
    st.sidebar.metric("Questions Asked", len(queries) if 'queries' in locals() else 0)
    
    # Emergency info
    st.sidebar.markdown("---")
    st.sidebar.error("""
    🚨 **Emergency?**
    If you have severe symptoms:
    - Call 911
    - Go to ER immediately
    - Don't wait for response
    """)
