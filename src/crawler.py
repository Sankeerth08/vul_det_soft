# src/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

class Crawler:
    def __init__(self, base_url, max_depth=2, delay=1, retries=3, auth=None):
        self.base_url = base_url
        self.max_depth = max_depth
        self.delay = delay  # Seconds between requests
        self.retries = retries  # Retry failed requests
        self.auth = auth  # Tuple (username, password)
        self.visited = {}  # Track URLs and their depth: {url: depth}
        self.links = set()
        self.forms = []

    def start(self):
        self.crawl(self.base_url, depth=0)

    def crawl(self, url, depth):
        if url in self.visited or depth > self.max_depth:
            return
        self.visited[url] = depth
        
        # Retry failed requests
        for _ in range(self.retries):
            try:
                time.sleep(self.delay)  # Rate limiting
                response = requests.get(url, auth=self.auth)
                soup = BeautifulSoup(response.text, 'html.parser')
                self.extract_links(soup, url, depth)
                self.extract_forms(soup, url)
                break  # Exit retry loop on success
            except Exception as e:
                print(f"[!] Error crawling {url} (attempt {_+1}/{self.retries}): {e}")

    def extract_links(self, soup, current_url, depth):
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            if self.base_url in full_url and full_url not in self.visited:
                self.links.add(full_url)
                self.crawl(full_url, depth + 1)  # Increase depth

    def extract_forms(self, soup, current_url):
        for form in soup.find_all('form'):
            action = urljoin(current_url, form.get('action', ''))
            method = form.get('method', 'get').lower()
            
            # Skip duplicate forms
            if any(f['action'] == action for f in self.forms):
                continue
            
            inputs = []
            for input_tag in form.find_all('input'):
                name = input_tag.get('name')
                if not name:  # Skip unnamed inputs
                    continue
                inputs.append({
                    'name': name,
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', '')
                })
            
            self.forms.append({
                'action': action,
                'method': method,
                'inputs': inputs
            })

    def get_results(self):
        return {
            'links': list(self.links),
            'forms': self.forms
        }