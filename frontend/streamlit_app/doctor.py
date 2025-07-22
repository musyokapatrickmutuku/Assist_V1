# frontend/streamlit_app/doctor.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8001")

def get_urgency_badge(urgency_level):
    """Return colored emoji badge based on urgency"""
    badges = {
        "high": "🔴 HIGH PRIORITY",
        "medium": "🟡 MEDIUM PRIORITY", 
        "low": "🟢 ROUTINE"
    }
    return badges.get(urgency_level, "🔵 UNCLASSIFIED")

def get_patient_info(patient_id):
    """Fetch patient information from backend"""
    try:
        # In a real app, this would be an API call
        # For demo, we'll make a simple API call to backend
        response = requests.get(f"{BACKEND_URL}/patient/{patient_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        # Fallback: hardcoded patient info for demo
        patient_names = {
            "P001": {"name": "Sarah Johnson", "diabetes_type": "Type 2", "current_hba1c": "6.9%", "complications": False},
            "P002": {"name": "Michael Thompson", "diabetes_type": "Type 1", "current_hba1c": "7.8%", "complications": False},
            "P003": {"name": "Carlos Rodriguez", "diabetes_type": "Type 2", "current_hba1c": "6.8%", "complications": True},
            "P004": {"name": "Priya Patel", "diabetes_type": "Type 2 (post-GDM)", "current_hba1c": "6.2%", "complications": False},
            "P005": {"name": "Eleanor Williams", "diabetes_type": "Type 2", "current_hba1c": "8.0%", "complications": True}
        }
        return patient_names.get(patient_id, None)

def format_time_ago(timestamp_str):
    """Format timestamp as 'X hours ago'"""
    try:
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        diff = now - timestamp
        
        if diff.total_seconds() < 3600:
            return f"{int(diff.total_seconds() / 60)} minutes ago"
        elif diff.total_seconds() < 86400:
            return f"{int(diff.total_seconds() / 3600)} hours ago"
        else:
            return f"{int(diff.total_seconds() / 86400)} days ago"
    except:
        return "Recently"

def doctor_portal():
    """Enhanced doctor portal with urgency indicators and patient context"""
    st.header("👨‍⚕️ Doctor Portal")
    
    # Add welcome message
    doctor_name = st.session_state.get("doctor_name", "Dr. Demo")
    st.write(f"Welcome back, {doctor_name}")

    # Create tabs
    review_tab, completed_tab, analytics_tab, help_tab = st.tabs([
        "📋 Review Queries", "✅ Completed Reviews", "📊 Analytics", "❓ Help"
    ])

    # --- Review Queries Tab ---
    with review_tab:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.subheader("Queries Awaiting Review")
        with col2:
            auto_refresh = st.checkbox("Auto-refresh", value=False, help="Automatically refresh every 30 seconds")
        with col3:
            if st.button("🔄 Refresh Now", use_container_width=True):
                st.rerun()

        # Auto-refresh functionality
        if auto_refresh:
            import time
            if "last_refresh" not in st.session_state:
                st.session_state.last_refresh = time.time()
            
            # Only refresh every 30 seconds
            if time.time() - st.session_state.last_refresh > 30:
                st.session_state.last_refresh = time.time()
                st.rerun()

        # Fetch pending queries
        try:
            response = requests.get(f"{BACKEND_URL}/pending_queries/")
            response.raise_for_status()
            pending_queries = response.json()
            
            # Show last updated time and debug info
            current_time = datetime.now().strftime("%H:%M:%S")
            st.caption(f"Last updated: {current_time} | Backend: {BACKEND_URL} | Found: {len(pending_queries)} queries")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Could not fetch pending queries from {BACKEND_URL}. Error: {str(e)}")
            pending_queries = []
        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")
            pending_queries = []

        if not pending_queries:
            st.info("✨ All caught up! No queries are currently awaiting review.")
        else:
            # Sort by urgency
            urgency_order = {"high": 0, "medium": 1, "low": 2}
            pending_queries.sort(key=lambda x: urgency_order.get(x.get('urgency_level', 'low'), 3))
            
            # Show summary metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                high_priority = sum(1 for q in pending_queries if q.get('urgency_level') == 'high')
                st.metric("High Priority", high_priority, delta_color="inverse")
            with col2:
                st.metric("Total Pending", len(pending_queries))
            with col3:
                avg_wait = "2.5 hours"  # This would be calculated in production
                st.metric("Avg Wait Time", avg_wait)
            
            st.markdown("---")
            
            # Display each query
            for query in pending_queries:
                urgency = query.get('urgency_level', 'low')
                
                # Create container with border color based on urgency
                with st.container():
                    # Urgency badge and time
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.markdown(f"### {get_urgency_badge(urgency)}")
                    with col2:
                        st.write(f"📅 {format_time_ago(query.get('timestamp'))}")
                    
                    # Patient info section
                    patient_id = query.get('patient_id', 'Unknown')
                    st.markdown(f"**Patient ID:** `{patient_id}`")
                    
                    # Try to get patient summary
                    patient_summary = get_patient_info(patient_id)
                    if patient_summary:
                        cols = st.columns(4)
                        with cols[0]:
                            st.markdown(f"**Name:** {patient_summary.get('name', 'N/A')}")
                        with cols[1]:
                            st.markdown(f"**Type:** {patient_summary.get('diabetes_type', 'N/A')}")
                        with cols[2]:
                            st.markdown(f"**HbA1c:** {patient_summary.get('current_hba1c', 'N/A')}")
                        with cols[3]:
                            complications = "⚠️ Yes" if patient_summary.get('complications') else "✅ None"
                            st.markdown(f"**Complications:** {complications}")
                    
                    # Query content
                    st.markdown("**Patient's Question:**")
                    with st.expander("View Question", expanded=True):
                        st.info(query.get('original_query', 'Question not found.'))
                    
                    # AI suggestion with safety indicators
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown("**AI-Generated Draft Response:**")
                    with col2:
                        safety_score = query.get('safety_score', 0)
                        confidence_score = query.get('confidence_score', 0)
                        st.markdown(f"🛡️ Safety: {safety_score}%")
                        st.markdown(f"📊 Confidence: {confidence_score}%")
                    
                    with st.expander("View AI Draft", expanded=True):
                        st.warning(query.get('ai_response', 'No AI response generated.'))
                    
                    # Doctor's response section
                    st.markdown("**Your Response to Patient:**")
                    
                    # Quick response templates for common scenarios
                    if urgency == "high":
                        if st.button("🚨 Use Emergency Template", key=f"emerg_{query['id']}"):
                            emergency_template = """Based on your symptoms, I recommend you seek immediate medical attention. Please go to the emergency room or call 911 right away.

Do not wait for further advice. Your safety is our top priority.

I will follow up with you after you receive emergency care."""
                            st.session_state[f"response_{query['id']}"] = emergency_template
                    
                    # Response text area
                    response_key = f"response_{query['id']}"
                    initial_value = st.session_state.get(response_key, query.get('ai_response', ''))
                    
                    final_response_text = st.text_area(
                        "Edit the response below:",
                        value=initial_value,
                        key=response_key,
                        height=200,
                        help="You can edit the AI suggestion or write your own response"
                    )
                    
                    # Action buttons
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col1:
                        if st.button("✅ Approve & Send", key=f"approve_{query['id']}", type="primary"):
                            if not final_response_text.strip():
                                st.error("The response cannot be empty.")
                            else:
                                payload = {
                                    "new_status": "approved",
                                    "doctor_response": final_response_text
                                }
                                try:
                                    update_response = requests.post(
                                        f"{BACKEND_URL}/update_query/{query['id']}", 
                                        json=payload
                                    )
                                    update_response.raise_for_status()
                                    st.success("✅ Response sent to patient!")
                                    st.balloons()
                                    st.rerun()
                                except:
                                    st.error("Failed to send response. Please try again.")
                    
                    with col2:
                        if st.button("🔄 Request More Info", key=f"info_{query['id']}"):
                            st.info("Feature coming soon: Request additional information from patient")
                    
                    with col3:
                        if st.button("📞 Schedule Call", key=f"call_{query['id']}"):
                            st.info("Feature coming soon: Schedule a follow-up call")
                    
                    st.markdown("---")

    # --- Completed Reviews Tab ---
    with completed_tab:
        st.subheader("Your Reviewed Queries")
        
        # In production, this would fetch from an API
        completed_data = [
            {
                "date": "2024-11-18",
                "patient": "Sarah Johnson",
                "query": "Blood sugar spikes after lunch",
                "response_time": "45 minutes",
                "urgency": "medium"
            },
            {
                "date": "2024-11-17",
                "patient": "Michael Thompson",
                "query": "Insulin pump settings question",
                "response_time": "2 hours",
                "urgency": "low"
            }
        ]
        
        if completed_data:
            df = pd.DataFrame(completed_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No completed reviews yet.")

    # --- Analytics Tab ---
    with analytics_tab:
        st.subheader("Your Performance Analytics")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Queries This Week", "23", "+15%")
        with col2:
            st.metric("Avg Response Time", "1.2 hours", "-30%")
        with col3:
            st.metric("Patient Satisfaction", "4.8/5", "+0.2")
        with col4:
            st.metric("Urgent Cases Handled", "5", "0")
        
        st.markdown("---")
        
        # Simple chart placeholder
        st.subheader("Response Time Trend")
        chart_data = pd.DataFrame({
            'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'],
            'Response Time (hours)': [2.1, 1.8, 1.5, 1.2, 1.3]
        })
        st.line_chart(chart_data.set_index('Day'))

    # --- Help Tab ---
    with help_tab:
        st.subheader("Help & Guidelines")
        
        with st.expander("🚨 Urgency Levels Explained"):
            st.markdown("""
            - **🔴 HIGH**: Requires immediate attention (chest pain, severe symptoms, extreme blood sugar)
            - **🟡 MEDIUM**: Should be addressed within hours (concerning symptoms, medication questions)
            - **🟢 ROUTINE**: Can be addressed within 24 hours (general questions, lifestyle advice)
            """)
        
        with st.expander("📝 Response Guidelines"):
            st.markdown("""
            1. **Always verify** the AI suggestion before approving
            2. **Personalize** responses based on patient history
            3. **Be clear** about when to seek emergency care
            4. **Document** any changes to treatment plans
            5. **Follow up** on high-priority cases
            """)
        
        with st.expander("💡 Using AI Suggestions"):
            st.markdown("""
            The AI provides draft responses based on:
            - Patient's medical history
            - Current medications
            - Diabetes type and complications
            - Query content and urgency
            
            **Remember**: AI suggestions are starting points. Your clinical judgment is essential.
            """)
        
        st.info("For technical support, contact: support@assist-ai.health")