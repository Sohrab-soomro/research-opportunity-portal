"""
REST API routes for research opportunities.

POST   /api/opportunities        -> create
GET    /api/opportunities        -> get all
GET    /api/opportunities/<id>   -> get one
PUT    /api/opportunities/<id>   -> update (also used to close: status = "Closed")
DELETE /api/opportunities/<id>   -> delete
"""
from datetime import datetime, date
import re

import mysql.connector
from flask import Blueprint, jsonify, request

from db import get_connection

opportunities_bp = Blueprint("opportunities", __name__)

TEXT_FIELDS = [
    "research_title",
    "research_description",
    "research_area",
    "faculty_name",
    "department",
    "required_skills",
]
ALL_FIELDS = TEXT_FIELDS + ["available_positions", "application_deadline", "status"]
TEXT_LIMITS = {"research_title": 200, "research_area": 100, "faculty_name": 100,
               "department": 100, "required_skills": 255}
VALID_STATUSES = ["Open", "Closed"]


# ---------------------------------------------------------------- helpers

def to_json(row):
    """Convert a database row (dict) into JSON-friendly values."""
    if row and isinstance(row.get("application_deadline"), date):
        row["application_deadline"] = row["application_deadline"].isoformat()
    return row


def validate(data):
    """
    Check one opportunity's data.
    Returns (clean_data, errors). If errors is empty, the data is valid.
    """
    errors = []
    clean = {}

    # Text fields must be non-empty strings
    for field in TEXT_FIELDS:
        value = data.get(field)
        if not isinstance(value, str) or value.strip() == "":
            errors.append(f"{field} is required")
        else:
            clean[field] = value.strip()
            if len(clean[field]) > TEXT_LIMITS.get(field, 65535) or (field == "research_description" and len(clean[field].encode("utf-8")) > 65535):
                errors.append(f"{field} exceeds its database length limit")

    # Available positions must be a positive whole number
    positions = data.get("available_positions")
    try:
        if isinstance(positions, bool):
            raise ValueError
        positions = int(str(positions))
        if positions <= 0 or positions > 2147483647:
            raise ValueError
        clean["available_positions"] = positions
    except (ValueError, TypeError):
        errors.append("available_positions must be a positive whole number")

    # Deadline must be a real date in YYYY-MM-DD format
    deadline = data.get("application_deadline")
    try:
        if not isinstance(deadline, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", deadline):
            raise ValueError
        clean["application_deadline"] = datetime.strptime(str(deadline), "%Y-%m-%d").date()
        if clean["application_deadline"].year < 1000:
            raise ValueError
    except (ValueError, TypeError):
        errors.append("application_deadline must be a valid date (YYYY-MM-DD)")

    # Status must be Open or Closed (defaults to Open when creating)
    status = data.get("status", "Open")
    if status not in VALID_STATUSES:
        errors.append("status must be either 'Open' or 'Closed'")
    else:
        clean["status"] = status

    return clean, errors


def find_by_id(cursor, opp_id):
    cursor.execute("SELECT * FROM opportunities WHERE id = %s", (opp_id,))
    return cursor.fetchone()


def db_error_response(error):
    """Log the real database error on the server, return a clean message."""
    # Connector messages may contain usernames, hosts or other private details.
    print("Database operation failed:", type(error).__name__)
    return jsonify({"error": "A database error occurred. Please try again later."}), 500


# ---------------------------------------------------------------- CREATE

@opportunities_bp.route("/api/opportunities", methods=["POST"])
def create_opportunity():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be valid JSON"}), 400

    clean, errors = validate(data)
    if errors:
        return jsonify({"error": "Invalid input", "details": errors}), 400

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """INSERT INTO opportunities
               (research_title, research_description, research_area, faculty_name,
                department, required_skills, available_positions,
                application_deadline, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            tuple(clean[f] for f in ALL_FIELDS),
        )
        conn.commit()
        new_row = find_by_id(cursor, cursor.lastrowid)
        return jsonify({
            "message": "Research opportunity created successfully",
            "data": to_json(new_row),
        }), 201
    except mysql.connector.Error as e:
        return db_error_response(e)
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------- GET ALL

@opportunities_bp.route("/api/opportunities", methods=["GET"])
def get_all_opportunities():
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM opportunities ORDER BY id DESC")
        rows = [to_json(r) for r in cursor.fetchall()]
        return jsonify({"message": "Research opportunities retrieved successfully",
                        "count": len(rows), "data": rows}), 200
    except mysql.connector.Error as e:
        return db_error_response(e)
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------- GET ONE

@opportunities_bp.route("/api/opportunities/<int:opp_id>", methods=["GET"])
def get_opportunity(opp_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        row = find_by_id(cursor, opp_id)
        if row is None:
            return jsonify({"error": "Research opportunity not found"}), 404
        return jsonify({"message": "Research opportunity retrieved successfully",
                        "data": to_json(row)}), 200
    except mysql.connector.Error as e:
        return db_error_response(e)
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------- UPDATE

@opportunities_bp.route("/api/opportunities/<int:opp_id>", methods=["PUT"])
def update_opportunity(opp_id):
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or len(data) == 0:
        return jsonify({"error": "Request body must be valid JSON with fields to update"}), 400
    if not any(field in data for field in ALL_FIELDS):
        return jsonify({"error": "No recognized fields to update"}), 400

    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        existing = find_by_id(cursor, opp_id)
        if existing is None:
            return jsonify({"error": "Research opportunity not found"}), 404

        # Start from the existing record and apply only the sent fields,
        # so a request like {"status": "Closed"} works on its own.
        merged = to_json(dict(existing))
        for field in ALL_FIELDS:
            if field in data:
                merged[field] = data[field]

        clean, errors = validate(merged)
        if errors:
            return jsonify({"error": "Invalid input", "details": errors}), 400

        cursor.execute(
            """UPDATE opportunities SET
                 research_title = %s, research_description = %s, research_area = %s,
                 faculty_name = %s, department = %s, required_skills = %s,
                 available_positions = %s, application_deadline = %s, status = %s
               WHERE id = %s""",
            tuple(clean[f] for f in ALL_FIELDS) + (opp_id,),
        )
        conn.commit()
        updated = find_by_id(cursor, opp_id)
        return jsonify({"message": "Research opportunity updated successfully",
                        "data": to_json(updated)}), 200
    except mysql.connector.Error as e:
        return db_error_response(e)
    finally:
        if conn:
            conn.close()


# ---------------------------------------------------------------- DELETE

@opportunities_bp.route("/api/opportunities/<int:opp_id>", methods=["DELETE"])
def delete_opportunity(opp_id):
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        if find_by_id(cursor, opp_id) is None:
            return jsonify({"error": "Research opportunity not found"}), 404

        cursor.execute("DELETE FROM opportunities WHERE id = %s", (opp_id,))
        conn.commit()
        return jsonify({"message": "Research opportunity deleted successfully",
                        "data": {"id": opp_id}}), 200
    except mysql.connector.Error as e:
        return db_error_response(e)
    finally:
        if conn:
            conn.close()
