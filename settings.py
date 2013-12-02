#!/usr/bin/python
import requests
import json
from facepy import GraphAPI
from urlparse import parse_qs
import pymongo
from pymongo import Connection
import sys

#..................Face APP SETTINGS..........................
FACEBOOK_APP_ID='*******'
FACEBOOK_APP_SECRET='*******'
APP_TOKEN = '******'
#..................Face APP SETTINGS..........................

#..................Server Settings............................
SERVER = 'avuxi-rnd.cloudapp.net' #put Server = localhost for local connection
PORT = 27017
DB_NAME = 'dataface'
USERNAME = 'roshan'
PASSWORD = '**********'
#..................Server Settings............................

#..................Facebook User Access Token.................
ACCESS_TOKEN = '******'
LONG_ACCESS_TOKEN = '*****'
#..................Facebook User Access Token.................

#https://developers.facebook.com/tools/access_token


def get_app_token():
    ''' This method generates user APP TOKEN 
    Please go to the https://developers.facebook.com/apps link to create
    app and generate app credentials
    '''
    graph = GraphAPI()
    response = graph.get(
            path='oauth/access_token',
            client_id=FACEBOOK_APP_ID,
            client_secret=FACEBOOK_APP_SECRET,
            grant_type='client_credentials'
    )
    data = parse_qs(response)
    APP_TOKEN = data['access_token'][0]
    print APP_TOKEN
    return APP_TOKEN

def get_long_access_token():
    ''' This method generates the long lived access token, 
    using the short lived access token. Please note that the short 
    lived access token in taken from https://developers.facebook.com/tools/access_token 
    and is valid only for hour and  after running this method copy the value printed in 
    the  terminal and paste it to  the LONG_LIVED_ACCESS_TOKEN value above
    '''
    graph = GraphAPI()
    response = graph.get(
            path='oauth/access_token',
            client_id=FACEBOOK_APP_ID,
            client_secret=FACEBOOK_APP_SECRET,
            grant_type='fb_exchange_token',
            fb_exchange_token=ACCESS_TOKEN
    )
    data = parse_qs(response)
    LONG_LIVED_ACCESS_TOKEN = data['access_token'][0]
    print LONG_LIVED_ACCESS_TOKEN
    return LONG_LIVED_ACCESS_TOKEN
#print get_app_token()
get_long_access_token()