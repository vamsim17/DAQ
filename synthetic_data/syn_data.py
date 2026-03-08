import json
import random
import csv
from datetime import datetime, timezone

def load_sensor_specs():
    specs = {}
    with open ("docs/sensor_specs.csv") as f:
        reader = csv.DictReader
        for row in reader:
            dtype = row["data_type"].strip()
            min = int((row["min_range"]) if dtype == "integer" else float(row["min_range"]))
            max = int((row["max_range"]) if dtype == "integer" else float(row["max_range"]))
            specs[row["sensor_name"].strip()] = (min, max, dtype)
    return specs
