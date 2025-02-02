# utils/report_generator.py
import json
from datetime import datetime

def save_json(data, filename):
    report = {
        "timestamp": datetime.now().isoformat(),
        "vulnerabilities": data
    }
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)