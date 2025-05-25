from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def clean_phone_numbers(phone_list):
    cleaned = []
    for phone in phone_list:
        # Remove spaces, dots etc.
        num = re.sub(r"[^\d+]", "", phone)
        if 7 <= len(num) <= 15:
            cleaned.append(num)
    return list(set(cleaned))

def scrape_website(url):
    driver = setup_driver()
    visited = set()
    emails = set()
    phones = set()

    domain = urlparse(url).netloc

    try:
        queue = [url]

        while queue:
            current_url = queue.pop(0)
            if current_url in visited:
                continue

            visited.add(current_url)

            try:
                driver.get(current_url)
                time.sleep(2)  # Wait for JS to load
                page = driver.page_source
                soup = BeautifulSoup(page, 'html.parser')

                # Scrape emails and phones
                text = soup.get_text()

                found_emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
                found_phones = re.findall(r"(\+?\d[\d\s\-\(\)]{7,}\d)", text)

                emails.update(found_emails)
                phones.update(found_phones)

                # Find internal links to crawl
                links = [a.get('href') for a in soup.find_all('a', href=True)]
                for link in links:
                    full_link = urljoin(current_url, link)
                    if urlparse(full_link).netloc == domain and full_link not in visited:
                        queue.append(full_link)

            except Exception as e:
                print(f"Failed to scrape {current_url}: {e}")

    finally:
        driver.quit()

    return {
        "emails": list(emails),
        "phones": clean_phone_numbers(phones)
    }

@app.route('/scrape_email', methods=['POST'])
def scrape():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL is required"}), 400

    result = scrape_website(url)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
