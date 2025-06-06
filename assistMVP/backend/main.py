import streamlit as st
import json
from datetime import datetime
from patient import patient_page
from doctor import doctor_page

# Set page config
page = st.sidebar.selectbox("Choose Page", ["Patient", "Doctor"])
if page == "Patient":
    patient_page()
else:
    doctor_page()
