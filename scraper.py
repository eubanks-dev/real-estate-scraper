# scraper.py

from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import sys
import json

app = Flask(__name__)

@app.route("/parsed-realpage-data")
def index():
	"""This route displays scraped/parsed data from real estate data sources

	Returns:
		Jinja2 Template: A rendered HTML page dispalying a table of real estate property data
	"""
	relevant_data = parse_realpage()	

	'''
	This template creates an HTML page with a table of property data. 
	It iterates over the list of dictionaries passed in as "table_data", and 
	generates a new row in the table for each property in the list.
	'''
	return render_template('properties_table_template.html', table_data=relevant_data)

def parse_realpage():
	"""Parse Realpage data and store relevant fields in a dictionary

	Returns:
		dictionary: dictionary containing relevant fields from Realpage property data
	"""
	realpage_data = locally_stored_realpage_data()
	property_list = []

	# for each property in the realpage data
	for property in realpage_data:
		# parse relevant property data and store in dictionary
		property_dict = {}
		property_dict["name"] = property['propertyName']
		property_dict["city"] = property['city']
		property_dict["state"] = property['state']
		property_dict["unitcount"] = property['unitcount']

		for metric_data in property['metricData']:
			if metric_data['metricCode'] == 'MPF-OCC':
				property_dict["occupancy"] = metric_data['metricValueFormatted']

		# Add dictionary to list of properties
		property_list.append(property_dict)

	return property_list


def locally_stored_realpage_data():
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