import json
import random
import csv
import os
from datetime import datetime, timedelta

#def iso_timestamp():
#    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

def load_sensor_specs(csv_path: str = "docs/sensor_specs.csv") -> dict:
    specs = {}
    with open (csv_path, newline = '') as f:
        for row in csv.DictReader(f):
            dtype = row["data_type"].strip()
            min = int(row["min_range"]) if dtype == "integer" else float(row["min_range"])
            max = int(row["max_range"]) if dtype == "integer" else float(row["max_range"])
            specs[row["sensor_name"].strip()] = (min, max, dtype)
    return specs
    
def random_sensor_val(sensor_name: str, specs: dict) -> float| int:
    min, max, dtype = specs[sensor_name]
    if dtype == "integer":
        return random.randint(int(min), int(max))
    else:
        return round(random.uniform(min, max), 2)


    
if __name__ == "__main__":
    specs = load_sensor_specs()
    payload = generate_payload(specs)
    print(json.dumps(payload, indent = 2))

