## Geo Tweet real-time stream

The following project provides an API that given the coordinates in latitude and longitude of the two corners of a box, will return a JSON stream with all the tweets being tweeted in the delimited area.

There is two main resources in this projects:
* ```/``` : This returns the main view.
* ```/streamTweets``` : raw JSON tweet API.

### JSON API
This API returns a ```application/stream+json``` that will make all the tweets inside the bounding box passed as argument.

The bounding box is passed as argument by providing the coordinates (lat, lon) of the upper left and bottom right corners.

<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/box_example.PNG" width="500"/>

- A = (52.6035, -2.0600)
- B = (50.5978, 1.8472)
 
 The call to the API will be:
 
 ```/streamTweets?north=52.6035&south=50.5978&west=-2.0600&east=1.8472```
 
And this call will return JSON objects at the users tweet in the delimited area:

<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/api.gif" width="750"/>


### Main view

<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/demo5.gif" width="600"/>


The main view keeps connected to the tweet stream to update in realtime the map with the new tweets. This connection has been done using websockets [due to a limitation of javascript to process a json stream](https://stackoverflow.com/questions/6558129/process-a-continuous-stream-of-json)

In the map there is a box representing the bounding box (as used for the API), that the users can interact with:

 * Drag and move around the map
<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/demo3.gif" width="600"/>

 * Resize
<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/demo2.gif" width="600"/>

The tweets in the stream will be within the area delimited by that box. Aditionally, the tweets __that contains geo information__ will be shown in the map with a marker, and will show the tweet by putting the mouse over them:
<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/demo1.gif" width="600"/>
 
Everytime a tweet is received this will be shown in the bottom of the map.
Also, when the box is moved the URI link will change providing a direct link to the API.

#### User concurrency

The back-end supports concurrency of multiple users, and the interface is synchronized between them so the changes done by one users will be noticed by the others.

<img src="https://github.com/ferpsanta/TweetStream/blob/master/demo/demo6.gif" width="600"/>


# Installation

For installing you should follow the following steps:
1. cd to the directory where ```requirements.txt``` is located
2. activate your virtualenv (recommended)
3. run: ```pip install -r requirements.txt``` in your shell
4. set your API keys correctly in the file ```config.cfg```. For this step you will need a [Twitter standard API key](https://developer.twitter.com/en/docs/basics/getting-started#get-started-app) and a [Google API key](https://developers.google.com/maps/documentation/embed/).
5. run: ```python app.py```

