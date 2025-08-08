import streamlit as st
import sqlite3
import uuid
from datetime import datetime
import os

# Configure the page
st.set_page_config(
    page_title="CivicAI – Complaint Assistant", 
    page_icon="📣",
    layout="centered"
)

# Initialize database
@st.cache_resource
def init_database():
    """Initialize SQLite database for storing complaints"""
    conn = sqlite3.connect('complaints.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            id TEXT PRIMARY KEY,
            user_id TEXT,
            original_text TEXT,
            translated_text TEXT,
            language TEXT,
            category TEXT,
            department TEXT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    return conn

# Language detection and translation (simplified version)
@st.cache_data
def detect_and_translate(text):
    """
    Simple language detection and translation function
    In production, you'd use Google Translate API or similar
    """
    # Simple heuristic - check for common non-English patterns
    hindi_chars = any(ord(char) > 2303 and ord(char) < 2431 for char in text)
    arabic_chars = any(ord(char) > 1535 and ord(char) < 1791 for char in text)
    
    if hindi_chars:
        return "hi", text  # In production, translate to English here
    elif arabic_chars:
        return "ar", text  # In production, translate to English here
    else:
        return "en", text

# Complaint classification
@st.cache_data
def classify_complaint(text):
    """
    Simple keyword-based complaint classification
    In production, you'd use a trained ML model
    """
    text_lower = text.lower()
    
    # Infrastructure keywords
    if any(word in text_lower for word in ['pothole', 'road', 'street', 'highway', 'bridge', 'traffic']):
        return "Infrastructure"
    
    # Water/Sanitation keywords
    elif any(word in text_lower for word in ['water', 'leak', 'pipe', 'drainage', 'sewer', 'toilet', 'sanitation']):
        return "Water & Sanitation"
    
    # Waste Management keywords
    elif any(word in text_lower for word in ['garbage', 'trash', 'waste', 'dump', 'litter', 'cleaning']):
        return "Waste Management"
    
    # Utilities keywords
    elif any(word in text_lower for word in ['electricity', 'power', 'light', 'streetlight', 'electric']):
        return "Utilities"
    
    # Public Safety keywords
    elif any(word in text_lower for word in ['crime', 'safety', 'police', 'security', 'violence', 'theft']):
        return "Public Safety"
    
    # Public Transport keywords
    elif any(word in text_lower for word in ['bus', 'transport', 'metro', 'train', 'taxi', 'rickshaw']):
        return "Public Transport"
    
    # Health keywords
    elif any(word in text_lower for word in ['health', 'hospital', 'medical', 'doctor', 'clinic']):
        return "Health Services"
    
    # Education keywords
    elif any(word in text_lower for word in ['school', 'education', 'teacher', 'student', 'college']):
        return "Education"
    
    else:
        return "General"

# Department routing
@st.cache_data
def get_department(category):
    """Route complaints to appropriate departments"""
    department_mapping = {
        "Infrastructure": "Public Works Department",
        "Water & Sanitation": "Water & Sewerage Department",
        "Waste Management": "Municipal Corporation",
        "Utilities": "Electricity Board",
        "Public Safety": "Police Department",
        "Public Transport": "Transport Department",
        "Health Services": "Health Department",
        "Education": "Education Department",
        "General": "General Administration"
    }
    return department_mapping.get(category, "General Administration")

# Store complaint in database
def store_complaint(conn, user_id, original_text, translated_text, language, category, department):
    """Store complaint in SQLite database"""
    complaint_id = str(uuid.uuid4())[:8].upper()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO complaints 
        (id, user_id, original_text, translated_text, language, category, department, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (complaint_id, user_id, original_text, translated_text, language, category, department, "Received"))
    conn.commit()
    return complaint_id

# Main Streamlit App
def main():
    # Initialize database
    conn = init_database()
    
    # Header
    st.title("📣 CivicAI – Smart Civic Complaint Assistant")
    st.markdown("Report issues like potholes, water leaks, garbage, and more in your own words!")
    st.markdown("---")
    
    # Sidebar for additional features
    with st.sidebar:
        st.header("📊 Dashboard")
        
        # Show complaint statistics
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM complaints")
        total_complaints = cursor.fetchone()[0]
        
        cursor.execute("SELECT category, COUNT(*) FROM complaints GROUP BY category")
        category_stats = cursor.fetchall()
        
        st.metric("Total Complaints", total_complaints)
        
        if category_stats:
            st.subheader("Categories")
            for category, count in category_stats:
                st.write(f"• {category}: {count}")
    
    # Main form
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Submit Your Complaint")
        
        # Input fields
        user_id = st.text_input("Your Name or ID (optional)", placeholder="Enter your name or ID")
        text = st.text_area(
            "Describe your complaint", 
            placeholder="Describe the issue you're facing in detail. You can write in English, Hindi, or any other language.",
            height=150
        )
        
        # Submit button
        if st.button("🚀 Submit Complaint", type="primary"):
            if text.strip() == "":
                st.warning("⚠️ Please describe your complaint before submitting.")
            else:
                with st.spinner("Processing your complaint..."):
                    try:
                        # Process the complaint
                        lang, translated_text = detect_and_translate(text)

                        category = classify_complaint(translated_text)
                        department = get_department(category)
                        
                        # Store in database
                        complaint_id = store_complaint(
                            conn, 
                            user_id if user_id else "anonymous", 
                            text, 
                            translated_text, 
                            lang, 
                            category, 
                            department
                        )
                        
                        # Success message
                        st.success("✅ Complaint submitted successfully!")
                        
                        # Display results
                        st.markdown("### 📋 Complaint Details")
                        
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.info(f"**Complaint ID**: `{complaint_id}`")
                            st.info(f"**Category**: {category}")
                        with col_b:
                            st.info(f"**Department**: {department}")
                            st.info(f"**Status**: Received")
                        
                        # Show next steps
                        st.markdown("### 🔄 What happens next?")
                        st.markdown(f"""
                        1. Your complaint has been forwarded to **{department}**
                        2. You will receive updates on complaint ID: `{complaint_id}`
                        3. Expected response time: 3-5 business days
                        4. You can track your complaint status using the ID above
                        """)
                        
                    except Exception as e:
                        st.error(f"❌ Something went wrong: {str(e)}")
    
    with col2:
        st.subheader("💡 Tips")
        st.markdown("""
        **For better results:**
        • Be specific about the location
        • Include relevant details
        • Mention urgency level
        • Add contact information
        
        **Supported Languages:**
        • English
        • Hindi
        • And many more!
        
        **Common Categories:**
        • Infrastructure
        • Water & Sanitation
        • Waste Management
        • Utilities
        • Public Safety
        • Transport
        """)
    
    # Recent complaints section
    st.markdown("---")
    st.subheader("📝 Recent Complaints")
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, category, department, status, created_at FROM complaints ORDER BY created_at DESC LIMIT 5")
    recent_complaints = cursor.fetchall()
    
    if recent_complaints:
        for complaint in recent_complaints:
            complaint_id, category, department, status, created_at = complaint
            
            with st.expander(f"Complaint {complaint_id} - {category}"):
                col_x, col_y, col_z = st.columns(3)
                with col_x:
                    st.write(f"**Department:** {department}")
                with col_y:
                    st.write(f"**Status:** {status}")
                with col_z:
                    st.write(f"**Date:** {created_at}")
    else:
        st.info("No complaints submitted yet. Be the first to report an issue!")

if __name__ == "__main__":
    main()
