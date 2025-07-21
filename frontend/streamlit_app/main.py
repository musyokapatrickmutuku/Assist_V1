# frontend/streamlit_app/main.py

import streamlit as st
import time
from patient import patient_portal
from doctor import doctor_portal

# --- Page Configuration ---
st.set_page_config(
    page_title="Assist AI - Medical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Landing Page Function (Integrated) ---
def show_landing():
    """Display the landing page with value proposition"""
    
    # Custom CSS for landing page
    st.markdown("""
    <style>
    .hero-header {
        font-size: 3.5rem;
        font-weight: bold;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        text-align: center;
    }
    .metric-number {
        font-size: 2.5rem;
        font-weight: bold;
        color: #667eea;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<h1 class="hero-header">Assist AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.5rem; color: #666;">Bridging the Care Gap Between Patients and Doctors</p>', unsafe_allow_html=True)
    
    # Problem Statement
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.info("""
        **🏥 The Problem We Solve**
        
        422 million people worldwide live with diabetes. Each one waits weeks for simple answers,
        while doctors are overwhelmed with routine queries. We're changing that.
        """)
    
    st.markdown("---")
    
    # Impact Metrics
    st.markdown("### 📊 Our Impact")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-number">4 hrs</div>
        <p>Response Time<br><small>vs 3 weeks</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-number">92%</div>
        <p>Patient<br><small>Satisfaction</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-number">70%</div>
        <p>Doctor Time<br><small>Saved</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
        <div class="metric-number">100%</div>
        <p>Doctor<br><small>Verified</small></p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # How it works
    st.markdown("### 🔄 How It Works")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 1️⃣ Patient Asks")
        st.write("Submit questions through secure portal with medical context")
    
    with col2:
        st.markdown("#### 2️⃣ AI Assists")
        st.write("AI reviews history and generates draft response")
    
    with col3:
        st.markdown("#### 3️⃣ Doctor Verifies")
        st.write("Doctor reviews, edits, and approves before sending")
    
    st.markdown("---")
    
    # Call to Action
    st.markdown("### 🚀 Ready to Try?")
    col1, col2 = st.columns(2)
    with col1:
        st.info("**For Patients**: Login with demo account to submit health questions")
    with col2:
        st.info("**For Doctors**: Review and respond to patient queries with AI assistance")

# --- Main App ---

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None

# Sidebar
with st.sidebar:
    st.title("🏥 Assist AI")
    st.write("Medical AI Assistant Demo")
    
    if not st.session_state.logged_in:
        # Show landing page toggle
        show_landing_page = st.checkbox("Show Landing Page", value=True)
        
        st.markdown("---")
        st.markdown("### Login")
        
        role = st.radio(
            "Select your role:",
            ("Patient", "Doctor"),
            key="role_selection"
        )
        
        st.session_state.role = role
        
        if role == "Patient":
            # Demo patient accounts
            patient_options = {
                "Sarah Johnson (Type 2)": "P001",
                "Michael Thompson (Type 1)": "P002",
                "Carlos Rodriguez (Type 2)": "P003",
                "Priya Patel (Pregnant)": "P004",
                "Eleanor Williams (Elderly)": "P005"
            }
            
            selected_patient = st.selectbox(
                "Select demo patient:",
                options=list(patient_options.keys())
            )
            
            st.session_state.patient_id = patient_options[selected_patient]
            st.session_state.patient_name = selected_patient.split(" (")[0]
            
        else:  # Doctor
            st.text_input("Doctor ID", value="D001", key="doctor_id")
            st.text_input("Name", value="Dr. Emily Chen", key="doctor_name")
        
        if st.button("Login", type="primary", use_container_width=True):
            st.session_state.logged_in = True
            st.rerun()
        
        st.info("Demo Password: demo123")
        
    else:
        # Logged in info
        st.success(f"Logged in as: {st.session_state.get('patient_name', st.session_state.get('doctor_name'))}")
        st.write(f"Role: {st.session_state.role}")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

# Main content area
if st.session_state.logged_in:
    if st.session_state.role == "Patient":
        patient_portal()
    else:
        doctor_portal()
else:
    # Show landing page or login prompt
    if 'show_landing_page' in locals() and show_landing_page:
        show_landing()
    else:
        st.header("Welcome to Assist AI")
        st.info("Please log in using the sidebar to continue.")