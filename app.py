from flask import Flask, render_template, request, redirect, url_for, flash
from mbta_helper import get_nearest_station, get_lat_lng  # Importing the necessary functions

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    """ 
    Ask for place name and redirect to nearest_mbta route
    Error when place name is not valid
    """
    if request.method == 'POST':
        place_name = request.form.get('place_name')  # Get the input data
        if place_name and 1 <= len(place_name) <= 100:  # Make sure length is correct
            return redirect(url_for('nearest_mbta', place_name=place_name))  # Go to MBTA route
        else:
            return render_template('error.html', error_message='Invalid place name!')  # Direct to error page
    return render_template('index.html') 

@app.route('/nearest_mbta', methods=['GET', 'POST'])
def nearest_mbta():
    """
    Get the place name and finds the nearest MBTA station
    """
    place_name = request.args.get('place_name')  # Get the place name from the query parameters
    lat, lng = get_lat_lng(place_name)  # Get latitude and longitude for the place name
    if lat and lng:  # Check if valid coordinates were returned
        station_name, wheelchair_accessible_value = get_nearest_station(lat, lng)  # Find the nearest MBTA station

        if wheelchair_accessible_value == 2:
            wheelchair_accessible = "Inaccessible"
        elif wheelchair_accessible_value == 1:
            wheelchair_accessible = "Accessible"
        else:
            wheelchair_accessible = "Unknown"   
        
        if station_name:  # make sure it exists
            return render_template('mbta_station.html', station_name=station_name, wheelchair_accessible=wheelchair_accessible)  # Render the station page
    else:
        return render_template('error.html', error_message='Invalid coordinates from place!')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error_message='Page not found!'), 404  # Render an error page

if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode


