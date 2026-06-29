from flask import Blueprint, jsonify, request
import os
import json
from groq import Groq

itinerary_bp = Blueprint("itinerary", __name__)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@itinerary_bp.route("/", methods=["POST"])
def generate_itinerary():
    data = request.get_json(force=True)
    if isinstance(data, str):
        data = json.loads(data)

    district = data.get("district")
    days = data.get("days", 2)
    interests = data.get("interests", [])

    if not district:
        return jsonify({"success": False, "message": "District is required"}), 400

    interests_str = ", ".join(interests) if interests else "general sightseeing"

    prompt = f"""Create a {days}-day tourism itinerary for {district}, Jharkhand, India.
Tourist interests: {interests_str}.

STRICT RULES:
- Group places by proximity — places in same area/direction must be on same day
- Never mix city center places with far-away places on same day
- Morning → temples, waterfalls, nature spots (cool weather, less crowd)
- Afternoon → museums, zoos, indoor places (open midday)
- Evening → markets, hills, lakes, food streets (lively after sunset)
- Include realistic opening hours for each place
- Include travel tip if place is far from city
- Day 1 should cover city center places, Day 2+ for places outside city

Respond with ONLY a JSON array. No text before or after. No markdown. Just raw JSON:
[
  {{
    "day": 1,
    "morning": {{
      "activity": "place and what to do there",
      "time": "7:00 AM - 10:00 AM",
      "reason": "why this time is best",
      "travel_tip": "only include if place is far, else empty string"
    }},
    "afternoon": {{
      "activity": "place and what to do there",
      "time": "11:00 AM - 2:00 PM",
      "reason": "why this time is best",
      "travel_tip": ""
    }},
    "evening": {{
      "activity": "place and what to do there",
      "time": "5:00 PM - 8:00 PM",
      "reason": "why this time is best",
      "travel_tip": ""
    }}
  }}
]"""

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

    raw = raw.strip()

    if raw.startswith('"') and raw.endswith('"'):
        raw = json.loads(raw)

    try:
        itinerary_data = json.loads(raw)
        return jsonify({"success": True, "district": district, "days": days, "itinerary": itinerary_data})
    except Exception as e:
        try:
            itinerary_data = json.loads(json.loads(raw))
            return jsonify({"success": True, "district": district, "days": days, "itinerary": itinerary_data})
        except:
            return jsonify({"success": True, "district": district, "days": days, "itinerary": raw, "raw": True, "error": str(e)})