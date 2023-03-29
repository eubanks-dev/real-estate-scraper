# scraper.py

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import sys
import json

app = Flask(__name__)

@app.route("/scraped-data")
def index():
	relevant_data = parse_realpage()	
	# print(relevant_data, file=sys.stderr)

	'''
	This template creates an HTML table with two columns: "Property Name" and "Unit Count". 
	It iterates over the dictionary passed in as "table_data", and generates a new row in the table for each property.
	'''
	return render_template('properties_table_template.html', table_data=relevant_data)

def parse_realpage():
	"""Parse Realpage data and store relevant fields in a dictionary

	Returns:
		dictionary: dictionary containing relevant fields from Realpage property data
	"""
	realpage_data = hardcoded_realpage_data()
	property_dict = {}

	# for each property in the realpage data
	for property in realpage_data:

		# get property name and unit count from JSON data
		property_name = property['propertyName']
		unit_count = property['unitcount']

		# Add property name and unit count to dictionary
		property_dict[property_name] = unit_count

	return property_dict


def hardcoded_realpage_data():
	"""Returns a locally stored copy of the JSON data returned by realpage at the following URL: https://dac.realpage.com/dac/markets/16980/properties

	Returns:
		string: Hardcoded realpage JSON data
	"""

	with open('realpage_data.json', 'r') as f:
		data = json.load(f)

	return data

def scrape_zillow():
	""" [NOT WORKING] Experiment - Use BeautifulSoup to parse scraped data from Zillow
	"""

	url = "https://www.zillow.com/seattle-wa/rentals/"

	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	listings = soup.find_all("div", class_="list-card-info")
	print("listings: ", listings.count, file=sys.stderr)

	for listing in listings:

		address = listing.find("address", file=sys.stderr)
		if address:
			print(address.text.strip(), file=sys.stderr)
		price = listing.find("div", class_="list-card-price")
		if price:
			print(price.text.strip(), file=sys.stderr)
		details = listing.find("ul", class_="list-card-details")
		if details:
			bedrooms = details.find("li")
			if bedrooms:
				print(bedrooms.text.strip(), file=sys.stderr)
			sqft = details.find("li", {"data-testid": "sqft"})
			if sqft:
				print(sqft.text.strip(), file=sys.stderr)
		print("--------------------", file=sys.stderr)