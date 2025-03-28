import requests
from bs4 import BeautifulSoup,Comment
from urllib.parse import urljoin, urlparse
import re

class WebCrawler:
    def __init__(self, base_url, max_depth=2):
        self.base_url = base_url
        self.max_depth = max_depth
        self.visited_urls = set()
        self.comentarios = []
        self.emails = set()

    def crawl(self, url, depth=0):
        if depth > self.max_depth or url in self.visited_urls:
            return
    

        print(f"[{depth}] Crawling: {url}")
        self.visited_urls.add(url)

        try:
            response = requests.get(url, timeout=5)
            if response.status_code != 200:
                return

            soup = BeautifulSoup(response.text, "html.parser")
            comentarios = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comentario in comentarios:
                self.comentarios.append(comentario.strip())
            self.get_emails(response.text)
            for link in soup.find_all("a", href=True):
                full_url = urljoin(url, link["href"])
                if self.is_valid_url(full_url):
                    self.crawl(full_url, depth + 1)

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def is_valid_url(self, url):
        parsed = urlparse(url)
        return parsed.netloc == urlparse(self.base_url).netloc and url not in self.visited_urls
    def get_emails(self, text):
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
        emails = re.findall(email_pattern, text)
        self.emails.update(emails)
    def imprime_resultados(self):
        print("\n=== Comentarios encontrados ===")
        for comentario in self.comentarios:
            print(comentario)
        print("\n=== Correos electrónicos encontrados ===")
        for email in self.emails:
            print(email)

# Ejemplo de uso
if __name__ == "__main__":
    start_url = "http://127.0.0.1:8000/victima.html"  # Cambia esta URL por la que deseas rastrear
    crawler = WebCrawler(start_url, max_depth=2)
    crawler.crawl(start_url)
    crawler.imprime_resultados()
