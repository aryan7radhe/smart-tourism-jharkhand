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


