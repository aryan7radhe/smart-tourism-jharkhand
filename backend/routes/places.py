from flask import Blueprint, jsonify, request

places_bp = Blueprint("places", __name__)

PLACES = [
    {"id": 1, "name": "Hundru Falls", "category": "waterfall", "district": "Ranchi",
     "description": "One of the highest waterfalls in Jharkhand.", "best_season": "July to October",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Hundru%20Falls%2C%20Jharkhand%2C%20India%204.jpg"},
    {"id": 2, "name": "Betla National Park", "category": "wildlife", "district": "Latehar",
     "description": "Home to tigers, elephants and diverse flora.", "best_season": "November to February",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Koel%20river%20at%20betla%20park.jpg"},
    {"id": 3, "name": "Deoghar Temple", "category": "religious", "district": "Deoghar",
     "description": "One of the 12 Jyotirlingas and a major pilgrimage site.", "best_season": "Year round",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Baba%20Baidyanath%20Jyotirlinga%20Temple.jpg"},
    {"id": 4, "name": "Dassam Falls", "category": "waterfall", "district": "Ranchi",
     "description": "A magnificent waterfall on the Kanchi River.", "best_season": "July to October",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Dassam%20falls.jpg"},
    {"id": 5, "name": "Pahari Mandir", "category": "religious", "district": "Ranchi",
     "description": "A hilltop temple dedicated to Lord Shiva with panoramic city views.", "best_season": "Year round",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Pahari%20Mandir%20-%20Ranchi%20Hill%209243.JPG"},
    {"id": 6, "name": "Tagore Hill", "category": "nature", "district": "Ranchi",
     "description": "A scenic hill associated with Rabindranath Tagore, offering beautiful views.", "best_season": "October to March",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Tagore%20hill%20Ranchi.jpg"},
    {"id": 7, "name": "Netarhat", "category": "nature", "district": "Latehar",
     "description": "Known as the Queen of Chotanagpur, famous for sunrise and sunset views.", "best_season": "October to February",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Waterfall%20in%20Netarhat.jpg"},
    {"id": 8, "name": "Jubilee Lake", "category": "nature", "district": "Jamshedpur",
     "description": "A beautiful artificial lake in the heart of Jamshedpur.", "best_season": "Year round",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Jublie%20lake.jpg"},
    {"id": 9, "name": "Dimna Lake", "category": "nature", "district": "Jamshedpur",
     "description": "A picturesque reservoir surrounded by hills, perfect for picnics.", "best_season": "October to March",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Dimna%20Lake%2C%20Jamshedpur.jpg"},
    {"id": 10, "name": "Baidyanath Temple", "category": "religious", "district": "Deoghar",
     "description": "One of the 12 Jyotirlingas and one of the most sacred Shiva temples in India.", "best_season": "Year round",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Baba%20Baidyanath%20Jyotirlinga%20Temple.jpg"},
    {"id": 11, "name": "Usri Falls", "category": "waterfall", "district": "Giridih",
     "description": "A beautiful waterfall near Giridih surrounded by dense forest.", "best_season": "July to October",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Usri%20falls%2Cgiridih%2Cjharkhand.jpg"},
    {"id": 12, "name": "Parasnath Hill", "category": "religious", "district": "Giridih",
     "description": "The highest peak in Jharkhand, sacred to Jains with 24 temples.", "best_season": "October to March",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Shikharji%2002.jpg"},
    {"id": 13, "name": "Lodh Falls", "category": "waterfall", "district": "Latehar",
     "description": "A spectacular waterfall in a remote forested region of Jharkhand.", "best_season": "July to October",
     "image_url": "https://commons.wikimedia.org/wiki/Special:FilePath/Lodh%20falls.jpg"}
]

@places_bp.route("/", methods=["GET"])
def get_all_places():
    return jsonify({"success": True, "count": len(PLACES), "data": PLACES})

@places_bp.route("/<int:place_id>", methods=["GET"])
def get_place(place_id):
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if not place:
        return jsonify({"success": False, "message": "Place not found"}), 404
    return jsonify({"success": True, "data": place})

@places_bp.route("/search", methods=["GET"])
def search_places():
    query = request.args.get("q", "").strip().lower()
    if not query:
        return jsonify({"success": False, "message": "Please provide a search term"}), 400
    result = [p for p in PLACES if query in p["name"].lower() or query in p["district"].lower() or query in p["category"].lower()]
    return jsonify({"success": True, "count": len(result), "data": result})

@places_bp.route("/filter", methods=["GET"])
def filter_places():
    category = request.args.get("category")
    district = request.args.get("district")
    result = PLACES
    if category:
        result = [p for p in result if p["category"].lower() == category.lower()]
    if district:
        result = [p for p in result if p["district"].lower() == district.lower()]
    return jsonify({"success": True, "count": len(result), "data": result})
