from db.connection import get_connection

def update_downtime_state(machine_id, timestamp, uptime, alarm_code=None):
    """
    If uptime becomes false => open downtime event
    If uptime becomes true => close downtime event
    """

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT uptime
        FROM machine_data
        WHERE machine_id = %s
        ORDER BY timestamp DESC
        LIMIT 1
    """, (machine_id,))

    last = cur.fetchone()
    last_uptime = last[0] if last else None

    if last_uptime is None:
        cur.close()
        conn.close()
        return

    if last_uptime is True and uptime is False:
        cur.execute("""
            INSERT INTO downtime_events(machine_id, start_time, reason)
            VALUES (%s, %s, %s)
        """, (machine_id, timestamp, alarm_code or "UNKNOWN"))

        conn.commit()

    if last_uptime is False and uptime is True:
        cur.execute("""
            UPDATE downtime_events
            SET end_time = %s
            WHERE machine_id = %s AND end_time IS NULL
        """, (timestamp, machine_id))

        conn.commit()

    cur.close()
    conn.close()