from flask import Blueprint, jsonify

places_bp = Blueprint("places", __name__)

PLACES = [
    {
        "id": 1,
        "name": "Hundru Falls",
        "category": "waterfall",
        "district": "Ranchi",
        "description": "One of the highest waterfalls in Jharkhand.",
        "best_season": "July to October"
    },
    {
        "id": 2,
        "name": "Betla National Park",
        "category": "wildlife",
        "district": "Latehar",
        "description": "Home to tigers, elephants and diverse flora.",
        "best_season": "November to February"
    },
    {
        "id": 3,
        "name": "Deoghar Temple",
        "category": "religious",
        "district": "Deoghar",
        "description": "One of the 12 Jyotirlingas, major pilgrimage site.",
        "best_season": "Year round"
    },
    {
    "id": 5,
    "name": "Dassam Falls",
    "category": "waterfall",
    "district": "Ranchi",
    "description": "A magnificent waterfall on the Kanchi river.",
    "best_season": "July to October"
},
{
    "id": 6,
    "name": "Pahari Mandir",
    "category": "religious",
    "district": "Ranchi",
    "description": "A hilltop temple dedicated to Lord Shiva with panoramic city views.",
    "best_season": "Year round"
},
{
    "id": 7,
    "name": "Tagore Hill",
    "category": "nature",
    "district": "Ranchi",
    "description": "A scenic hill where Rabindranath Tagore stayed, offering beautiful views.",
    "best_season": "October to March"
},
{
    "id": 8,
    "name": "Betla National Park",
    "category": "wildlife",
    "district": "Latehar",
    "description": "One of the first national parks in India with tigers and elephants.",
    "best_season": "November to February"
},
{
    "id": 9,
    "name": "Netarhat",
    "category": "nature",
    "district": "Latehar",
    "description": "Queen of Chotanagpur, famous for sunrise and sunset views.",
    "best_season": "October to February"
},
{
    "id": 10,
    "name": "Jubilee Lake",
    "category": "nature",
    "district": "Jamshedpur",
    "description": "A beautiful artificial lake in the heart of Jamshedpur city.",
    "best_season": "Year round"
},
{
    "id": 11,
    "name": "Dimna Lake",
    "category": "nature",
    "district": "Jamshedpur",
    "description": "A picturesque reservoir surrounded by hills, perfect for picnics.",
    "best_season": "October to March"
},
{
    "id": 12,
    "name": "Baidyanath Temple",
    "category": "religious",
    "district": "Deoghar",
    "description": "One of the 12 Jyotirlingas, one of the most sacred Shiva temples in India.",
    "best_season": "Year round"
},
{
    "id": 13,
    "name": "Usri Falls",
    "category": "waterfall",
    "district": "Giridih",
    "description": "A beautiful waterfall near Giridih surrounded by dense forest.",
    "best_season": "July to October"
},
{
    "id": 14,
    "name": "Parasnath Hill",
    "category": "religious",
    "district": "Giridih",
    "description": "The highest peak in Jharkhand, sacred to Jains with 24 temples.",
    "best_season": "October to March"
},
{
    "id": 15,
    "name": "Lodh Falls",
    "category": "waterfall",
    "district": "Latehar",
    "description": "The highest waterfall in Jharkhand at 143 meters, stunning and remote.",
    "best_season": "July to October"
}
]

@places_bp.route("/", methods=["GET"])
def get_all_places():
    return jsonify({"success": True, "data": PLACES})



@places_bp.route("/<int:place_id>", methods=["GET"])
def get_place(place_id):
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if not place:
        return jsonify({"success": False, "message": "Place not found"}), 404
    return jsonify({"success": True, "data": place})

    # for p in PLACES:
    #  if p["id"] == place_id:
    #     return jsonify({"success": True, "data": p})
    # return jsonify({"success": False, "message": "Place not found"}), 404


@places_bp.route("/search" , methods = ["GET"])
def search_places():
    query = request.args.get("q" , "")

    if not query:
        return jsonify({"success": False , "messages": "Please provide a search term"}), 400
    
    query = query.lower()

    result=[]

    for p in PLACES:
        if query in p["name"].lower():
            result.append(p)

    
    return jsonify({"success": True , "count": len(result) , "data": result})



from flask import Blueprint, jsonify, request  # add request here at top

@places_bp.route("/filter", methods=["GET"])
def filter_places():
    category = request.args.get("category")
    district = request.args.get("district")

    result = PLACES

    if category:
        result = [p for p in result if p["category"] == category]
    if district:
        result = [p for p in result if p["district"] == district]

    return jsonify({"success": True, "count": len(result), "data": result})


