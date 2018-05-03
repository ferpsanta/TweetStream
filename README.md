## Geo Tweet real-time stream

The following project provides an API that given the coordinates in latitude and longitude of the two corners of a box, will return a JSON stream with all the tweets being tweeted in the delimited area.

There is two main resources in this projects:
* ```/``` : This returns the main view.
* ```/streamTweets``` : raw JSON tweet API.

### JSON API
This API returns a ```application/stream+json``` that will make all the tweets inside the bounding box passed as argument.

The bounding box is passed as argument by providing the coordinates (lat, lon) of the upper left and bottom right corners.

- A = (52.6035, -2.0600)
- B = (50.5978, 1.8472)
 
 The call to the API will be:
 
 ```/streamTweets?north=52.6035&amp;south=50.5978&amp;west=-2.0600&amp;east=1.8472```
 
And this call will return JSON objects at the users tweet in the delimited area:

### Main view


