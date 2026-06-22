from flask import Flask
from flask_cors import CORS
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

from routes.places import places_bp
from routes.itinerary import itinerary_bp 

app.register_blueprint(places_bp, url_prefix="/api/places")
app.register_blueprint(itinerary_bp, url_prefix="/api/itinerary")


@app.route("/")
def home():
    return {"message": "Smart Tourism Jharkhand API is running!"}

if __name__ == "__main__":
    app.run(debug=True)