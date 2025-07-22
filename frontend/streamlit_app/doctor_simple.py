# frontend/streamlit_app/doctor_simple.py
# Simplified doctor portal for MVP demo

import streamlit as st
import requests
from datetime import datetime
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8002")

def doctor_portal_simple():
    """Simplified doctor portal for MVP demo"""
    doctor_name = st.session_state.get("doctor_name", "Dr. Demo")
    
    st.title(f"👨‍⚕️ Doctor Portal - {doctor_name}")
    st.subheader("Patient Questions Awaiting Review")
    
    # Refresh button
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()
    
    try:
        # Get pending questions
        response = requests.get(f"{BACKEND_URL}/pending_questions/")
        
        if response.status_code == 200:
            pending = response.json()
            
            if not pending:
                st.info("✨ All caught up! No pending questions to review.")
            else:
                st.write(f"**{len(pending)} question(s) waiting for your review:**")
                
                for i, question in enumerate(pending):
                    urgency_colors = {
                        "high": "🔴",
                        "medium": "🟡", 
                        "low": "🟢"
                    }
                    
                    urgency = question.get('urgency', 'low')
                    urgency_icon = urgency_colors.get(urgency, "🔵")
                    
                    with st.expander(f"{urgency_icon} Question {i+1} - {urgency.upper()} priority", expanded=i==0):
                        # Patient info
                        st.write(f"**Patient:** {question.get('patient_name', 'Unknown')} (ID: {question.get('patient_id', 'N/A')})")
                        st.write(f"**Submitted:** {question.get('date', 'Recently')}")
                        
                        # Question
                        st.markdown("**Patient's Question:**")
                        st.info(question.get('question', 'Question not available'))
                        
                        # Response form
                        st.markdown("**Your Response:**")
                        
                        response_key = f"response_{question.get('id', i)}"
                        
                        # Quick response templates
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            if st.button(f"📊 Standard Response", key=f"std_{i}"):
                                st.session_state[response_key] = "Thank you for your question. Based on your symptoms, I recommend..."
                        with col2:
                            if st.button(f"🎬 Schedule Visit", key=f"visit_{i}"):
                                st.session_state[response_key] = "I'd like to see you in the office to discuss this further. Please call to schedule an appointment."
                        with col3:
                            if st.button(f"🚨 Urgent Care", key=f"urgent_{i}"):
                                st.session_state[response_key] = "This requires immediate attention. Please go to the emergency room or call 911."
                        
                        # Response text area
                        doctor_response = st.text_area(
                            "Write your response:",
                            value=st.session_state.get(response_key, ""),
                            key=response_key,
                            height=120,
                            placeholder="Provide your medical advice and recommendations..."
                        )
                        
                        # Send response
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            if st.button(f"✅ Send Response to Patient", key=f"send_{i}", type="primary"):
                                if doctor_response.strip():
                                    # Send response
                                    payload = {
                                        "question_id": question.get('id'),
                                        "doctor_response": doctor_response,
                                        "status": "answered"
                                    }
                                    
                                    try:
                                        send_response = requests.post(f"{BACKEND_URL}/send_response/", json=payload)
                                        if send_response.status_code == 200:
                                            st.success("✅ Response sent to patient!")
                                            st.balloons()
                                            # Clear the response
                                            if response_key in st.session_state:
                                                del st.session_state[response_key]
                                            st.rerun()
                                        else:
                                            st.error("Failed to send response")
                                    except Exception as e:
                                        st.error(f"Error sending response: {str(e)}")
                                else:
                                    st.warning("Please write a response before sending")
                        
                        with col2:
                            if st.button(f"🗑️ Dismiss", key=f"dismiss_{i}"):
                                st.info("Dismiss feature coming soon")
                        
                        st.markdown("---")
        else:
            st.error("Could not connect to backend server")
            
    except Exception as e:
        st.error(f"Error loading questions: {str(e)}")
    
    # Sidebar stats
    st.sidebar.markdown("### Today's Stats")
    try:
        stats_response = requests.get(f"{BACKEND_URL}/doctor_stats/")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            st.sidebar.metric("Questions Today", stats.get('today', 0))
            st.sidebar.metric("Responses Sent", stats.get('responses', 0))
            st.sidebar.metric("Avg Response Time", stats.get('avg_time', '2.5 hrs'))
        else:
            st.sidebar.metric("Questions Pending", len(pending) if 'pending' in locals() else 0)
    except:
        st.sidebar.metric("Questions Pending", len(pending) if 'pending' in locals() else 0)
    
    # Quick actions
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Quick Actions")
    st.sidebar.button("📈 View Analytics", disabled=True, help="Coming soon")
    st.sidebar.button("📊 Patient Reports", disabled=True, help="Coming soon")
    st.sidebar.button("⚙️ Settings", disabled=True, help="Coming soon")
