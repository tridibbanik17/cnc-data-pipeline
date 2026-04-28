def clean_payload(payload):
    required_fields = [
        "machine_id", "timestamp", "spindle_load", "tool_wear",
        "cycle_time", "uptime", "alarm_active"
    ]

    for f in required_fields:
        if f not in payload:
            raise ValueError(f"Missing required field: {f}")

    if payload["spindle_load"] < 0 or payload["spindle_load"] > 150:
        raise ValueError("Spindle load out of expected range")

    if payload["tool_wear"] < 0 or payload["tool_wear"] > 1:
        raise ValueError("Tool wear out of expected range")

    if payload["cycle_time"] <= 0:
        raise ValueError("Invalid cycle time")

    return payload