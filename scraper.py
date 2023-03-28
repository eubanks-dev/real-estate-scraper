# scraper.py

from flask import Flask
import requests
from bs4 import BeautifulSoup
import sys
import json

app = Flask(__name__)

@app.route("/scraped-data")
def index():
	print("About to parse realpage data", file=sys.stderr)
	relevant_data = parse_realpage()	
	print(relevant_data, file=sys.stderr)
	return "done"

def parse_realpage():
	realpage_data = json.loads(hardcoded_realpage_data())
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
	"""Returns an excerpt of the JSON data returned by realpage at the following URL: https://dac.realpage.com/dac/markets/16980/properties

	Returns:
		string: Hardcoded realpage JSON data
	"""

	return '''
	[
		{
			"propertyId":8668,
			"propertyName":"Clover Ridge East Apartments",
			"zipCode":"60074",
			"address":"1445 E Evergreen Dr",
			"city":"Palatine",
			"state":"IL",
			"averageSquareFootage":863,
			"stories":"3",
			"stable":"stable",
			"class":"B",
			"latitude":"42.1322402",
			"longitude":"-88.0098342",
			"imageHero":"/85/785/hero_b7bbb5.jpg",
			"heroSource":"RealPage",
			"submarketName":"Arlington Heights/Palatine/Wheeling",
			"unitcount":275,
			"yearBuilt":"1986",
			"metricData":[
				{
					"metricCode":"MPF-RPSF",
					"metricValue":2.110,
					"metricValueFormatted":"$2.110"
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.1346,
					"metricValueFormatted":"13.46%"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":2.110,
					"metricValueFormatted":"$2.110"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1823,
					"metricValueFormatted":"$1,823"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1823,
					"metricValueFormatted":"$1,823"
				},
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9891,
					"metricValueFormatted":"98.91%"
				}
			]
		},
		{
			"propertyId":9030,
			"propertyName":"Riverwood",
			"zipCode":"60438",
			"address":"3649 173rd Ct",
			"city":"Lansing",
			"state":"IL",
			"averageSquareFootage":908,
			"stories":"4",
			"stable":"stable",
			"class":"C",
			"latitude":"41.5794661",
			"longitude":"-87.5267188",
			"imageHero":"/92/1192/hero_9ad847.jpg",
			"heroSource":"RealPage",
			"submarketName":"South Cook County",
			"unitcount":354,
			"yearBuilt":"1971",
			"metricData":[
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1200,
					"metricValueFormatted":"$1,200"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.0166,
					"metricValueFormatted":"1.66%"
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1200,
					"metricValueFormatted":"$1,200"
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.322,
					"metricValueFormatted":"$1.322"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.322,
					"metricValueFormatted":"$1.322"
				},
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9492,
					"metricValueFormatted":"94.92%"
				}
			]
		},
		{
			"propertyId":9032,
			"propertyName":"Tiberon Trails",
			"zipCode":"46410",
			"address":"1240 W 52nd Dr",
			"city":"Merrillville",
			"state":"IN",
			"averageSquareFootage":836,
			"stories":"3",
			"stable":"stable",
			"class":"C",
			"latitude":"41.523104",
			"longitude":"-87.348678",
			"imageHero":"/96/1196/hero_b8f73c.jpg",
			"heroSource":"RealPage",
			"submarketName":"Merrillville/Portage/Valparaiso",
			"unitcount":376,
			"yearBuilt":"1971",
			"metricData":[
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.0459,
					"metricValueFormatted":"4.59%"
				},
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9495,
					"metricValueFormatted":"94.95%"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":950,
					"metricValueFormatted":"$950"
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.136,
					"metricValueFormatted":"$1.136"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.136,
					"metricValueFormatted":"$1.136"
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":950,
					"metricValueFormatted":"$950"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				}
			]
		},
		{
			"propertyId":9168,
			"propertyName":"Fox Crest",
			"zipCode":"60085",
			"address":"2805 W Glen Flora Ave",
			"city":"Waukegan",
			"state":"IL",
			"averageSquareFootage":814,
			"stories":"3",
			"stable":"stable",
			"class":"C",
			"latitude":"42.3771352",
			"longitude":"-87.8689769",
			"imageHero":"/56/1356/hero_8a32bc.jpg",
			"heroSource":"RealPage",
			"submarketName":"Lake County/Kenosha",
			"unitcount":244,
			"yearBuilt":"1983",
			"metricData":[
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9836,
					"metricValueFormatted":"98.36%"
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1214,
					"metricValueFormatted":"$1,214"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.492,
					"metricValueFormatted":"$1.492"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.492,
					"metricValueFormatted":"$1.492"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1214,
					"metricValueFormatted":"$1,214"
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.0541,
					"metricValueFormatted":"5.41%"
				}
			]
		},
		{
			"propertyId":9179,
			"propertyName":"Axis at Westmont",
			"zipCode":"60559",
			"address":"One Fountainhead Dr",
			"city":"Westmont",
			"state":"IL",
			"averageSquareFootage":969,
			"stories":"2",
			"stable":"stable",
			"class":"C",
			"latitude":"41.7799435",
			"longitude":"-87.9765453",
			"imageHero":"/69/1369/hero_a715bb.jpg",
			"heroSource":"RealPage",
			"submarketName":"Southeast DuPage County",
			"unitcount":400,
			"yearBuilt":"1971",
			"metricData":[
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.593,
					"metricValueFormatted":"$1.593"
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.0556,
					"metricValueFormatted":"5.56%"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1543,
					"metricValueFormatted":"$1,543"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.593,
					"metricValueFormatted":"$1.593"
				},
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9575,
					"metricValueFormatted":"95.75%"
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1543,
					"metricValueFormatted":"$1,543"
				}
			]
		},
		{
			"propertyId":9180,
			"propertyName":"Twin Lake Towers",
			"zipCode":"60559",
			"address":"200 W 60th St",
			"city":"Westmont",
			"state":"IL",
			"averageSquareFootage":865,
			"stories":"6",
			"stable":"stable",
			"class":"B",
			"latitude":"41.779239",
			"longitude":"-87.9816724",
			"imageHero":"/70/1370/hero_db03f1.jpg",
			"heroSource":"RealPage",
			"submarketName":"Southeast DuPage County",
			"unitcount":399,
			"yearBuilt":"1969",
			"metricData":[
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.839,
					"metricValueFormatted":"$1.839"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1591,
					"metricValueFormatted":"$1,591"
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":0.1359,
					"metricValueFormatted":"13.59%"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1591,
					"metricValueFormatted":"$1,591"
				},
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9724,
					"metricValueFormatted":"97.24%"
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.839,
					"metricValueFormatted":"$1.839"
				}
			]
		},
		{
			"propertyId":9424,
			"propertyName":"Williamsburg On The Lake",
			"zipCode":"46383",
			"address":"2810 Winchester Dr",
			"city":"Valparaiso",
			"state":"IN",
			"averageSquareFootage":907,
			"stories":"2",
			"stable":"stable",
			"class":"C",
			"latitude":"41.4943199",
			"longitude":"-87.0352368",
			"imageHero":"/50/1650/hero_d4e563.jpg",
			"heroSource":"RealPage",
			"submarketName":"Merrillville/Portage/Valparaiso",
			"unitcount":150,
			"yearBuilt":"1981",
			"metricData":[
				{
					"metricCode":"MPF-OCC",
					"metricValue":0.9733,
					"metricValueFormatted":"97.33%"
				},
				{
					"metricCode":"MPF-HIST-ASK-RENT",
					"metricValue":1241,
					"metricValueFormatted":"$1,241"
				},
				{
					"metricCode":"MPF-RENT",
					"metricValue":1241,
					"metricValueFormatted":"$1,241"
				},
				{
					"metricCode":"MPF-HIST-AVG-ASK-RPSF",
					"metricValue":1.368,
					"metricValueFormatted":"$1.368"
				},
				{
					"metricCode":"MPF-RPSF",
					"metricValue":1.368,
					"metricValueFormatted":"$1.368"
				},
				{
					"metricCode":"MPF-ANN-RENT-CHG",
					"metricValue":-0.1148,
					"metricValueFormatted":"-11.48%"
				},
				{
					"metricCode":"MPF-HIST-CONC-RATIO",
					"metricValue":null,
					"metricValueFormatted":null
				}
			]
		}
	]
   '''

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