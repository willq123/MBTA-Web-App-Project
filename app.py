from flask import Flask, request, redirect, url_for
from mbta_helper import find_stop_near

app = Flask(__name__)

# def hello():
#     return "Hello World!" # this is the original one that is given by the prof
# not sure what we need to deal with it. I just keep it here FYI. 


@app.route("/", methods = ["GET", "POST"])
def home():
    """
    Display the home page with a form to input a place name.
    Handle the form submission and redirect to the nearest station page.
    """
    if request.method == "POST": 
        place_name = request.form.get("place_name")
        if place_name:
            return redirect(url_for("show_nearest_station", place_name = place_name))
        else:
            return """
            <html>
            <body>
                <h1>Welcome to the MBTA Station Finder</h1>
                <form method="POST" action="/">
                    <label for="place_name"> Enter a place name:</label>
                    <input type="text" id="place_name" name="place_name" required>
                    <button type="submit">Submit</button>
                </form>
                <p style = "color:red;"> Error: Please enter a valid place name.</p>
            </body>
            </html>
            """
    return """
    <html>
    <body>
        <h1>Welcome to the MBTA Station Finder</h1>
        <form method="POST" action="/">
            <label for="place_name">Enter a place name:</label>
            <input type="text" id="place_name" name="place_name" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """
        

@app.route("/nearest_mbta/<place_name>")
def show_nearest_station(place_name):
    try:
        station_name, wheelchair_accessible = find_stop_near(place_name)
        accessibility = "Yes" if wheelchair_accessible else "No"
        result = f"""
        <html>
        <body>
            <h1>Nearest MBTA Station to {place_name}</h1>
            <p><strong>Station Name:</strong> {station_name}</p>
            <p><strong>Wheelchair Accessible:</strong> {accessibility}</p>
            <a href="/">Search again</a>
        </body>
        </html>
        """
        return result
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
    app.run(debug=True, port = 5001)

# I didn't use the html template. I combine the html and the app into one.
# It worked out tho. If you want, you can make revisions and separate the code.

