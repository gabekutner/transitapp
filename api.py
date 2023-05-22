# api.py

import os
import json
import requests
import urllib.parse
from datetime import datetime, timedelta


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

def entry_check(address: str):
	""" Checks the entry value. """
	ls = list(address)
	if ls[len(ls)-1] == " ":
		address = address[:-1]
		return address


def get_coordinates(address: str):
	""" Gets the latitude x longitude for an address. """

	checked_address = entry_check(address)
	if checked_address == None:
		url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
	else:
		url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(checked_address) +'?format=json'

	response = requests.get(url).json()

	try:
		lat = response[0]["lat"]
		lon = response[0]["lon"]
		return lat, lon, checked_address
	except IndexError:
		return None

	

def nearby_stops(lat: float, lon: float, output: str = "list"):
	""" Get stops and global_stop_id with latitude and longitude. 

		Args: 
			lat: The latitude of the address.
			lon: The longitude of the address.
			output: The data type to return. Default is a list.
	"""
	with requests.get(url+"/public/nearby_stops", headers=headers, params={'lat': lat, 'lon': lon, 'max_distance': 1500}) as data:

		if output == 'dict': 
			stops = {}
			for i in data.json()['stops']:
				stops.update({i['stop_name']: i['global_stop_id']})

		elif output == 'list':
			# for gui, there needs to be a list returned
			stops = []
			for i in data.json()['stops']:
				stops.append(i['stop_name'])

		else:
			raise Exception('Specify list or dict in nearby_stops call.')

		return stops

def stop_departures(global_stop_id: str) -> list:
	""" Get departure times. 

		Args:
			global_stop_id: The global stop id.
	"""
	with requests.get(url+"/public/stop_departures", headers=headers, params={'global_stop_id': global_stop_id}) as data:

		response = data.json()['route_departures']

		list_of_trains = []
		for i in response:

			train_list = []

			direction_headsign = i['itineraries'][0]['direction_headsign']
			route_long_name = i['route_long_name']
			route_short_name = i['route_short_name']
			tts_long_name = i['tts_long_name']
			tts_short_name = i['tts_short_name']
			route_color = i['route_color']

			list_of_times = []
			for v in i['itineraries'][0]['schedule_items']:
				dt = (datetime.fromtimestamp(v['departure_time']).strftime('%Y-%m-%d %H:%M:%S'))
				list_of_times.append(dt)

			train_list.append(direction_headsign)
			train_list.append(route_long_name)
			train_list.append(route_short_name)
			train_list.append(tts_long_name)
			train_list.append(tts_short_name)
			train_list.append(route_color)
			train_list.append(list_of_times)

			list_of_trains.append(train_list)

		return list_of_trains



if __name__ == '__main__':

	# user enters address

	# using address, gets coordinates
	address = get_secrets("ADDRESS")
	coor = get_coordinates(address)
	# print(coor)
	# print(coor)

	# using coordinates finds stops within a 1500 meter radius
	nearbyStops = (nearby_stops(coor[0], coor[1], 'dict'))

	# print(nearbyStops)

	# print(nearbyStops)

	# user picks stop

	# return train name / #, departure times

	# commented to not show stops near me
	departure_info = stop_departures(nearbyStops["West Portal"])

	print(departure_info)






