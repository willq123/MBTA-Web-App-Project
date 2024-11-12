from flask import Flask, request, redirect, url_for, render_template
# import os
# from dotenv import load_dotenv
from mbta_helper import find_stop_near # , get_lat_lng
from weather import get_weather
# from event import get_events

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST": 
        place_name = request.form.get("place_name")
        if place_name:
            return redirect(url_for("show_nearest_station", place_name=place_name))
        else:
            return render_template("home.html")  # Render home.html
    return render_template("home.html")  # Render home.html

@app.route("/nearest_mbta/<place_name>")
def show_nearest_station(place_name):
    try:
        station_name, wheelchair_accessible = find_stop_near(place_name)
        weather_description, temperature = get_weather(place_name)
        accessibility = "Yes" if wheelchair_accessible else "No"
        return render_template("nearest_station.html", place_name=place_name, station_name=station_name, accessibility=accessibility, weather_description=weather_description, temperature=temperature)  # Render nearest_station.html
    except Exception as e:
        return f"""
        <html>
        <body>
            <h1>Error</h1>
            <p>{str(e)}</p>
            <a href="/">Try again</a>
        </body>
        </html>
        """

if __name__ == "__main__":
    app.run(debug=True, port=5001)
