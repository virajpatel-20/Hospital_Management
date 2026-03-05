from flask import Blueprint, request, jsonify
from database import mongo
from bson.objectid import ObjectId
from datetime import datetime

doctor = Blueprint("doctor", __name__)

# VIEW DOCTOR APPOINTMENTS
@doctor.route("/doctor/appointments/<email>", methods=["GET"])
def doctor_view(email):
    try:
        status_filter = request.args.get("status", "")
        search = request.args.get("search", "").strip()
        date_filter = request.args.get("date", "")

        query = {"doctor_email": email.lower()}
        if status_filter:
            query["status"] = status_filter
        if date_filter:
            query["date"] = date_filter
        if search:
            query["$or"] = [
                {"patient_name": {"$regex": search, "$options": "i"}},
                {"reason": {"$regex": search, "$options": "i"}}
            ]

        data = list(mongo.db.appointments.find(query).sort("date", -1))
        for d in data:
            d["_id"] = str(d["_id"])

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch appointments"}), 500


# APPROVE APPOINTMENT
@doctor.route("/doctor/approve/<id>", methods=["PUT"])
def approve(id):
    try:
        appt = mongo.db.appointments.find_one({"_id": ObjectId(id)})
        if not appt:
            return jsonify({"error": "Appointment not found"}), 404

        if appt["status"] != "Pending":
            return jsonify({"error": "Only pending appointments can be approved"}), 400

        mongo.db.appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "Approved", "updated_at": datetime.utcnow().isoformat()}}
        )
        return jsonify({"message": "Appointment approved successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to approve appointment"}), 500


# COMPLETE APPOINTMENT
@doctor.route("/doctor/complete/<id>", methods=["PUT"])
def complete(id):
    try:
        data = request.get_json() or {}
        appt = mongo.db.appointments.find_one({"_id": ObjectId(id)})
        if not appt:
            return jsonify({"error": "Appointment not found"}), 404

        mongo.db.appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "status": "Completed",
                "doctor_notes": data.get("notes", ""),
                "updated_at": datetime.utcnow().isoformat()
            }}
        )
        return jsonify({"message": "Appointment marked as completed"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to complete appointment"}), 500


# CANCEL APPOINTMENT (doctor)
@doctor.route("/doctor/cancel/<id>", methods=["PUT"])
def cancel(id):
    try:
        appt = mongo.db.appointments.find_one({"_id": ObjectId(id)})
        if not appt:
            return jsonify({"error": "Appointment not found"}), 404

        mongo.db.appointments.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"status": "Cancelled", "updated_at": datetime.utcnow().isoformat()}}
        )
        return jsonify({"message": "Appointment cancelled"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to cancel appointment"}), 500


# DOCTOR STATS
@doctor.route("/doctor/stats/<email>", methods=["GET"])
def doctor_stats(email):
    try:
        pipeline = [
            {"$match": {"doctor_email": email.lower()}},
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
