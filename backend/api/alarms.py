from flask import Blueprint, jsonify
from db.connection import get_connection

alarms_bp = Blueprint("alarms", __name__)

@alarms_bp.route("/alarms", methods=["GET"])
def alarms():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT machine_id, timestamp, alarm_code
        FROM machine_data
        WHERE alarm_active = true
        ORDER BY timestamp DESC
        LIMIT 50
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()

    alarms = []
    for r in rows:
        alarms.append({
            "machine_id": r[0],
            "timestamp": r[1].isoformat(),
            "alarm_code": r[2]
        })

    return jsonify(alarms)