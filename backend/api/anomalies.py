from flask import Blueprint, jsonify
from db.connection import get_connection
from services.jwt_guard import require_auth


anomalies_bp = Blueprint("anomalies", __name__)

@anomalies_bp.route("/anomalies", methods=["GET"])
@require_auth
def anomalies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT machine_id, timestamp, anomaly_type, severity
        FROM (
            SELECT machine_id, timestamp, anomaly_type, severity
            FROM anomaly_flags
            ORDER BY timestamp DESC
            LIMIT 100
        ) t
        ORDER BY timestamp ASC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    result = []
    for r in rows:
        result.append({
            "machine_id": r[0],
            "timestamp": r[1].isoformat(),
            "anomaly_type": r[2],
            "severity": float(r[3])
        })

    return jsonify(result)