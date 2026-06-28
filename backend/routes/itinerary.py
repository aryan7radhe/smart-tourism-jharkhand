from flask import Blueprint, jsonify, request
import os
import json
from groq import Groq

itinerary_bp = Blueprint("itinerary", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@itinerary_bp.route("/", methods=["POST"])
def generate_itinerary():
    data = request.get_json()
    district = data.get("district")
    days = data.get("days", 2)
    interests = data.get("interests", [])

    if not district:
        return jsonify({"success": False, "message": "District is required"}), 400

    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = f"""Create a {days}-day tourism itinerary for {district}, Jharkhand, India.
Tourist interests: {interests_str}.
Respond with ONLY a JSON array. No text before or after. No markdown. Just raw JSON like this:
[{{"day": 1, "morning": "activity", "afternoon": "activity", "evening": "activity"}}]"""

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a travel guide. Always respond with valid JSON only, no markdown, no extra text."},
            {"role": "user", "content": prompt}
        ]
    )

    raw = chat.choices[0].message.content.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    try:
        itinerary_data = json.loads(raw)
        return jsonify({"success": True, "district": district, "days": days, "itinerary": itinerary_data})
    except:
        return jsonify({"success": True, "district": district, "days": days, "itinerary": raw, "raw": True})