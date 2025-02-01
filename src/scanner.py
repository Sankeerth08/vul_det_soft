# src/scanner.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="OWASP Top 10 Vulnerability Scanner")
    parser.add_argument("--url", help="Target URL to scan", required=True)
    parser.add_argument("--auth-user", help="Username for authentication", default=None)
    parser.add_argument("--auth-pass", help="Password for authentication", default=None)
    args = parser.parse_args()

    print(f"[*] Scanning: {args.url}")
# scanner.py
from crawler import Crawler

def main():
    args = parse_args()  # Use argparse to get --url
    crawler = Crawler(args.url)
    crawler.start()
    results = crawler.get_results()
    print(f"[+] Found {len(results['links'])} links and {len(results['forms'])} forms.")

# scanner.py
from crawler import Crawler
from sqli_detector import SQLiDetector

def main():
    args = parse_args()
    crawler = Crawler(args.url)
    crawler.start()
    
    # Test for SQLi
    sqli_detector = SQLiDetector(args.url)
    vulnerabilities = []
    for form in crawler.forms:
        vulns = sqli_detector.test_form(form)
        vulnerabilities.extend(vulns)
    
    print(f"[+] Found {len(vulnerabilities)} SQLi vulnerabilities.")

# scanner.py
def parse_args():
    parser = argparse.ArgumentParser(description="OWASP Top 10 Vulnerability Scanner")
    parser.add_argument("--url", help="Target URL", required=True)
    parser.add_argument("--output", help="Save results to file (JSON/HTML)", default=None)
    parser.add_argument("--depth", help="Crawling depth (default: 2)", type=int, default=2)
    parser.add_argument("--timeout", help="Request timeout (seconds)", type=int, default=10)
    parser.add_argument("--verbose", help="Show detailed logs", action="store_true")
    return parser.parse_args()

if args.output:
    save_json(vulnerabilities, args.output)
    
if __name__ == "__main__":
    main()