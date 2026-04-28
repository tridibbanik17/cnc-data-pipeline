from flask import Blueprint, jsonify, request
from db.connection import get_connection
from services.jwt_guard import require_auth

history_bp = Blueprint("history", __name__)

@history_bp.route("/machines/<machine_id>/history", methods=["GET"])
@require_auth
def machine_history(machine_id):
    limit = request.args.get("limit", default=200, type=int)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, spindle_load, tool_wear, cycle_time, uptime, alarm_active
        FROM machine_data
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT %s
    """, (machine_id, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in reversed(rows):  # chronological order
        result.append({
            "timestamp": r[0].isoformat(),
            "spindle_load": float(r[1]),
            "tool_wear": float(r[2]),
            "cycle_time": float(r[3]),
            "uptime": bool(r[4]),
            "alarm_active": bool(r[5]),
        })

    return jsonify({
        "machine_id": machine_id,
        "points": result
    })