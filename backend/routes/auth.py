from flask import Blueprint, request, jsonify
from database import mongo
import bcrypt
import re
from datetime import datetime

auth = Blueprint("auth", __name__)

def validate_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def validate_password(password):
    return len(password) >= 6

def validate_phone(phone):
    return re.match(r'^\+?[\d\s\-]{10,15}$', phone)

def check_password(plain, hashed):
    # Fix: handle both bytes and string stored passwords
    if isinstance(hashed, str):
        hashed = hashed.encode("utf-8")
    return bcrypt.checkpw(plain.encode("utf-8"), hashed)


# ─── SEED ADMIN (visit once, then remove) ───────────────────────────────────
@auth.route("/seed-admin")
def seed_admin():
    existing = mongo.db.users.find_one({"email": "admin@hospital.com"})
    if existing:
        return jsonify({"message": "Admin already exists"}), 200

    hashed = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
    mongo.db.users.insert_one({
        "name": "Admin",
        "email": "admin@hospital.com",
        "password": hashed,
        "role": "admin",
        "is_active": True,
        "created_at": datetime.utcnow().isoformat()
    })
    return jsonify({"message": "Admin created! Email: admin@hospital.com | Password: admin123"}), 201


# ─── PATIENT REGISTER ────────────────────────────────────────────────────────
@auth.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required = ["name", "email", "password"]
        for field in required:
            if not data.get(field, "").strip():
                return jsonify({"error": f"{field.capitalize()} is required"}), 400

        if not validate_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        if not validate_password(data["password"]):
            return jsonify({"error": "Password must be at least 6 characters"}), 400

        if data.get("phone") and not validate_phone(data["phone"]):
            return jsonify({"error": "Invalid phone number"}), 400

        existing = mongo.db.users.find_one({"email": data["email"].lower()})
        if existing:
            return jsonify({"error": "Email already registered"}), 409

        hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

        user_doc = {
            "name": data["name"].strip(),
            "email": data["email"].lower().strip(),
            "password": hashed,
            "role": "patient",
            "phone": data.get("phone", ""),
            "age": data.get("age", ""),
            "blood_group": data.get("blood_group", ""),
            "address": data.get("address", ""),
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }

        mongo.db.users.insert_one(user_doc)
        return jsonify({"message": "Registration successful! You can now login."}), 201

    except Exception as e:
        return jsonify({"error": "Registration failed. Please try again."}), 500


# ─── LOGIN ───────────────────────────────────────────────────────────────────
@auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        if not data.get("email") or not data.get("password"):
            return jsonify({"error": "Email and password are required"}), 400

        user = mongo.db.users.find_one({"email": data["email"].lower().strip()})
        if not user:
            return jsonify({"error": "No account found with this email"}), 404

        if not user.get("is_active", True):
            return jsonify({"error": "Account has been deactivated"}), 403

        if check_password(data["password"], user["password"]):
            return jsonify({
                "message": "Login successful",
                "user": {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"],
                    "phone": user.get("phone", ""),
                    "age": user.get("age", ""),
                    "blood_group": user.get("blood_group", ""),
                    "address": user.get("address", ""),
                    "specialization": user.get("specialization", "")
                }
            }), 200

        return jsonify({"error": "Incorrect password"}), 401

    except Exception as e:
        return jsonify({"error": "Login failed. Please try again."}), 500


# ─── REGISTER DOCTOR (admin only) ────────────────────────────────────────────
@auth.route("/register-doctor", methods=["POST"])
def register_doctor():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        required = ["name", "email", "password", "specialization"]
        for field in required:
            if not data.get(field, "").strip():
                return jsonify({"error": f"{field.capitalize()} is required"}), 400

        if not validate_email(data["email"]):
            return jsonify({"error": "Invalid email format"}), 400

        existing = mongo.db.users.find_one({"email": data["email"].lower()})
        if existing:
            return jsonify({"error": "Email already registered"}), 409

        hashed = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())

        doctor_doc = {
            "name": data["name"].strip(),
            "email": data["email"].lower().strip(),
            "password": hashed,
            "role": "doctor",
            "specialization": data["specialization"].strip(),
            "phone": data.get("phone", ""),
            "department": data.get("department", ""),
            "experience": data.get("experience", ""),
            "available_days": data.get("available_days", []),
            "created_at": datetime.utcnow().isoformat(),
            "is_active": True
        }

        mongo.db.users.insert_one(doctor_doc)
        return jsonify({"message": "Doctor registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": "Doctor registration failed."}), 500


# ─── GET ALL DOCTORS (public) ─────────────────────────────────────────────────
@auth.route("/doctors", methods=["GET"])
def get_doctors():
    try:
        search = request.args.get("search", "").strip()
        specialization = request.args.get("specialization", "").strip()

        query = {"role": "doctor", "is_active": True}

        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"specialization": {"$regex": search, "$options": "i"}},
                {"department": {"$regex": search, "$options": "i"}}
            ]
        if specialization:
            query["specialization"] = {"$regex": specialization, "$options": "i"}

        doctors = list(mongo.db.users.find(query, {"password": 0}))
        for d in doctors:
            d["_id"] = str(d["_id"])
        return jsonify(doctors), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch doctors"}), 500


# ─── GET USER PROFILE ─────────────────────────────────────────────────────────
@auth.route("/profile/<email>", methods=["GET"])
def get_profile(email):
    try:
        user = mongo.db.users.find_one({"email": email.lower()}, {"password": 0})
        if not user:
            return jsonify({"error": "User not found"}), 404
        user["_id"] = str(user["_id"])
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch profile"}), 500


# ─── UPDATE PROFILE ───────────────────────────────────────────────────────────
@auth.route("/profile/<email>", methods=["PUT"])
def update_profile(email):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        allowed = ["name", "phone", "age", "blood_group", "address"]
        update_data = {k: v for k, v in data.items() if k in allowed}

        if not update_data:
            return jsonify({"error": "No valid fields to update"}), 400

        mongo.db.users.update_one(
            {"email": email.lower()},
            {"$set": update_data}
        )
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to update profile"}), 500