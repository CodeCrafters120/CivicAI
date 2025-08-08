from flask import Flask, request, jsonify
from classify import classify_complaint
from detect_language import detect_and_translate
from complaint_router import get_department
from database import store_complaint

app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit_complaint():
    text = request.json["text"]
    user_id = request.json.get("user_id", "anonymous")

    lang, translated_text = detect_and_translate(text)
    category = classify_complaint(translated_text)
    department = get_department(category)

    complaint_id = store_complaint(user_id, text, category, department)

    return jsonify({
        "complaint_id": complaint_id,
        "category": category,
        "department": department,
        "status": "Received"
    })

if __name__ == "__main__":
    app.run(debug=True)
