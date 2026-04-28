def calculate_oee(runtime_minutes, planned_minutes, good_parts, total_parts):
    if planned_minutes == 0:
        return 0

    availability = runtime_minutes / planned_minutes

    performance = 1.0
    if total_parts > 0:
        performance = total_parts / (planned_minutes / 1.0)

    quality = 1.0
    if total_parts > 0:
        quality = good_parts / total_parts

    return round(availability * performance * quality, 4)