import streamlit as st
import json
from datetime import datetime
from pending_queries import generate_response, save_query


# Patient Page
def patient_page():
    st.title("🩺 AI Health Assistant")

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



    # Full-width button without columns
    send_button = st.button("🔍 Ask Assist", use_container_width=True)       
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
