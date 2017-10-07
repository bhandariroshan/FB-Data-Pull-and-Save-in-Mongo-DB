FB-Data-Pull-and-Save-in-Mongo-DB
=================================

This project aims to make use of Facebook Graph API and then pull events, event details happening around various locations specified as latitude and longitude. It also parses the facebook places api to search various locations around a specific location. Then saves the data in the mongodb. This project uses python and mongodb database. Pymongo is used to make remote connection.

To run the code, you need to follow following instructions:-
=================================

1. To install the requirements:-
	
	pip install -r requirements.txt

2. Settings 
 
 a. Create a facebook app from :-  https://developers.facebook.com/apps
 
 	i.  Get the APP_ID and APP_SECRET and put in the respective values in settings.py file 
	
	ii. Run the method get_app_token() and copy the value printed in terminal.
	   Paste it in the APP_TOKEN= '......here.....' in settings.py file
	   
 b. For the Facebook Settings:-
 
 	i. Generate the temporary access token from here:-
 		https://developers.facebook.com/tools/access_token

 	ii. Put this token in the ACCESS_TOKEN ='......here......' variable in the settings.py file.
	
 	iii. Note that this token is valid only for 1 hour. So you need to generate LONG_LIVED_ACCESS_TOKEN 
	
 	     by running the get_long_access_token() method of settings.py Please note and copy the value printed 
 		 in the terminal and paste it in the 
 		 LONG_LIVED_ACCESS_TOKEN = '.......here......'
		 
 3. To run the facebook Event Search
 
  	i. First put the place along with its' latitude and longitude value in the place collection of dataface database. 
	   I have included some sample in the database and it looks something like this:-
	  	{
		    "_id" : ObjectId("52984f5a269b8c2b689a1930"),
		    "timezone" : "US/NewYork",
		    "place" : "New York",
		    "location" : "40.67,73.94"
		}

	ii. To save a new location you can use save_place(place, location, Timezone) method in the search_events.py file
		
		Eg:-
		save_place('London', '51.50,0.1275', 'Europe/London')
		save_place('New York', '40.67,73.94', 'US/NewYork') 

	iii. To execute places search on every document in the places collection, you need to run the parse_events_api() 
		method in the search_events.py file. This document parses every location from the facebook event search api and 
		parses every result from the facebook api and keeps in the eventSearchResult collection.
		
		Ex documents in the collection:-
		{
			"_id" : ObjectId("52987751aa805bd8b83d0d0b"),
			"id" : "127923610711605",
			"start_time" : "2013-11-27T03:00:00+0000",
			"name" : "Robert Stone in Conversation With Rachel Kushner at The Strand",
			"location" : "New York, NY, United States"
		}

		{
			"_id" : ObjectId("52987751aa805bd8b83d0d0c"),
			"id" : "137004316485839",
			"start_time" : "2013-11-27T00:00:00+0000",
			"location" : "Brooklyn, NY, United States",
			"name" : "Cheap Blue Yonder @ Rubber Tracks - Brooklyn, NY",
			"end_time" : "2013-11-27T03:00:00+0000"
		}

	iv. Note to get events for any location only you can use filters in the mongodb queries.

4. To run the facebook places search:-

    i. First put the latitude and longitude value in the center in the jobs collection. 
    
    	Ex:- 
		{
			"APISecure" : "demo",
			"State" : "pending",
			"StateLastChange" : "2013.10.21 14:23",
			"StateLastProcess" : ISODate("2013-11-30T08:33:44.621Z"),
			"_id" : 2,
			"center" : "52.516,13.383",
			"city" : "berlin,germany",
			"key" : "01",
			"name" : "01",
			"type" : "places"
		}

ii. You can use save_job method in the search_places.py file to create new job there:- 
	
	Ex:- 
	save_job('
		{
			"APISecure" : "demo",
			"State" : "pending",
			"StateLastChange" : "2013.10.21 14:23",
			"StateLastProcess" : ISODate("2013-11-30T08:33:44.621Z"),
			"_id" : 2,
			"center" : "52.516,13.383",
			"city" : "berlin,germany",
			"key" : "01",
			"name" : "01",
			"type" : "places"
		}
	)
	

iii. To run the places search then you can execute the parse_places_api() method in the search_places.py file
	
Please note that this method takes no query, if you want to execute search for specific topic(like:- "coffee" or "medicine" or "bakery" or "hotels" or "airport" or "taxi" or "book" etc) you have to change the query = '*' filed in the parse_places_api() method in the search_places.py file. The results of the api are saved in the searcPlacesResults collection as:- 
		
		
		{
			"_id" : ObjectId("52994cd4269b8c0808d97971"),
			"category" : "Political organization",
			"name" : "Schekker",
			"category_list" : [
				{
					"id" : "2261",
					"name" : "Political Organization"
				}
			],
			"location" : {
				"city" : "Berlin",
				"zip" : "10117",
				"country" : "Germany",
				"longitude" : 13.38375,
				"state" : "",
				"street" : "Dorotheenstr. 84 ",
				"latitude" : 52.5184212
			},
			"id" : "203779599653854"
		}

NOTE:

PLEASE REPLACE THE ACCESS_TOKEN AND THE LONG_ACCESS_TOKEN IN THE SETTINGS.PY FILE WITH THE ACCESS_TOKEN AND LONG_ACCESS_TOKEN THAT WILL BE GENTERATED BY METHOD MENTIONED ABOVE
