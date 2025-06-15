# assistMVP/streamlit_app/doctor.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def doctor_portal():
    """
    Renders the main doctor portal interface, including tabs for reviewing
    pending queries and viewing completed ones.
    """
    st.header("Doctor Portal")

    # Create the tabbed interface based on the UI design
    review_tab, completed_tab, help_tab = st.tabs(["Review Queries", "Completed Reviews", "Help"])

    # --- Review Queries Tab ---
    with review_tab:
        st.subheader("Queries Awaiting Review")
        st.write("Review patient queries and the AI-generated suggestions, then edit and approve the final response.")

        if st.button("Refresh Queries"):
            st.rerun()

        try:
            # Call the backend API to fetch queries with 'pending_review' status
            response = requests.get("http://localhost:8000/pending_queries/")
            response.raise_for_status()
            pending_queries = response.json()

        except requests.exceptions.RequestException as e:
            st.error("Could not fetch pending queries from the backend service. Please ensure it is running.")
            pending_queries = []

        if not pending_queries:
            st.info("No queries are currently awaiting review.")
        else:
            # Loop through each pending query and display it in its own container
            for query in pending_queries:
                with st.container(border=True):
                    # Display key information about the query
                    st.markdown(f"**Patient ID:** `{query.get('patient_id', 'N/A')}`")
                    st.markdown(f"**Patient's Question:**")
                    st.info(query.get('original_query', 'Question not found.'))
                    
                    st.markdown(f"**AI-Generated Suggestion (for your review):**")
                    st.warning(query.get('ai_response', 'No AI response generated.'))

                    st.markdown("---")
                    
                    # Text area for the doctor to write or edit the final response
                    # It's pre-filled with the AI's suggestion for easy editing.
                    final_response_text = st.text_area(
                        "Final Response to Patient:", 
                        value=query.get('ai_response', ''), # Pre-fill with AI response
                        key=f"response_{query['id']}",
                        height=150
                    )
                    
                    # Button to approve and finalize the query
                    if st.button("Approve & Send Final Response", key=f"approve_{query['id']}"):
                        if not final_response_text.strip():
                            st.error("The final response cannot be empty.")
                        else:
                            # Prepare the payload for the backend API
                            payload = {
                                "new_status": "approved", 
                                "doctor_response": final_response_text
                            }
                            try:
                                # Call the backend endpoint to update the query's status
                                update_response = requests.post(f"http://localhost:8000/update_query/{query['id']}", json=payload)
                                update_response.raise_for_status()
                                st.success(f"Query for Patient {query['patient_id']} has been approved and finalized.")
                                st.rerun() # Refresh the page to remove the approved query
                            except requests.exceptions.RequestException as e:
                                st.error(f"Failed to approve query. Could not connect to the backend.")

    # --- Completed Reviews Tab (Placeholder) ---
    with completed_tab:
        st.subheader("Your Reviewed Queries")
        st.info("This section will show a history of queries you have already reviewed. (Functionality to be implemented)")
        # TODO: Add an API endpoint and call to fetch completed reviews for this doctor.

    # --- Help Tab ---
    with help_tab:
        st.subheader("Help & Support")
        st.write("This portal is for reviewing AI-assisted patient queries. All final responses are your own and should be based on your professional medical judgment.")
        st.write("For technical issues, please contact the IT department.")
