from settings import *
import datetime

def save_place(place,location,timezone):
    ''' This method can be used to save  a place along with the 
    location of the place, timezone that can be used to execute 
    event search in the facebook. Note the timezone can later be
    useful during filtering of the result.'''
    
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    try:
        db.places.insert({'place':place,'location':location, 'timezone':timezone})
    except:
        print "Data could not be saved"
    conn.disconnect()

def get_places():
    ''' This method reads the database for the places to be scanned for events'''
    
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    try:
        places = db.places.find()
        places_list =  []
        for eachPlace in places:
            places_list.append(eachPlace)
        return places_list
    except:
        print "Could not find Collection"
    conn.disconnect()

def parse_events_api():
    ''' This method makes event search in the facebook using its' 
    api and parses the json result and saves te results in the 
    eventSearchResult Collection of the dataface database.'''

    places = get_places()
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    for eachPlace in places:
        url = 'https://graph.facebook.com/search'
        payload= {
            'q':eachPlace['place'],
            'center':eachPlace['location'],
            'limit':5000,
            'type':'event',
            'access_token':LONG_ACCESS_TOKEN
        }
        r = requests.get(url,params=payload)
        json_response = json.loads(r.text) 
        data = json_response['data']

        while ('paging' in json_response):
            try:
                url = json_response['paging']['next']
                r = requests.get(url)
                json_response = json.loads(r.text) 
                data.extend(json_response['data'])
            except:
                #print "no data in next field"
                continue
        for eachResult in data:
            try:
                db.eventSearchResult.update(eachResult, eachResult, True)
                eventDetail = get_events_details(eachResult['id'])
                db.eventDetail.update(eventDetail, eventDetail, True)
                #print eachResult
            except:
               print "Data could not be saved"
               continue
        db.places.update({'$place':eachPlace},{'$set':{'lastUpdated':datetime.datetime.now()}})
    conn.disconnect()

def get_events_details(eventId='127923610711605'):
   ''' This method gets details of facebook events using facebook graph api '''
   url = 'https://graph.facebook.com/' + eventId + '?access_token=' + APP_TOKEN
   r = requests.get(url)
   json_response = json.loads(r.text) 
   print json_response
   return json_response

# save_place('Kathmandu', '27.70,85.33', 'Asia/Kathmandu')
# save_place('London', '51.50,0.1275', 'Europe/London')
# save_place('New York', '40.67,73.94', 'US/NewYork')
#parse_events_api()

parse_events_api()