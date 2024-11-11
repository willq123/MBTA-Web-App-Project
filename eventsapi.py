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
    
    url = f"https://www.eventbrite.com/api/v3/events/search/?location.latitude={lat}&location.longitude={lon}&token={EVENTBRITE_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        events_list = []
        for event in data['events']:
            events_list.append((event['name']['text'], event['start']['local'], event['venue']['address']['localized_address_display']))
        return [(event['name']['text'], event['start']['local'], event['venue']['address']['localized_address_display']) for event in data['events']]
    else:
        raise Exception("Could not retrieve events.")
    
print(get_events("Boston Commons"))
