import streamlit as st
import json
from datetime import datetime
from patient import patient_page
from doctor import doctor_page

# Set page config
st.sidebar.subheader("**Meet Assist — Your Friendly Health Helper for Diabetes**")
st.sidebar.write("**Struggling to explain your symptoms or ask for the right treatment? Assist helps you turn your thoughts into clear, accurate requests your doctor will understand. It’s like having a smart friend by your side who knows diabetes—and speaks doctor!**")
page = st.sidebar.selectbox("Choose Page", ["Patient", "Doctor"])
if page == "Patient":
    patient_page()
else:
    doctor_page()
