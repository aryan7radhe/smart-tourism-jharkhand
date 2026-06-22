from flask import Blueprint , jsonify , request
import requests
import os


weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/" , methods = ["GET"])
def get_weather():
    district = request.args.get("district")

    if not district:
        return jsonify({"success": False, "message": "District is required"}), 400
    
    api_key = os.getenv("OPENWEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={district},IN&appid={api_key}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return  jsonify({"success": False, "message": "City not found"}), 404
    
    result = {
        "district": district,
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "description": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }
    
    return jsonify({"success": True, "data": result})