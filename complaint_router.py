def get_department(category):
    routing = {
        "Water Leakage": "Hydraulic Department",
        "Garbage Issue": "Solid Waste Department",
        "Road/Pothole": "Road Maintenance",
        "Sanitation": "Public Health",
        "Streetlight Fault": "Electrical Department",
        "Drainage Blockage": "Storm Water Drain"
    }
    return routing.get(category, "General Admin")
