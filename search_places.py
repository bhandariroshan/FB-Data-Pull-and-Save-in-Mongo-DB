from settings import *
import datetime 

def save_job(values):
    ''' This method saves the dictionary passed as jobs in the jobs Collection'''
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    try:
        db.jobs.insert(values)
    except:
        print "Data could not be saved"
    conn.disconnect()

def get_jobs():
    ''' This method reads the  jobs from the jobs Collection to search for in the facebook'''
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    try:
        places = db.jobs.find()
        places_list =  []
        for eachPlace in places:
            places_list.append(eachPlace)
        return places_list
    except:
        print "Could not find Collection"
    conn.disconnect()

def parse_places_api():
    ''' This method parses the json response of the places search of the facebook. 
    Note that the query below can be changed to specific words like coffee or books
    or bar or taxi to execute specific search in the facebook. '''

    query = '*'
    places = get_jobs()
    conn = Connection(SERVER,PORT)
    db = conn[DB_NAME]
    db.authenticate(USERNAME, PASSWORD)
    for eachPlace in places:
        #print eachPlace
        if (eachPlace['State'] == 'pending'):
            url = 'https://graph.facebook.com/search'
            payload= {
                'q':query,
                'center':eachPlace['center'],
                'type':'place',
                'access_token':APP_TOKEN
            }
            r = requests.get(url,params=payload)
            json_response = json.loads(r.text) 
            data = json_response['data']
            count = len(json_response['data'])
            while ('next' in json_response['paging']):
                #print json_response['paging']
                try:
                    url = json_response['paging']['next']
                    r = requests.get(url)
                    json_response = json.loads(r.text) 
                    data.extend(json_response['data'])
                except:
                    print "no data in next field"
                    continue
            for eachResult in data:
                #print eachResult
                try:
                    print count
                    count = count -1
                    db.placeSearchResult.update(eachResult,eachResult,True)
                    placeDetails = get_place_details(eachResult['id'])
                    db.placeDetails.update(placeDetails, placeDetails, True)
                except:
                    print "Data could not be saved"
                    continue
                db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'processing'}})
            db.jobs.update(eachPlace, {'$set':{'StateLastProcess':datetime.datetime.now(), 'state':'completed'}})
            conn.disconnect()
        else:
            continue

def get_place_details(placeId):
    ''' This method gets details of places using facebook graph api '''
    url = 'https://graph.facebook.com/' + placeId + '?access_token=' + APP_TOKEN
    r = requests.get(url)
    json_response = json.loads(r.text) 
    # print json_response
    return json_response

parse_places_api()

# save_job({"APISecure" : "demo",
#   "State" : "pending",
#   "StateLastChange" : "2013.10.21 14:23",
#   "StateLastProcess" : "2013-12-02T11:13:13.110Z",
#   "_id" : 2,
#   "center" : "52.516,13.383",
#   "city" : "berlin,germany",
#   "key" : "01",
#   "name" : "01",
#   "state" : "pending",
#   "type" : "places"})
