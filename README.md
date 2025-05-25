# 📬 Email & Phone Scraper API

A Flask-based microservice that scrapes **email addresses** and **phone numbers** from a given website URL. It uses **Selenium** to render JavaScript-based content, and **BeautifulSoup** for HTML parsing. The scraper crawls internal links within the same domain to gather contact data from multiple pages.

---

## 🌐 Features

- ✅ Extracts **email addresses** and **phone numbers** from websites
- ✅ Crawls internal links recursively (within same domain)
- ✅ Headless Chrome support using Selenium
- ✅ Cleans and deduplicates phone numbers
- ✅ Simple, well-documented JSON API
- ✅ Docker compatible for easy deployment

---

## 🔧 Tech Stack

- **Python 3.7+**
- **Flask** – RESTful API backend
- **Selenium + Headless Chrome** – Dynamic web page rendering
- **BeautifulSoup** – HTML parsing
- **Regex** – Pattern matching for emails and phone numbers

---

## 📁 Project Structure


---

## 📦 Setup & Installation
.
├── app.py # Main Flask app
├── requirements.txt # Python dependencies
└── README.md # Project documentation

### 1. Clone the repository

```bash
git clone https://github.com/saileshwankar/Email-Extractor-WebScraper.git
cd email-phone-scraper-api

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


🚀 Running the App
bash
python app.py

By default, the API will be available at:
http://127.0.0.1:5000/scrape_email
