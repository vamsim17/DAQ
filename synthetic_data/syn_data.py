import json
import random
import csv
import os
from datetime import datetime, timedelta

#def iso_timestamp():
#    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_sensor_specs(csv_path = "docs/sensor_specs.csv"):
    specs = {}
    with open (csv_path, newline = '') as f:
        for row in csv.DictReader(f):
            dtype = row["data_type"].strip()
            low = int(row["min_range"]) if dtype == "integer" else float(row["min_range"])
            high = int(row["max_range"]) if dtype == "integer" else float(row["max_range"])
            specs[row["sensor_name"].strip()] = (low, high, dtype)
    return specs
    
def random_sensor_val(sensor_name, specs):
    low, high, dtype = specs[sensor_name]
    if dtype == "integer":
        return random.randint(int(low), int(high))
    else:
        return round(random.uniform(low, high), 2)

def build_sensors_section(specs):
    speed_keys = [k for k in specs if k.startswith("speed_")]
    min_speed = min(specs[k][0] for k in speed_keys)
    max_speed = max(specs[k][0] for k in speed_keys)
    base_speed = round(random.uniform(min_speed, max_speed), 2)

    sensors = {}
    for name in specs:
        if name.startswith("speed_"):
            low, high, _ = specs[name]
            val = round(max(low, min(high, base_speed + random.uniform(-0.3, 0.3))), 2)
            sensors[name] = random_sensor_val(name, specs)
    return sensors

def generate_packed_id(ts_ms):
    return f"pkt_{ts_ms}"

def generate_session_id(dt):
    session_start = dt.replace(second = 0, microsecond = 0)
    return f"auto_{session_start.strftime('%Y%m%d_%H%M%S')}"

def build_record(dt, vehicle_id, specs, session_id = None):
    ts_ms = int(dt.timestamp() * 1000)
    record = {
        "timestamp": dt.strftime("%Y-%m-%dT%H:%M:%S.") + f"{dt.microsecond // 1000:03d}Z",
        "session_id": session_id if session_id else generate_session_id(dt),
        "vehicle_id": vehicle_id,
        "sensors": build_sensors_section(specs),
        "telemetry_metadata": {
            "packet_id": generate_packed_id(ts_ms),
            "sample_rate_hz": 100
        }
    }
    return record

def generate(
        count = 10,
        output_dir = ".",
        vehicle_id = "FSAE_2022_001",
        session_id = None,
        start_dt = None,
        interval_ms = 10,
        specs_path = "docs/sensor_specs.csv"
):
    os.makedirs(output_dir, exist_ok = True)
    specs = load_sensor_specs(specs_path)

    if start_dt is None:
        start_dt = datetime.now()
    written = []
    for i in range(count):
        dt = start_dt + timedelta(milliseconds=i * interval_ms)
        record = build_record(dt, vehicle_id, specs, session_id)

        filename = dt.strftime("%Y%m%d_%H%M%S") + f"_{dt.microsecond // 1000:03d}.json"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, "w") as f:
            json.dump(record, f, indent=2)
        written.append(filepath)
    print(f"Generated {count} records {output_dir}/")
    return written

if __name__ == "__main__":
    generate(
        count = 10,
        output_dir="synthetic_out",
        vehicle_id = "FSAE_2022_001",
        specs_path = "docs/sensor_specs.csv"
    )

