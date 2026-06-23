from flask import Blueprint, jsonify, request
from utils.db import clicks_collection
from routes.places import PLACES
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

recommend_bp = Blueprint("recommend", __name__)

@recommend_bp.route("/click", methods=["POST"])
def track_click():
    data = request.get_json()
    place_id = data.get("place_id")
    session_id = data.get("session_id")

    if not place_id or not session_id:
        return jsonify({"success": False, "message": "place_id and session_id required"}), 400

    clicks_collection.insert_one({
        "place_id": place_id,
        "session_id": session_id
    })

    return jsonify({"success": True, "message": "Click tracked"})


@recommend_bp.route("/", methods=["GET"])
def get_recommendations():
    session_id = request.args.get("session_id")

    if not session_id:
        return jsonify({"success": False, "message": "session_id required"}), 400

    clicked = list(clicks_collection.find({"session_id": session_id}))
    clicked_ids = [c["place_id"] for c in clicked]

    if not clicked_ids:
        return jsonify({"success": True, "data": [], "message": "No clicks yet"})

    place_content = [
        f"{p['name']} {p['category']} {p['district']} {p['description']}"
        for p in PLACES
    ]

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(place_content)

    clicked_places = [p for p in PLACES if p["id"] in clicked_ids]
    clicked_content = " ".join([
        f"{p['name']} {p['category']} {p['district']}"
        for p in clicked_places
    ])

    user_vector = vectorizer.transform([clicked_content])

    similarities = cosine_similarity(user_vector, tfidf_matrix).flatten()

    scored = [(PLACES[i], similarities[i]) for i in range(len(PLACES)) if PLACES[i]["id"] not in clicked_ids]
    scored.sort(key=lambda x: x[1], reverse=True)
    top3 = [p for p, score in scored[:3]]

    return jsonify({"success": True, "data": top3})