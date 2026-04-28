import requests

BASE = "http://127.0.0.1:5000/api"

def test_latest_metrics():
    r = requests.get(f"{BASE}/metrics/latest")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_oee():
    r = requests.get(f"{BASE}/oee")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_alarms():
    r = requests.get(f"{BASE}/alarms")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

if __name__ == "__main__":
    test_latest_metrics()
    test_oee()
    test_alarms()
    print("All API tests passed.")