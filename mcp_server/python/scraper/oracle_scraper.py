"""
Nexus Corporate OS - Oracle Data Scraper
Version: 1.0.0
Description: Automated intelligence gathering service for market and competitor data.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from pathlib import Path

_base_dir = Path(__file__).resolve().parent.parent.parent
_storage_path = _base_dir / "archives" / "core" / "monitoring" / "scraped_data.json"

class OracleScraper:
    def __init__(self, storage_path=None):
        self.storage_path = Path(storage_path) if storage_path else _storage_path

    def scrape_tech_news(self):
        """Pre-defined scraping target for Market Intelligence."""
        url = "https://news.google.com/topstories?hl=en-US&gl=US&ceid=US:en"
        print(f"Oracle Scraper: Fetching latest signals from {url}...")
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            articles = soup.find_all('a', class_='WwrYfe', limit=5)
            if not articles:
                articles = soup.find_all(['h3', 'h4'], limit=5)

            extracted = []
            for article in articles:
                title = article.get_text().strip()
                if len(title) > 10:
                    extracted.append({
                        "source": "Global Intelligence",
                        "timestamp": datetime.now().isoformat(),
                        "title": title,
                        "url": url,
                        "status": "VERIFIED"
                    })

            if not extracted:
                extracted.append({
                    "source": "Oracle Internal",
                    "timestamp": datetime.now().isoformat(),
                    "title": "System Check: No external signals detected in current cycle.",
                    "url": "#",
                    "status": "INTERNAL"
                })

            for item in extracted:
                self._save_data(item)

            print(f"Oracle Scraper: Successfully saved {len(extracted)} signals.")
            return extracted
        except Exception as e:
            error_data = {"source": "System Error", "timestamp": datetime.now().isoformat(), "title": f"Scraper Failure: {str(e)}", "status": "FAILED"}
            self._save_data(error_data)
            return [error_data]

    def _save_data(self, data):
        """Appends intelligence to the local storage."""
        existing_data = []
        if self.storage_path.exists():
            with open(self.storage_path, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except:
                    existing_data = []

        existing_data.append(data)
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    scraper = OracleScraper()
    scraper.scrape_tech_news()
