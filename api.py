# api.py

import os
import json
import requests
import urllib.parse
from datetime import datetime


with open(os.path.join(os.path.dirname(__file__), 'secrets.json')) as f:
	secrets = json.load(f)

def get_secrets(setting):
	""" Get environment variables or return exception. """
	try:
		return secrets[setting]
	except KeyError:
		raise Exception(f"Set the {setting} environment variable.")


url = "https://external.transitapp.com/v3"
api_key = get_secrets("API_KEY")
headers = {'apiKey': api_key}


def get_coordinates(address: str):
	""" Gets the latitude x longitude for an address. """
	url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

	response = requests.get(url).json()
	lat = (response[0]["lat"])
	lon = (response[0]["lon"])
	return lat, lon


def nearby_stops(lat: float, lon: float):
	""" Get stops and global_stop_id with latitude and longitude. """
	with requests.get(url+"/public/nearby_stops", headers=headers, params={'lat': lat, 'lon': lon, 'max_distance': 400}) as data:

		stops = {}
		for i in data.json()['stops']:
			stops.update({i['stop_name']: i['global_stop_id']})

		return stops

def stop_departures(global_stop_id: str) -> list:
	""" Get departure times. """
	with requests.get(url+"/public/stop_departures", headers=headers, params={'global_stop_id': global_stop_id}) as data:

		f = data.json()['route_departures']

		# stopped here 5/14
		print(f[0]['itineraries'][0]['direction_headsign'])

		list_of_times = []
		for i in f[0]['itineraries'][0]['schedule_items']:
			# i['departure_time']
			list_of_times.append(datetime.utcfromtimestamp(i['departure_time']).strftime('%Y-%m-%d %H:%M:%S'))

		return list_of_times



if __name__ == '__main__':

	# user enters address

	# using address, gets coordinates
	address = get_secrets('ADDRESS')
	coor = get_coordinates(address)

	# using coordinates finds stops within a 300 meter radius
	nearbyStops = (nearby_stops(coor[0], coor[1]))

	# user picks stop

	# return train name / #, departure times
	print(stop_departures(nearbyStops['Right of Way / Ocean Ave']))





