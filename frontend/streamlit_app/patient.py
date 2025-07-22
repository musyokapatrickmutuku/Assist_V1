# frontend/streamlit_app/patient.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

# Sample queries for easy demo
SAMPLE_QUERIES = {
    "Type 2 - High Blood Sugar": "My blood sugar reading is 250 mg/dL after lunch. I took my medications this morning. Should I be concerned?",
    "Type 2 - Diet Question": "Can I eat fruits if I have Type 2 diabetes? I'm worried about the sugar content.",
    "Type 1 - Low Blood Sugar": "I'm feeling dizzy and shaky. My glucose meter shows 65 mg/dL. What should I do?",
    "Medication Side Effects": "I've been experiencing nausea since starting my new medication. Is this normal?",
    "Exercise Concerns": "I want to start exercising but I'm worried about low blood sugar. Any tips?",
    "Pregnancy & Diabetes": "I'm pregnant and have diabetes. How often should I check my blood sugar?",
}

def get_status_icon(status):
    """Return icon based on query status"""
    icons = {
        "pending_review": "⏳",
        "approved": "✅",
        "urgent": "🚨",
        "needs_info": "❓"
    }
    return icons.get(status, "📄")

def patient_portal():
    """Enhanced patient portal with better UX"""
    # Get patient info from session
    patient_id = st.session_state.get("patient_id", "P001")
    patient_name = st.session_state.get("patient_name", "Demo Patient")
    
    # Header with personalized greeting
    st.header(f"Welcome back, {patient_name}! 👋")
    
    # Quick stats (would be fetched from backend in production)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Last HbA1c", "6.9%", "-0.3%", delta_color="inverse")
    with col2:
        st.metric("Avg Glucose", "130 mg/dL", "Good")
    with col3:
        st.metric("Next Appointment", "Sept 15", "In 2 weeks")
    with col4:
        st.metric("Active Queries", "1", "Pending")
    
    st.markdown("---")
    
    # Create tabs
    submit_tab, queries_tab, resources_tab, profile_tab = st.tabs([
        "❓ Ask a Question", "📋 My Queries", "📚 Resources", "👤 My Profile"
    ])

    # --- Submit Query Tab ---
    with submit_tab:
        st.subheader("Ask Your Healthcare Team")
        st.write("Get personalized answers to your diabetes-related questions. Your doctor will review and respond within 24 hours.")
        
        # Quick question buttons
        st.markdown("### Quick Questions")
        selected_template = None
        
        cols = st.columns(3)
        for idx, (title, question) in enumerate(SAMPLE_QUERIES.items()):
            col_idx = idx % 3
            with cols[col_idx]:
                if st.button(title, key=f"template_{idx}", use_container_width=True):
                    selected_template = question
        
        st.markdown("### Your Question")
        
        # Form for query submission
        with st.form(key="query_form"):
            # Pre-fill with template if selected
            initial_value = selected_template if selected_template else ""
            if selected_template:
                st.info("Template loaded! Feel free to modify it.")
            
            medical_question = st.text_area(
                "Describe your concern or question:",
                value=initial_value,
                height=150,
                placeholder="Example: I've been experiencing fatigue lately despite good blood sugar control..."
            )
            
            # Additional context
            col1, col2 = st.columns(2)
            with col1:
                urgency = st.select_slider(
                    "How urgent is this?",
                    options=["Can wait", "Soon", "Urgent"],
                    value="Soon",
                    help="This helps us prioritize your question"
                )
            
            with col2:
                symptoms = st.multiselect(
                    "Any symptoms? (Optional)",
                    ["Fatigue", "Dizziness", "Nausea", "Headache", "Vision changes", "Other"],
                    help="Select all that apply"
                )
            
            # File upload
            uploaded_file = st.file_uploader(
                "📎 Attach files (optional)",
                type=["pdf", "jpg", "jpeg", "png"],
                help="Upload lab results, glucose logs, or other relevant documents"
            )
            
            # Submit button
            submit_col1, submit_col2, submit_col3 = st.columns([1, 2, 1])
            with submit_col2:
                submit_button = st.form_submit_button(
                    label="🚀 Send to My Doctor",
                    use_container_width=True,
                    type="primary"
                )

        # Reset query submitted flag when showing form
        if "query_submitted" in st.session_state:
            del st.session_state.query_submitted

        # Handle submission
        if submit_button and medical_question:
            with st.spinner("Sending your query..."):
                # Map urgency to backend format
                urgency_map = {"Can wait": "low", "Soon": "medium", "Urgent": "high"}
                
                payload = {
                    "patient_id": patient_id,
                    "query": medical_question,
                    "uploaded_file_name": uploaded_file.name if uploaded_file else None
                }
                
                try:
                    api_response = requests.post(f"{BACKEND_URL}/process_query/", json=payload)
                    api_response.raise_for_status()
                    response_data = api_response.json()
                    
                    # Show appropriate response based on urgency
                    urgency_level = response_data.get("urgency_level", "low")
                    
                    if urgency_level == "high":
                        st.error("🚨 " + response_data.get("final_response_to_patient", "Query marked as urgent and sent to your doctor for immediate review!"))
                    elif urgency_level == "medium":
                        st.warning("⚡ " + response_data.get("final_response_to_patient", "Query submitted for priority review. You'll hear back within a few hours."))
                    else:
                        st.success("✅ " + response_data.get("final_response_to_patient", "Query submitted successfully! You'll receive a response within 24 hours."))
                    
                    # Show additional confirmation
                    st.info("📧 Your query has been recorded and is now visible in your 'My Queries' tab.")
                    
                    # Show next steps
                    with st.expander("What happens next?"):
                        st.markdown("""
                        1. **AI Analysis**: Our AI reviews your question for urgency ✅ Done
                        2. **Doctor Review**: Your doctor reviews the AI suggestion ⏳ In Progress
                        3. **Personalized Response**: You receive a verified response 📅 Soon
                        4. **Follow-up**: Schedule appointments if needed 🔄 Available
                        """)
                    
                    # Force a refresh of the page to show the new query in "My Queries"
                    st.balloons()
                    
                    # Clear form by setting a flag to rerun
                    if "query_submitted" not in st.session_state:
                        st.session_state.query_submitted = True
                        st.rerun()
                        
                except requests.exceptions.RequestException:
                    st.error("😔 Could not submit your query. Please try again or contact support.")

    # --- My Queries Tab ---
    with queries_tab:
        st.subheader("Your Query History")
        
        # Filter options
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            filter_status = st.selectbox(
                "Filter by status",
                ["All", "Pending", "Answered", "Urgent"],
                index=0
            )
        with col2:
            filter_date = st.date_input(
                "From date",
                value=datetime.now().date().replace(day=1)
            )
        with col3:
            if st.button("🔄 Refresh"):
                st.rerun()
        
        # Fetch queries
        try:
            response = requests.get(f"{BACKEND_URL}/queries/by_patient/{patient_id}")
            response.raise_for_status()
            my_queries = response.json()
            
            if not my_queries:
                st.info("📭 You haven't submitted any queries yet. Ask your first question above!")
            else:
                # Create interactive cards for each query
                for idx, query in enumerate(my_queries):
                    # Parse date
                    try:
                        query_date = datetime.fromisoformat(query.get("timestamp", ""))
                        date_str = query_date.strftime('%B %d, %Y at %I:%M %p')
                    except:
                        date_str = "Recently"
                    
                    # Create expandable card
                    status = query.get("status", "pending_review")
                    status_text = status.replace("_", " ").title()
                    icon = get_status_icon(status)
                    
                    with st.expander(f"{icon} {date_str} - {status_text}", expanded=(idx == 0)):
                        # Query content
                        st.markdown("**Your Question:**")
                        st.write(query.get("original_query", "N/A"))
                        
                        # Response section
                        if query.get("doctor_final_response"):
                            st.markdown("**Doctor's Response:**")
                            st.success(query.get("doctor_final_response"))
                            
                            # Action buttons for answered queries
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                if st.button("👍 Helpful", key=f"helpful_{idx}"):
                                    st.toast("Thank you for your feedback!")
                            with col2:
                                if st.button("❓ Follow-up", key=f"followup_{idx}"):
                                    st.info("Start a new query above to ask a follow-up question")
                            with col3:
                                if st.button("📅 Book Appointment", key=f"book_{idx}"):
                                    st.info("Feature coming soon!")
                        else:
                            st.info("⏳ Awaiting doctor's response...")
                            st.caption("Expected response time: Within 24 hours")
                
        except requests.exceptions.RequestException:
            st.error("Could not fetch your query history. Please try again later.")

    # --- Resources Tab ---
    with resources_tab:
        st.subheader("Diabetes Management Resources")
        
        # Educational content cards
        col1, col2 = st.columns(2)
        
        with col1:
            with st.container():
                st.markdown("### 🍎 Nutrition Guide")
                st.write("Learn about diabetes-friendly foods and meal planning.")
                st.button("Read More →", key="nutrition_guide")
            
            with st.container():
                st.markdown("### 💊 Medication Info")
                st.write("Understanding your diabetes medications.")
                st.button("Read More →", key="med_guide")
        
        with col2:
            with st.container():
                st.markdown("### 🏃‍♀️ Exercise Tips")
                st.write("Safe exercise guidelines for diabetes.")
                st.button("Read More →", key="exercise_guide")
            
            with st.container():
                st.markdown("### 📊 Glucose Tracking")
                st.write("How to monitor and log your blood sugar.")
                st.button("Read More →", key="tracking_guide")
        
        # Emergency info
        st.markdown("---")
        st.markdown("### 🚨 Emergency Information")
        st.error("""
        **When to Seek Immediate Help:**
        - Blood sugar over 400 mg/dL or under 50 mg/dL
        - Severe symptoms: confusion, unconsciousness, chest pain
        - Persistent vomiting or severe dehydration
        
        **Emergency Contact:** Call 911 or go to nearest ER
        """)

    # --- Profile Tab ---
    with profile_tab:
        st.subheader("My Health Profile")
        
        # This would be fetched from backend in production
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Information")
            st.write(f"**Name:** {patient_name}")
            st.write(f"**Patient ID:** {patient_id}")
            st.write("**Diabetes Type:** Type 2")
            st.write("**Diagnosis Date:** March 15, 2022")
        
        with col2:
            st.markdown("### Care Team")
            st.write("**Primary Doctor:** Dr. Emily Chen")
            st.write("**Endocrinologist:** Dr. Michael Roberts")
            st.write("**Dietitian:** Jane Smith, RD")
            st.write("**Care Coordinator:** Lisa Johnson")
        
        st.markdown("---")
        st.markdown("### Current Medications")
        meds_df = pd.DataFrame({
            "Medication": ["Metformin", "Lisinopril", "Empagliflozin"],
            "Dose": ["1000mg BID", "15mg daily", "10mg daily"],
            "Purpose": ["Blood sugar control", "Blood pressure", "Heart & kidney protection"]
        })
        st.dataframe(meds_df, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        if st.button("📋 Download Health Summary", use_container_width=True):
            st.info("Feature coming soon: Download your complete health summary as PDF")