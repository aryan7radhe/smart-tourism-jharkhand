from flask import Blueprint, jsonify, request
import requests
import os
import json
from utils.cache import get_cache, set_cache

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/", methods=["GET"])
def get_weather():
    district = request.args.get("district")

    if not district:
        return jsonify({"success": False, "message": "District is required"}), 400

    # Check cache first
    cache_key = f"weather:{district}"
    cached = get_cache(cache_key)
    if cached:
        return jsonify({"success": True, "data": json.loads(cached), "cached": True})

    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={district},IN&appid={api_key}&units=metric"

    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return jsonify({"success": False, "message": "City not found"}), 404

    result = {
        "district": district,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

    # Cache for 1 hour
    set_cache(cache_key, json.dumps(result), expire_seconds=3600)

    return jsonify({"success": True, "data": result})