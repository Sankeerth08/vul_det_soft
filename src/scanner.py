# src/scanner.py
import argparse
from crawler import Crawler
from sqli_detector import SQLiDetector
from utils.report_generator import save_json

def parse_args():
    parser = argparse.ArgumentParser(description="OWASP Top 10 Vulnerability Scanner")
    parser.add_argument("--url", help="Target URL", required=True)
    parser.add_argument("--output", help="Save results to file (JSON)", default=None)
    parser.add_argument("--depth", type=int, default=2, help="Crawling depth (default: 2)")
    parser.add_argument("--timeout", type=int, default=10, help="Request timeout in seconds (default: 10)")
    parser.add_argument("--auth-user", help="Username for authentication", default=None)
    parser.add_argument("--auth-pass", help="Password for authentication", default=None)
    parser.add_argument("--delay", type=int, default=1, help="Delay between requests in seconds (default: 1)")
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"[*] Scanning: {args.url}")
    
    # Configure authentication
    auth = (args.auth_user, args.auth_pass) if args.auth_user and args.auth_pass else None
    
    # Step 1: Crawl the website
    crawler = Crawler(
        base_url=args.url,
        max_depth=args.depth,
        delay=args.delay,
        auth=auth
    )
    crawler.start()
    results = crawler.get_results()
    print(f"[+] Found {len(results['links'])} links and {len(results['forms'])} forms.")
    
    # Step 2: Detect SQLi vulnerabilities
    sqli_detector = SQLiDetector(
        target_url=args.url,
        timeout=args.timeout,
        auth=auth
    )
    vulnerabilities = []
    for form in results['forms']:
        vulns = sqli_detector.test_form(form)
        vulnerabilities.extend(vulns)
    print(f"[+] Found {len(vulnerabilities)} SQLi vulnerabilities.")
    
    # Step 3: Save results
    if args.output:
        save_json(vulnerabilities, args.output)
        print(f"[+] Report saved to {args.output}")

if __name__ == "__main__":
    main()