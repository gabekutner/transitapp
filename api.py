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
	""" Get departure times. """
	with requests.get(url+"/public/stop_departures", headers=headers, params={'global_stop_id': global_stop_id}) as data:

		response = data.json()['route_departures']

		list = []

		for i in response:

			ls = []

			direction_headsign = i['itineraries'][0]['direction_headsign']
			route_long_name = i['route_long_name']
			route_short_name = i['route_short_name']
			tts_long_name = i['tts_long_name']
			tts_short_name = i['tts_short_name']
			route_color = i['route_color']

			list_of_times = []
			for v in i['itineraries'][0]['schedule_items']:
				# i['departure_time']
				list_of_times.append(datetime.utcfromtimestamp(v['departure_time']).strftime('%H:%M:%S'))


			ls.append(direction_headsign)
			ls.append(route_long_name)
			ls.append(route_short_name)
			ls.append(tts_long_name)
			ls.append(tts_short_name)
			ls.append(route_color)
			ls.append(list_of_times)

			list.append(ls)

		return list



if __name__ == '__main__':

	# user enters address

	# using address, gets coordinates
	address = get_secrets('ADDRESS')
	coor = get_coordinates(address)

	# using coordinates finds stops within a 1500 meter radius
	nearbyStops = (nearby_stops(coor[0], coor[1], 'dict'))

	# user picks stop

	# return train name / #, departure times

	# commented to not show stops near me
	# departure_info = stop_departures(nearbyStops[])

	# print(departure_info)
	





