from flask import Flask, jsonify
from flask_cors import CORS
from database import mongo
import logging

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/hospitalDB"
app.config["SECRET_KEY"] = "hospital-secret-key-2024"

mongo.init_app(app)
CORS(app)

logging.basicConfig(level=logging.INFO)

# Register blueprints
from routes.auth import auth
from routes.appointment import appointment
from routes.doctor import doctor
from routes.admin import admin

app.register_blueprint(auth)
app.register_blueprint(appointment)
app.register_blueprint(doctor)
app.register_blueprint(admin)

# Global error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Internal server error"}), 500

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

if __name__ == "__main__":
    app.run(debug=True)
