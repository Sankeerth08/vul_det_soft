# src/crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class Crawler:
    def __init__(self, base_url):
        self.base_url = base_url
        self.visited = set()
        self.links = set()
        self.forms = []

    def start(self):
        self.crawl(self.base_url)

    def crawl(self, url):
        if url in self.visited:
            return
        self.visited.add(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.extract_links(soup, url)
            self.extract_forms(soup, url)
        except Exception as e:
            print(f"[!] Error crawling {url}: {e}")

    def extract_links(self, soup, current_url):
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(current_url, href)
            if self.base_url in full_url and full_url not in self.visited:
                self.links.add(full_url)
                self.crawl(full_url)  # Recursive crawling

    def extract_forms(self, soup, current_url):
        for form in soup.find_all('form'):
            form_details = {
                'action': urljoin(current_url, form.get('action', '')),
                'method': form.get('method', 'get').lower(),
                'inputs': []
            }
            for input_tag in form.find_all('input'):
                input_details = {
                    'name': input_tag.get('name'),
                    'type': input_tag.get('type', 'text'),
                    'value': input_tag.get('value', '')
                }
                form_details['inputs'].append(input_details)
            self.forms.append(form_details)

    def get_results(self):
        return {
            'links': list(self.links),
            'forms': self.forms
        }