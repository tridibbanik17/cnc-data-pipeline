from services.oee_calculator import calculate_oee

def test_calculate_oee():
    oee = calculate_oee(runtime_minutes=50, planned_minutes=100, good_parts=90, total_parts=100)
    assert oee > 0

if __name__ == "__main__":
    test_calculate_oee()
    print("OEE test passed.")