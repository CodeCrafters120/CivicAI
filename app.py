# app.py

import streamlit as st
from classify import classify_complaint
from detect_language import detect_and_translate
from complaint_router import get_department

st.title("🛠️ CivicAI - Complaint Classifier")

st.markdown("This tool classifies civic complaints by department and type using AI.")

user_input = st.text_area("📝 Enter your complaint:", height=150)

if st.button("🔍 Analyze"):
    if not user_input.strip():
        st.warning("Please enter a complaint.")
    else:
        # Step 1: Translate if needed
        translated = detect_and_translate(user_input)

        # Step 2: Classify complaint type and department
        complaint_type = classify_complaint(translated)
        department = get_department(translated)

        st.success("✅ Analysis complete!")
        st.write("**Translated Complaint:**", translated)
        st.write("**Department:**", department)
        st.write("**Complaint Type:**", complaint_type)
