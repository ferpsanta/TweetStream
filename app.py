from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder="templates")
socketio = SocketIO(app, async_mode=None)  # Async mode will be handled automatically

# Load configuration from config.cfg
app.config.from_pyfile('config.cfg')
# Push the app configuration to the app context for it to be available to the submodules.
app.app_context().push()

""" GLOBAL VARIABLES """
# Map view starting coordinates
init_coords = {'lat': 42.1850,
               'lng': 38.8140}
coordinates = {"east": 1.8472,
               "west": -2.060,
               "south": 50.5978,
               "north": 52.6035}


""" API """


@app.route("/")
def mapview():
    """
        Method in charge to render the GoogleMaps map, centered in the given coordinates and with
        a box delimited by "area_bounds", this box will represent the area covered by the tweet
        stream.
    :return: html with the map
    """
    return render_template('index.html',
                           center=init_coords,
                           area_bounds=coordinates,
                           google_api_key=app.config['GOOGLE_API_KEY'],
                           async_mode=socketio.async_mode)


if __name__ == "__main__":
    app.debug = True
    socketio.run(app)
