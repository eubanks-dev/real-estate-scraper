# scraper.py

from flask import Flask

app = Flask(__name__)

@app.route("/scraped-data")
def index():
	return "Show scraped data here"
