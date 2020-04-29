from datetime import datetime
from opencage.geocoder import OpenCageGeocode
import requests
# GET requests to stream data from NASA's OpenNotify API


# Request current location of ISS
def request_iss_location():
    response = requests.get("http://api.open-notify.org/iss-now.json")
    json_data = response.json()
    time_stamp = json_data['timestamp']
    lat = json_data['iss_position']['latitude']
    lon = json_data['iss_position']['longitude']
    # Format into a readable time-stamp
    formatted_ts = datetime.utcfromtimestamp(time_stamp).strftime('%m-%d-%Y %H:%M:%S')
    return float(lat), float(lon), formatted_ts


# Request ISS flight crew information
def request_flight_crew_info():
    response = requests.get("http://api.open-notify.org/astros.json")
    json_data = response.json()
    number = json_data['number']
    flight_crew = []
    # Get the name of each crew member
    for person in json_data['people']:
        flight_crew.append(person['name'])
    return flight_crew


# How many times/when will ISS pass over this location?
def request_pass_predictions(lat, lon):
    # Request parameters
    payload = {'lat': lat, 'lon': lon}
    response = requests.get("http://api.open-notify.org/iss-pass.json?", params=payload)
    json_data = response.json()
    pass_info = json_data['response']
    pass_times = []
    for p in pass_info:
        formatted_time = datetime.utcfromtimestamp(p['risetime']).strftime('%m-%d-%Y %H:%M:%S')
        pass_times.append(formatted_time)
    return pass_times


# Find location based on coordinates
def request_location_from_coords(lat, lon):
    key = '95d6bcc151474d98a00b4181e587bf15'
    geocoder = OpenCageGeocode(key)
    response = geocoder.reverse_geocode(lat, lon)
    info = response[0]['components']
    all_info = []
    if 'city' in info:
        all_info.append(info['city'])
    if 'state' in info:
        all_info.append(info['state'])
    if 'country' in info:
        all_info.append(info['country'])
    if 'body_of_water' in info:
        all_info.append("The " + info['body_of_water'])
    final_string = ""
    for item in all_info:
        final_string += item + ", "
    return final_string.rstrip(', ')


def request_coords_from_location(location):
    key = '95d6bcc151474d98a00b4181e587bf15'
    geocoder = OpenCageGeocode(key)
    response = geocoder.geocode(location)
    try:
        lat = round(response[0]['geometry']['lat'], 4)
        lon = round(response[0]['geometry']['lng'], 4)
    except IndexError:
        return 0, 0
    else:
        return lat, lon
