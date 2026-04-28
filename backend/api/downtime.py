from flask import Blueprint, jsonify
from db.connection import get_connection
from services.jwt_guard import require_auth

downtime_bp = Blueprint("downtime", __name__)

@downtime_bp.route("/downtime", methods=["GET"])
@require_auth
def downtime():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT machine_id, start_time, end_time, reason
        FROM downtime_events
        ORDER BY start_time DESC
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "machine_id": r[0],
            "start_time": r[1].isoformat(),
            "end_time": r[2].isoformat() if r[2] else None,
            "reason": r[3]
        })

    return jsonify(result)