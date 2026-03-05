from flask import Blueprint, request, jsonify
from database import mongo
from bson.objectid import ObjectId
from datetime import datetime

admin = Blueprint("admin", __name__)

# GET ALL APPOINTMENTS (with search/filter)
@admin.route("/admin/appointments", methods=["GET"])
def all_appointments():
    try:
        status_filter = request.args.get("status", "")
        search = request.args.get("search", "").strip()
        date_filter = request.args.get("date", "")

        query = {}
        if status_filter:
            query["status"] = status_filter
        if date_filter:
            query["date"] = date_filter
        if search:
            query["$or"] = [
                {"patient_name": {"$regex": search, "$options": "i"}},
                {"doctor_name": {"$regex": search, "$options": "i"}},
                {"patient_email": {"$regex": search, "$options": "i"}}
            ]

        data = list(mongo.db.appointments.find(query).sort("date", -1))
        for d in data:
            d["_id"] = str(d["_id"])

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch appointments"}), 500


# GET ALL USERS
@admin.route("/admin/users", methods=["GET"])
def all_users():
    try:
        role_filter = request.args.get("role", "")
        search = request.args.get("search", "").strip()

        query = {}
        if role_filter:
            query["role"] = role_filter
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}}
            ]

        users = list(mongo.db.users.find(query, {"password": 0}).sort("created_at", -1))
        for u in users:
            u["_id"] = str(u["_id"])

        return jsonify(users), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch users"}), 500


# ADMIN DASHBOARD STATS
@admin.route("/admin/stats", methods=["GET"])
def admin_stats():
    try:
        total_patients = mongo.db.users.count_documents({"role": "patient"})
        total_doctors = mongo.db.users.count_documents({"role": "doctor"})
        total_appointments = mongo.db.appointments.count_documents({})
        pending = mongo.db.appointments.count_documents({"status": "Pending"})
        approved = mongo.db.appointments.count_documents({"status": "Approved"})
        completed = mongo.db.appointments.count_documents({"status": "Completed"})
        cancelled = mongo.db.appointments.count_documents({"status": "Cancelled"})

        return jsonify({
            "total_patients": total_patients,
            "total_doctors": total_doctors,
            "total_appointments": total_appointments,
            "pending": pending,
            "approved": approved,
            "completed": completed,
            "cancelled": cancelled
        }), 200

    except Exception as e:
        return jsonify({"error": "Failed to fetch stats"}), 500


# DELETE USER
@admin.route("/admin/user/<id>", methods=["DELETE"])
def delete_user(id):
    try:
        result = mongo.db.users.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": "Failed to delete user"}), 500


# TOGGLE USER STATUS
@admin.route("/admin/user/toggle/<id>", methods=["PUT"])
def toggle_user(id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        new_status = not user.get("is_active", True)
        mongo.db.users.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"is_active": new_status}}
        )
        status_str = "activated" if new_status else "deactivated"
        return jsonify({"message": f"User {status_str} successfully"}), 200

    except Exception as e:
        return jsonify({"error": "Failed to update user status"}), 500
