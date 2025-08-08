def classify_complaint(text):
    keywords = {
        "water": "Water Leakage",
        "pothole": "Road/Pothole",
        "garbage": "Garbage Issue",
        "toilet": "Sanitation",
        "light": "Streetlight Fault",
        "drain": "Drainage Blockage"
    }
    for k, v in keywords.items():
        if k in text.lower():
            return v
    return "General Complaint"
