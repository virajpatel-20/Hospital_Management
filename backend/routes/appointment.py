from flask import Blueprint, request, jsonify
from database import mongo
from bson.objectid import ObjectId
from datetime import datetime

appointment = Blueprint("appointment", __name__)

def validate_appointment_data(data):
    required = ["patient_name", "patient_email", "doctor_name", "doctor_email", "date", "time"]
    for field in required:
        if not data.get(field, "").strip():
            return False, f"{field.replace('_', ' ').capitalize()} is required"
    try:
        appt_date = datetime.strptime(data["date"], "%Y-%m-%d")
        if appt_date.date() < datetime.utcnow().date():
            return False, "Appointment date cannot be in the past"
    except ValueError:
        return False, "Invalid date format (use YYYY-MM-DD)"
    return True, None


# BOOK APPOINTMENT
@appointment.route("/book-appointment", methods=["POST"])
def book():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400

        is_valid, error_msg = validate_appointment_data(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Check for duplicate appointment (same doctor, date, time)
        existing = mongo.db.appointments.find_one({
            "doctor_email": data["doctor_email"],
            "date": data["date"],
            "time": data["time"],
            "status": {"$nin": ["Cancelled"]}
        })
        if existing:
            return jsonify({"error": "This time slot is already booked with that doctor"}), 409

        mongo.db.appointments.insert_one({
            "patient_name": data["patient_name"].strip(),
            "patient_email": data["patient_email"].lower().strip(),
            "doctor_name": data["doctor_name"].strip(),
            "doctor_email": data["doctor_email"].lower().strip(),
            "date": data["date"],
            "time": data["time"],
            "reason": data.get("reason", "").strip(),
            "notes": data.get("notes", "").strip(),
            "status": "Pending",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        })

        return jsonify({"message": "Appointment booked successfully! Awaiting confirmation."}), 201

    except Exception as e:
        return jsonify({"error": "Failed to book appointment"}), 500


# VIEW PATIENT APPOINTMENTS
@appointment.route("/my-appointments/<email>", methods=["GET"])
def view(email):
    try:
        status_filter = request.args.get("status", "")
        search = request.args.get("search", "").strip()

        query = {"patient_email": email.lower()}
        if status_filter:
            query["status"] = status_filter
        if search:
            query["$or"] = [
                {"doctor_name": {"$regex": search, "$options": "i"}},
                {"reason": {"$regex": search, "$options": "i"}}
            ]

        data = list(mongo.db.appointments.find(query).sort("date", -1))
        for d in data:
            d["_id"] = str(d["_id"])

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch appointments"}), 500


# CANCEL APPOINTMENT (patient)
@appointment.route("/cancel/<id>", methods=["PUT"])
def cancel(id):
    try:
        appt = mongo.db.appointments.find_one({"_id": ObjectId(id)})
        if not appt:
            return jsonify({"error": "Appointment not found"}), 404

        if appt["status"] in ["Completed", "Cancelled"]:
            return jsonify({"error": f"Cannot cancel a {appt['status'].lower()} appointment"}), 400

        mongo.db.appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "Cancelled", "updated_at": datetime.utcnow().isoformat()}}
        )
        return jsonify({"message": "Appointment cancelled successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to cancel appointment"}), 500


# GET APPOINTMENT HISTORY STATS
@appointment.route("/appointment-stats/<email>", methods=["GET"])
def stats(email):
    try:
        pipeline = [
            {"$match": {"patient_email": email.lower()}},
            {"$group": {"_id": "$status", "count": {"$sum": 1}}}
        ]
        result = list(mongo.db.appointments.aggregate(pipeline))
        stats_dict = {r["_id"]: r["count"] for r in result}
        total = sum(stats_dict.values())

        return jsonify({
            "total": total,
            "pending": stats_dict.get("Pending", 0),
            "approved": stats_dict.get("Approved", 0),
            "completed": stats_dict.get("Completed", 0),
            "cancelled": stats_dict.get("Cancelled", 0)
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch stats"}), 500
