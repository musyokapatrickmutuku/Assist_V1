# assistMVP/streamlit_app/patient.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def patient_portal():
    """
    Renders the patient portal, including tabs for submitting new queries
    and viewing historical queries.
    """
    st.header("Patient Portal")

    submit_tab, queries_tab, help_tab = st.tabs(["Submit Query", "My Queries", "Help"])

    with submit_tab:
        st.subheader("Submit a Medical Query")
        patient_id = st.session_state.get("patient_id", "P001")
        with st.form(key="query_form"):
            medical_question = st.text_area("Your medical question:", height=150)
            uploaded_file = st.file_uploader("Upload medical documents (optional)")
            submit_button = st.form_submit_button(label="Submit Query")

        if submit_button and medical_question:
            with st.spinner("Submitting your query..."):
                payload = {"patient_id": patient_id, "query": medical_question}
                try:
                    import os

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
api_response = requests.post(f"{BACKEND_URL}/process_query/", json=payload)
                    api_response.raise_for_status()
                    response_data = api_response.json()
                    st.success(response_data.get("final_response_to_patient", "Query submitted successfully!"))
                except requests.exceptions.RequestException:
                    st.error("Could not connect to the backend service.")

    with queries_tab:
        st.subheader("Your Query History")
        patient_id = st.session_state.get("patient_id", "P001")
        
        if st.button("Refresh History"):
            st.rerun()

        try:
            # THE FIX: Call the new endpoint to get this patient's queries
            response = requests.get(f"{BACKEND_URL}/queries/by_patient/{patient_id}")
            response.raise_for_status()
            my_queries = response.json()

            if not my_queries:
                st.info("You have not submitted any queries yet.")
            else:
                display_data = []
                for q in my_queries:
                    try:
                        date_str = datetime.fromisoformat(q.get("timestamp", "")).strftime('%Y-%m-%d %H:%M')
                    except (ValueError, TypeError):
                        date_str = "N/A"
                        
                    display_data.append({
                        "Date Submitted": date_str,
                        "Your Query": q.get("original_query"),
                        "Status": q.get("status", "N/A").replace("_", " ").title(),
                        "Doctor's Response": q.get("doctor_final_response", "Awaiting Review...")
                    })
                
                df = pd.DataFrame(display_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

        except requests.exceptions.RequestException:
            st.error("Could not fetch your query history.")

    with help_tab:
        st.subheader("Help & Support")
        st.write("If you are experiencing a medical emergency, please call your local emergency services immediately.")
