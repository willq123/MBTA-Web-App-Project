import os
from dotenv import load_dotenv
from mbta_helper import get_lat_lng
import urllib.request
import json


# Load environment variables from .env file
load_dotenv()
# OPENWEAHTER_API_KEY = os.getenv("OPENWEAHTER_API_KEY")
OPENWEAHTER_API_KEY = "609fbd278449cd40fd0ebb63cc736e4e"

def get_weather(location):
    """
    Fetch the weather data for the given location using OpenWeather API.
    """
    lat, lon = get_lat_lng(location)
    if lat is None or lon is None:
        raise Exception("Could not retrieve coordinates.")
    
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={OPENWEAHTER_API_KEY}&units=metric"
    
    with urllib.request.urlopen(url) as response:
        response_text = response.read().decode("utf-8")
        data = json.loads(response_text)        
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        return weather_description, temperature
    
    
