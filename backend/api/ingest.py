from flask import Blueprint, request, jsonify
from db.connection import get_connection
from services.data_cleaning import clean_payload
from services.anomaly_detection import detector
from services.downtime_state_machine import update_downtime_state

ingest_bp = Blueprint("ingest", __name__)

@ingest_bp.route("/ingest", methods=["POST"])
def ingest():
    payload = request.get_json()

    try:
        payload = clean_payload(payload)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO machine_data(machine_id, timestamp, spindle_load, tool_wear, cycle_time, uptime, alarm_active, alarm_code)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        payload["machine_id"],
        payload["timestamp"],
        payload["spindle_load"],
        payload["tool_wear"],
        payload["cycle_time"],
        payload["uptime"],
        payload["alarm_active"],
        payload.get("alarm_code")
    ))

    conn.commit()

    cur.execute("""
        SELECT spindle_load, tool_wear, cycle_time
        FROM machine_data
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT 50
    """, (payload["machine_id"],))

    rows = cur.fetchall()
    if rows:
        detector.train(rows)

    is_anomaly, severity = detector.detect([
        payload["spindle_load"],
        payload["tool_wear"],
        payload["cycle_time"]
    ])

    if is_anomaly:
        cur.execute("""
            INSERT INTO anomaly_flags(machine_id, timestamp, anomaly_type, severity)
            VALUES (%s, %s, %s, %s)
        """, (
            payload["machine_id"],
            payload["timestamp"],
            "TELEMETRY_OUTLIER",
            severity
        ))
        conn.commit()

    update_downtime_state(
        payload["machine_id"],
        payload["timestamp"],
        payload["uptime"],
        payload.get("alarm_code")
    )

    cur.close()
    conn.close()

    return jsonify({"status": "ok", "anomaly": is_anomaly})