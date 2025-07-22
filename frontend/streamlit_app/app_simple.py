# frontend/streamlit_app/app_simple.py
# Simplified main app for MVP demo

import streamlit as st
from patient_simple import patient_portal_simple
from doctor_simple import doctor_portal_simple

# Page Configuration
st.set_page_config(
    page_title="Assist AI - Simple Demo",
    page_icon="🏥",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.doctor_name = "Dr. Emily Chen"
    st.session_state.patient_id = "P001"
    st.session_state.patient_name = "Sarah Johnson"

# Sidebar Login
with st.sidebar:
    st.title("🏥 Assist AI")
    st.write("Simple Medical Assistant Demo")
    
    if not st.session_state.logged_in:
        st.markdown("### Login")
        
        # Role selection
        role = st.radio("I am a:", ["Patient", "Doctor"])
        st.session_state.role = role
        
        if role == "Patient":
            # Patient selection
            patients = {
                "Sarah Johnson": "P001",
                "Michael Thompson": "P002",
                "Carlos Rodriguez": "P003",
                "Priya Patel": "P004",
                "Eleanor Williams": "P005"
            }
            
            selected = st.selectbox("Select Patient:", list(patients.keys()))
            st.session_state.patient_id = patients[selected]
            st.session_state.patient_name = selected
            
        else:  # Doctor
            doctor_input = st.text_input("Doctor Name:", value="Dr. Emily Chen", key="doctor_name_input")
            st.session_state.doctor_name = doctor_input
        
        if st.button("Login", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
        
        st.info("Demo login - no password needed")
        
    else:
        # Show logged in user
        if st.session_state.role == "Patient":
            patient_name = st.session_state.get("patient_name", "Demo Patient")
            patient_id = st.session_state.get("patient_id", "P001")
            st.success(f"Logged in as: {patient_name}")
            st.write(f"Patient ID: {patient_id}")
        else:
            doctor_name = st.session_state.get("doctor_name", "Dr. Demo")
            st.success(f"Logged in as: {doctor_name}")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# Main Content
if st.session_state.logged_in:
    if st.session_state.role == "Patient":
        patient_portal_simple()
    else:
        doctor_portal_simple()
else:
    # Welcome screen
    st.title("🏥 Assist AI - Simple Demo")
    st.subheader("Connecting Patients with Doctors")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### For Patients 👤
        - Submit medical questions
        - Get responses from doctors
        - Track your question history
        - Simple and easy to use
        """)
    
    with col2:
        st.markdown("""
        ### For Doctors 👨‍⚕️
        - Review patient questions
        - Send responses quickly
        - Prioritize urgent cases
        - Simple workflow
        """)
    
    st.info("👈 Please login using the sidebar to get started")
    
    # Show demo stats
    st.markdown("---")
    st.markdown("### Demo Features")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Demo Patients", "5", "Active")
    with col2:
        st.metric("Response Time", "< 5 min", "Demo mode")
    with col3:
        st.metric("Success Rate", "100%", "Simplified")
