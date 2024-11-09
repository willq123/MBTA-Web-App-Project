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
    
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            data = json.load(response)
            if data['features']:
                coordinates = data['features'][0]['geometry']['coordinates']
                return str(coordinates[1]), str(coordinates[0])  # Return (latitude, longitude)
            else:
                raise ValueError("No matching location found.")
        else:
            raise ConnectionError(f"Error {response.status}: {response.reason}")
    



def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"{MBTA_BASE_URL}?filter[latitude]={latitude}&filter[longitude]={longitude}&sort=distance&api_key={MBTA_API_KEY}"
    
    with urllib.request.urlopen(url) as response:
        if response.status == 200:
            data = json.load(response)
            if data['data']:
                nearest_station = data['data'][0] # want to get the first item in the list
                station_name = nearest_station['attributes']['name']
                wheelchair_accessible = nearest_station['attributes']['wheelchair_boarding'] == 1  # 1 indicates accessible

                return station_name, wheelchair_accessible
            else:
                raise ValueError("No nearby stations found.")
    


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    latitude, longitude = get_lat_lng(place_name)
    station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
    return station_name, wheelchair_accessible


def main():
    """
    You should test all the above functions here
    """
    place_name = "Boston Common"
    print(get_lat_lng(place_name))
    


if __name__ == "__main__":
    main()


# When I run the code, it gives me urllib.error.HTTPError: HTTP Error 401: Unauthorized.
# ChatGPT said the possible API key or token is invalid or API Key not loaded correctly. 
# You might have to double check that. Thanks!