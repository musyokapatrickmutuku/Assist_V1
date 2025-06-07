import streamlit as st
import json
from datetime import datetime
from patient import patient_page
from doctor import doctor_page

st.markdown(
    """
    <style>
    /* Make entire selectbox clickable with pointer cursor */
    div[data-testid="stSelectbox"] {
        cursor: pointer !important;
    }

    /* Also apply to dropdown icon */
    div[data-testid="stSelectbox"] svg {
        cursor: pointer !important;
    }

    /* Optionally change hover background for feedback */
    div[data-testid="stSelectbox"]:hover {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Set page config
st.sidebar.header("**Assist — AI Diabetes Assistant**")
st.sidebar.subheader("***Your Friendly Health Helper for Diabetes***")
st.sidebar.write("Struggling to explain your symptoms or ask for the right treatment? Assist helps you turn your thoughts into clear, accurate requests your doctor will understand. It's like having a smart friend by your side who knows diabetes—and speaks doctor!")
st.sidebar.markdown("---")

page = st.sidebar.selectbox(
    "Access as:",
    ["👤 Patient (Ask Questions)", "👨‍⚕️ Doctor (Review & Reply)"],
    help="Select Patient to submit health queries or Doctor to review and respond."
)
st.sidebar.markdown("---")
st.sidebar.markdown("*Assist MVP — Built for diabetes care with Streamlit*")

if page == "👤 Patient (Ask Questions)":
    patient_page()
else:
    doctor_page()

