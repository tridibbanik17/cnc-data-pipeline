import time
import random
import requests
import yaml
from datetime import datetime

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def generate_payload(machine_id):
    spindle_load = round(random.uniform(10, 95), 2)
    tool_wear = round(random.uniform(0, 1), 3)

    uptime = random.choice([True, True, True, False])
    alarm_active = random.choice([False, False, False, True])

    cycle_time = round(random.uniform(20, 180), 2)

    alarm_code = None
    if alarm_active:
        alarm_code = random.choice(["E_STOP", "TOOL_BREAK", "OVERHEAT", "LOW_LUBE"])

    return {
        "machine_id": machine_id,
        "timestamp": datetime.utcnow().isoformat(),
        "spindle_load": spindle_load,
        "tool_wear": tool_wear,
        "cycle_time": cycle_time,
        "uptime": uptime,
        "alarm_active": alarm_active,
        "alarm_code": alarm_code
    }

def main():
    config = load_config()
    url = config["backend_url"]
    machines = config["machine_ids"]
    interval = config["interval_seconds"]

    print("Starting CNC simulator...")
    print("Sending telemetry to:", url)

    while True:
        for m in machines:
            payload = generate_payload(m)

            try:
                r = requests.post(url, json=payload, timeout=2)
                print(f"[{m}] Sent telemetry -> status {r.status_code}")
            except Exception as e:
                print("Error sending telemetry:", e)

        time.sleep(interval)

if __name__ == "__main__":
    main()