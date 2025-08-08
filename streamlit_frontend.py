import streamlit as st
import requests

st.set_page_config(page_title="CivicAI – Complaint Assistant", layout="centered")

st.title("📣 CivicAI – Smart Civic Complaint Assistant")
st.markdown("Report issues like potholes, water leaks, garbage, and more in your own words!")

user_id = st.text_input("Your Name or ID (optional)", "")
text = st.text_area("Describe your complaint", "")

if st.button("Submit Complaint"):
    if text.strip() == "":
        st.warning("Please describe your complaint before submitting.")
    else:
        response = requests.post("http://localhost:5000/submit", json={
            "user_id": user_id if user_id else "anonymous",
            "text": text
        })

        if response.status_code == 200:
            data = response.json()
            st.success(f"✅ Complaint submitted successfully!")
            st.markdown(f"**Complaint ID**: `{data['complaint_id']}`")
            st.markdown(f"**Category**: {data['category']}")
            st.markdown(f"**Department**: {data['department']}")
            st.markdown(f"**Status**: {data['status']}")
        else:
            st.error("Something went wrong. Please try again later.")
