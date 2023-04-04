# scraper.py

from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import sys
import json

app = Flask(__name__)

@app.route("/parsed-realpage-data")
def parsed_realpage_data():
	"""This route displays the raw, unfiltered property data parsed from Realpage source

	Returns:
		Jinja2 Template: A rendered HTML page dispalying a table of real estate property data
	"""
	table_data = parse_realpage()	

	'''
	This template creates an HTML page with a table of property data. 
	It iterates over the list of dictionaries passed in as "table_data", and 
	generates a new row in the table for each property in the list.
	'''
	return render_template('realpage_properties_template.html', table_data=table_data)

@app.route("/realpage-data-with-filtering")
def realpage_data_with_filtering():
	"""This route is called by DataTables.js to retrieve Realpage data with sorting, searching, and pagination capabilities

	Returns:
		Response object: Fields needed by DataTables.js to render the table 
	"""
	filtered_property_list = parse_realpage()	
	
	# Check for search parameter and perform search filtering
	search_string = request.args.get('search[value]')
	if search_string:
		filtered_property_list = search_property_fields(filtered_property_list, search_string)

	# Check for order parameter and perform sorting
	order_column = request.args.get('order[0][column]', type=int)
	if order_column is not None:
		order_dir = request.args.get('order[0][dir]')
		filtered_property_list = sort_list_of_dictionaries(filtered_property_list, order_column, order_dir)
		
	'''
	This template creates an HTML page with a table of property data. 
	It iterates over the list of dictionaries passed in as "table_data", and 
	generates a new row in the table for each property in the list.
	'''
	return render_template('realpage_properties_template.html', table_data=filtered_property_list)

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


def search_property_fields(property_list, search_string):
    """
    Returns the subset of the properties whose name, city, or state contains the search string.

    :param property_list: a list of dictionaries representing real estate properties
    :param search_string: the search string to look for in the "name", "city", or "state" fields
    :return: the subset of the property_list that contains the search_string in the "name", "city",
             or "state" fields
    """
    return [d for d in property_list if search_string in d['name'] or
                                          search_string in d['city'] or
                                          search_string in d['state']]
def sort_list_of_dictionaries(dict_list, order_column, order_dir="asc"):
    """
    Sort a list of dictionaries based on the specified column and direction.

    Args:
        dict_list (list of dict): The data to be sorted.
        order_column (int): The index of the column to sort by.
        order_dir (str): The direction to sort in ("asc" or "desc").  Defaulted to "asc".

    Returns:
        list of dict: The sorted data.
    """
    
	# Check if the specified order column is out of range.
    if order_column < 0 or order_column >= len(dict_list[0]):
        raise ValueError("Order column index out of range")
    
    # Determine the key to sort by based on the specified column.
    key = list(dict_list[0].keys())[order_column]
    print("Sorting on key: ", key, file=sys.stderr)

    # Sort the data based on the key and direction.
    # In the special case of the "Occupancy" column, remove the '%' sign and do numeric sorting instead of alphabetical
    if key is 'occupancy':
        key_func = lambda x: float(x[key].replace('%',''))
        sorted_data = sorted(dict_list, key=key_func, reverse=(order_dir == "desc"))
	# else just sort alphabetically
    else:
        sorted_data = sorted(dict_list, key=lambda x: x[key], reverse=(order_dir == "desc"))

    return sorted_data

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