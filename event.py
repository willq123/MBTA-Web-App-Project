import requests
import os
from dotenv import load_dotenv
from mbta_helper import get_lat_lng

# Load environment variables from .env file
load_dotenv()
EVENTBRITE_API_KEY = os.getenv("EVENTBRITE_API_KEY")

def get_events(location):
    """
    find events near the given location using the Eventbrite API.
    """
    lat, lon = get_lat_lng(location)  # Reuse the get_lat_lng function from mbta_helper.py
    if lat is None or lon is None:
        raise Exception("Could not retrieve coordinates.")
    
    url = f"https://www.eventbriteapi.com/v3/users/me/?token={EVENTBRITE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return Exception("Could not retrieve events.")




data = get_events('boston')
print(data)