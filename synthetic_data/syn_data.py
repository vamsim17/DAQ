import json
import random
import csv
from datetime import datetime, timezone

def iso_timestamp():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_sensor_specs():
    specs = {}
    with open ("docs/sensor_specs.csv", newline = '') as f:
        reader = csv.DictReader
        for row in reader:
            specs[row["sensor_name"]] = {
                "type": row["data_type"],
                "min": float(row["min_range"]),
                "max": float(row["max_range"])
            }
    return specs
    
def generate_sensors(specs):
    sensors = {}
    for sensor, spec in specs.items():
        value = random.uniform(spec["min"], spec["max"])
        if spec["value"] == "int":
            value = int(value)
        else:
            value = round(value, 2)
    return sensors

def generate_payload(specs):
    payload = {
        "timestamp": iso_timestamp(),
        "session_id": "auto_" + datetime.now().strftime("%Y%m%d_%H%M%S"),
        "vehicle_id": "FSAE_2022_001",
        "sensors": generate_sensors(specs),
        "telemetry_metadata": {
            "packet_id": f"pkt_{int(datetime.now().timestamp()*1000)}",
            "sample_rate_hz": 100,
            "daq_version": "v2.2.1"
        }
    }
    return payload
    
