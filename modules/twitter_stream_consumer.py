import logging
import queue

from flask import current_app as app
from tweepy import Stream, OAuthHandler, TweepError
from tweepy.streaming import StreamListener

logger = logging.getLogger(__name__)


class JsonListener(StreamListener):
    """
        The streaming api is quite different from the REST api because the REST api is used to
        pull data from twitter but the streaming api pushes messages to a persistent session.
        This allows the streaming api to download more data in real time than could be done using
        the REST API.

        In Tweepy, an instance of tweepy.Stream establishes a streaming session and routes messages
        to StreamListener instance.
    """
    def __init__(self, data_stream):
        super(JsonListener, self).__init__()
        self.data_stream = data_stream

    def on_data(self, data):
        self.data_stream.put(data)

    def on_error(self, status):
        # Sometimes you will get the error code 420, this error is due to the api limit reached.
        # Error codes: https://developer.twitter.com/en/docs/basics/response-codes
        logger.error("Error {} while getting data.".format(status))


class TwitterStreamConsumer(object):
    """
        TwitterStreamConsumer class handles the starting and the stop of the tweet consumer stream.
        It's mandatory to have the following keys set in the flask app configuration:
        + TWITTER_CONSUMER_KEY
        + TWITTER_CONSUMER_SECRET
        + TWITTER_ACCESS_TOKEN
        + TWITTER_ACCESS_TOKEN_SECRET
    """
    def __init__(self):
        self.auth_token = OAuthHandler(app.config['TWITTER_CONSUMER_KEY'],
                                       app.config['TWITTER_CONSUMER_SECRET'])
        self.auth_token.set_access_token(app.config['TWITTER_ACCESS_TOKEN'],
                                         app.config['TWITTER_ACCESS_TOKEN_SECRET'])

        self.data_stream = queue.Queue()  # data shared queue
        self.stream_listener = JsonListener(self.data_stream)
        self.stream = Stream(self.auth_token, self.stream_listener)

    def start_stream(self, coordinates):
        """
            Starts a new live-stream in the given coordinates in an asynchronous way.
        :param coordinates: dictionary containing the coordinates of the 2 edges of the region to be
                            shown
        :return: None
        """
        logger.info("New tweet stream started in {}".format(self.area_coordinates(coordinates)))
        try:
            self.stream.filter(locations=self.area_coordinates(coordinates), async=True)
        except TweepError as e:
            logger.error("{}".format(e))

    @staticmethod
    def area_coordinates(coordinates):
        """
            Converts from dictionary of coordinates to a list containing the coordinates in order.
        :param coordinates: dictionary containing north-east south-west coordinates.
        :returns list containing the coordinates from the dict in order.
        """
        return [coordinates['west'],
                coordinates['south'],
                coordinates['east'],
                coordinates['north']]
