from flask import Flask, render_template, logging, request, Response
from flask_socketio import SocketIO

from modules.twitter_stream_consumer import TwitterStreamConsumer

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


@socketio.on('get_tweets', namespace='/webTweetStream')
def connect(bounds):
    app.logger.debug("/get_tweets socket")


@app.route("/streamTweets", methods=['GET'])
def stream_tweets():
    """
        Returns a response stream of JSON objects containing the real-time tweets within the area
        delimited by the coordinates given as argument in the request.
        For alignment with the Twitter API, the endpoint call for getting the tweet stream will
        look like:
            /streamTweets?north=N&south=S&west=W&east=E

        where N, S, W, E must be valid longitudes and latitudes delimiting the corner of the bounding
        box that covers the tweets area.
    :return: generator containing JSONs as stream response.
    """
    north = request.args.get('north', type=float)
    south = request.args.get('south', type=float)
    west = request.args.get('west', type=float)
    east = request.args.get('east', type=float)

    app.logger.info("API streaming tweets around in the region: [{},{},{},{}]".format(north, east,
                                                                                      south, west))
    consumer = TwitterStreamConsumer()
    consumer.start_stream({"north": north,
                           "east": east,
                           "west": west,
                           "south": south})

    def generate():
        while True:
            try:
                data = consumer.data_stream.get()
                yield data
            except Exception as e:
                print(e)

    return Response(generate(), content_type='application/json')


if __name__ == "__main__":
    app.debug = True
    app.debug_log_format = """-------------------------------------------------------------------------
                                %(worker_id)s (levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n%(message)s
                              -------------------------------------------------------------------------"""
    app.logger.setLevel(logging.DEBUG)
    app.logger.info("App start")
    socketio.run(app)
