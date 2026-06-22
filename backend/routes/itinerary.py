from flask import Blueprint, jsonify,request
import os
from groq import Groq

itinerary_bp = Blueprint("itinerary" , __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@itinerary_bp.route("/" , methods=["POST"])
def generate_itinerary():
    data = request.get_json()

    district = data.get("district")
    days = data.get("days" , 2)
    interests = data.get("interests", [])

    if not district:
        return jsonify({"success": False, "message": "District is required"}), 400

    prompt = f"""
    Create a {days}-day tourism itinerary for {district}, Jharkhand, India.
    Tourist interests: {", ".join(interests) if interests else "general sightseeing"}.
    Format it day by day with morning, afternoon and evening activities.
    Keep it concise and practical.
    """

    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a helpful travel guide for Jharkhand, India."},
            {"role": "user", "content": prompt}
        ]
    )

    result = chat.choices[0].message.content

    return jsonify({"success": True, "district": district, "days": days, "itinerary": result})