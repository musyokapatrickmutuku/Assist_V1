import streamlit as st

# Set page config
st.set_page_config(
    page_title="Assist: Diabetes Care Companion",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Simplified CSS - only hide sidebar and ensure proper contrast
st.markdown('''
    <style>
        section[data-testid="stSidebar"] {
            display: none;
        }
        div.stButton > button {
            background-color: #f8cdfa;
            color: #700675;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 1px;
            padding: 0.8rem 0;
            font-size: 1.2rem;
            border: none;
            border-radius: 10px;
        }
        
    </style>
''', unsafe_allow_html=True)

# Function to generate response for diabetes-related questions
def generate_response(query):
    if not query.strip():
        return "Please enter a valid question about diabetes."

    query_lower = query.lower()

    if "blood sugar" in query_lower or "glucose" in query_lower:
        return "To manage your blood sugar, monitor regularly, eat balanced meals low in refined sugar, and follow your treatment plan. If readings are consistently high or low, contact your healthcare provider."
    elif "insulin" in query_lower:
        return "Insulin helps regulate blood sugar. Always follow your prescribed dosage, store insulin properly, and monitor for signs of hypoglycemia (like dizziness or sweating)."
    elif "hypoglycemia" in query_lower or "low sugar" in query_lower:
        return "If you experience low blood sugar: eat or drink something with fast-acting sugar (like juice or glucose tablets). Recheck levels in 15 minutes. If symptoms persist, seek medical help."
    elif "diet" in query_lower or "food" in query_lower:
        return "A diabetes-friendly diet includes whole grains, lean proteins, non-starchy vegetables, and healthy fats. Avoid sugary drinks and limit processed carbs."
    elif "exercise" in query_lower or "workout" in query_lower:
        return "Exercise can help control blood sugar. Aim for 30 minutes most days. Check your levels before and after activity, and carry a quick snack in case of hypoglycemia."
    else:
        return f"Thank you for your question: '{query}'. While this assistant provides general diabetes advice, please consult a healthcare provider for personalized care."

# Main UI
#st.title("🏥 Meet Assist — Your Friendly Health Helper for Diabetes")
st.subheader("**Meet Assist — Your Friendly Health Helper for Diabetes**")
st.write("**Struggling to explain your symptoms or ask for the right treatment? Assist helps you turn your thoughts into clear, accurate requests your doctor will understand. It’s like having a smart friend by your side who knows diabetes—and speaks doctor!**")


# Input section
patient_query = st.text_input(
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
send_button = st.button("🔍 Get Answer", use_container_width=True)

# Response section
if send_button and patient_query:
    with st.spinner("Generating response..."):
        response = generate_response(patient_query)
    
    st.markdown("### 📋 Response:")
    st.info(response)

    
    st.warning("⚠️ **Disclaimer:** This assistant provides general health information and is not a substitute for professional medical advice.")
elif send_button and not patient_query:
    st.error("Please enter a question before submitting.")

# Footer
st.markdown("---")
st.markdown("*Assist MVP — Built for diabetes care with Streamlit*")
