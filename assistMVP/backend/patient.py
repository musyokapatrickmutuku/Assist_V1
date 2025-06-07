import streamlit as st
import json
from datetime import datetime
from pending_queries import generate_response, save_query

# Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Patient Page
def patient_page():
    st.title("🩺 Ask Assist")

    # Input section
    patient_query = st.text_area(
        "💬 Ask a question about diabetes:",
        placeholder="e.g., What should I eat if my blood sugar is high?"
    )
    st.markdown("---")
    # File upload section
    st.markdown(" ***📂 Upload a file (optional)***")
    uploaded_file = st.file_uploader(
        "Upload lab results, blood test reports, or doctor notes to help us understand your situation better:",
        type=["pdf", "jpg", "jpeg", "png"]
    )

    # Process file if uploaded
    if uploaded_file is not None:
        file_details = {
            "filename": uploaded_file.name,
            "filetype": uploaded_file.type,
            "filesize": uploaded_file.size
        }
        st.success(f"Uploaded file: {file_details['filename']} ({file_details['filetype']}, {file_details['filesize'] // 1024} KB)")

        # Optional: Display image previews
        if uploaded_file.type.startswith("image"):
            from PIL import Image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded image", use_column_width=True)

        elif uploaded_file.type == "application/pdf":
            st.markdown("✅ PDF uploaded. (File preview not shown)")



    # Custom styled button
    st.markdown("""
        <style>
        div.stButton > button {
            background-color: black;
            color: white;
            border: none;
            border-radius: 4px;
            padding: 0.3rem 0.8rem;
            font-weight: bold;
            width: 40%;
            margin: 0 auto;
            display: block;
        }
        div.stButton > button:hover {
            background-color: #553287;
            color: #fff;
        }
        </style>
    """, unsafe_allow_html=True)
    send_button = st.button("**SEND YOUR QUESTION**", use_container_width=True)
    # Response section
    if send_button and patient_query:
        with st.spinner("Generating response..."):
            response = generate_response(patient_query)
            save_query(patient_query, response)
            
        # Display response
        st.success("Your health question is now under review by your doctor. You'll hear back soon!")
        st.write("AI Response:", response)
        # st.markdown("### 📋 Response:")
        # st.info(response)

        
        st.warning("⚠️ **Disclaimer:** This assistant provides general health information and is not a substitute for professional medical advice.")
    elif send_button and not patient_query:
        st.error("Please enter a question before submitting.")
