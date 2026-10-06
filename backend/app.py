"""
University Research Opportunity Portal - Flask backend.

Run:  python app.py
Then open http://localhost:5000 in the browser (the frontend is served here too).
"""
import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import FLASK_PORT
from routes.opportunities import opportunities_bp

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend")

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
CORS(app)  # allows the frontend to call the API even if opened from another origin

app.register_blueprint(opportunities_bp)


# ---------------------------------------------------------------- frontend

@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")


# ---------------------------------------------------------------- JSON error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=FLASK_PORT, debug=False)
