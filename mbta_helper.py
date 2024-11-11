import json
import os
import urllib.request
import pprint

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
MAPBOX_TOKEN = os.getenv("MAPBOX_TOKEN")
MBTA_API_KEY = os.getenv("MBTA_API_KEY")

# Useful base URLs (you need to add the appropriate parameters for each API request)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it
def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_lng() and get_nearest_station() might need to use this function.
    """
    with urllib.request.urlopen(url) as resp:
        response_text = resp.read().decode("utf-8")
        response_data = json.loads(response_text)
        return response_data
    

def get_lat_lng(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{urllib.parse.quote(place_name)}.json?access_token={MAPBOX_TOKEN}"
    data = get_json(url)
    if data['features']:
        coordinates = data['features'][0]['geometry']['coordinates']
        return str(coordinates[1]), str(coordinates[0])  # Return (latitude, longitude)
    else:
        return None


def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance"
    response =urllib.request.urlopen(url)
    response_text = response.read().decode("utf-8")
    data = json.loads(response_text)
    if data['data']:
        station_name = data['data'][0]['attributes']['name']
        wheelchair_accessible = data['data'][0]['attributes']['wheelchair_boarding']

        return station_name, wheelchair_accessible
    else:
        return None, None


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    lat, lng = get_lat_lng(place_name)
    if lat is None or lng is None:
        return "There is no Statiuon near this place"
    else:
        return get_nearest_station(lat, lng)


def main():
    """
    You should test all the above functions here
    """
    place_name = "Boston Commons"
    lat, lng = get_lat_lng(place_name)
    # print(lat, lng)

    nearest_station = get_nearest_station(lat, lng)
    # print(nearest_station)
    
    name, accessibility = find_stop_near("Boston Commons")
    # print(name, accessibility)
    

if __name__ == "__main__":
    main()


# When I run the code, it gives me urllib.error.HTTPError: HTTP Error 401: Unauthorized.
# ChatGPT said the possible API key or token is invalid or API Key not loaded correctly. 
# You might have to double check that. Thanks!