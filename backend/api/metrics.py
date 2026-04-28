from flask import Blueprint, jsonify
from db.connection import get_connection
from services.jwt_guard import require_auth

metrics_bp = Blueprint("metrics", __name__)

@metrics_bp.route("/metrics/latest", methods=["GET"])
@require_auth
def latest_metrics():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT ON (machine_id)
            machine_id, timestamp, spindle_load, tool_wear, cycle_time, uptime, alarm_active, alarm_code
        FROM machine_data
        ORDER BY machine_id, timestamp DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "machine_id": r[0],
            "timestamp": r[1].isoformat(),
            "spindle_load": r[2],
            "tool_wear": r[3],
            "cycle_time": r[4],
            "uptime": r[5],
            "alarm_active": r[6],
            "alarm_code": r[7]
        })

    return jsonify(result)