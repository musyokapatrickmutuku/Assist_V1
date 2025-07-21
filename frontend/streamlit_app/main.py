# streamlit_app/main.py

import streamlit as st
from patient import patient_portal
from doctor import doctor_portal

# --- Page Configuration ---
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide" # Use wide layout for the two-column design
)

# --- Main App Layout ---

# Create two columns: a smaller one for the sidebar, and a larger one for content
left_col, main_col = st.columns([0.3, 0.7])

# --- Left Sidebar Content ---
with left_col:
    st.title("Medical AI Assistant")
    st.write("Demo Application")

    # Use session state to track login
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.role = "Patient"

    role = st.radio(
        "Select your role:",
        ("Patient", "Doctor"),
        key="role_selection"
    )

    st.session_state.role = role

    # Display appropriate login fields based on role
    if role == "Patient":
        st.text_input("Patient ID", value="P001", key="patient_id")
        st.text_input("Name", value="Demo Patient", key="patient_name")
        st.text_input("Email", value="patient@demo.com", key="patient_email", type="password")
    else: # Doctor
        st.text_input("Doctor ID", value="D_101", key="doctor_id")
        st.text_input("Name", value="Dr. Demo", key="doctor_name")
        st.text_input("Specialty", value="General Medicine", key="doctor_specialty")

    # Login/Logout Buttons
    if st.session_state.logged_in:
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        if st.button("Login"):
            st.session_state.logged_in = True
            st.rerun()

# --- Main Content Area ---
with main_col:
    if st.session_state.logged_in:
        if st.session_state.role == "Patient":
            patient_portal()
        else:
            doctor_portal()
    else:
        st.header("Welcome to the Medical AI Assistant")
        st.info("Please log in using the panel on the left to continue.")