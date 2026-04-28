from flask import Blueprint, jsonify
from db.connection import get_connection
from services.jwt_guard import require_auth

oee_bp = Blueprint("oee", __name__)

@oee_bp.route("/oee", methods=["GET"])
@require_auth
def oee():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT machine_id,
               COUNT(*) FILTER (WHERE uptime = true) as uptime_count,
               COUNT(*) as total_count
        FROM machine_data
        GROUP BY machine_id
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        machine_id = r[0]
        uptime_count = r[1]
        total_count = r[2]

        availability = 0
        if total_count > 0:
            availability = uptime_count / total_count

        result.append({
            "machine_id": machine_id,
            "availability": round(availability, 3),
            "oee_estimate": round(availability * 0.9, 3)
        })

    return jsonify(result)