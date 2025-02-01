import json
from datetime import datetime

def save_json(results, filename):
    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"[+] Saved results to {filename}")