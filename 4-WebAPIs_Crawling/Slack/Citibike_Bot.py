#!/usr/bin/python3

import time
import re
import requests


# In[ ]:

def message_matches(user_id, message_text):
    '''
    Check if the username and the word 'bot' appears in the text
    '''
    regex_expression = '.*@' + user_id + '.*bot.*'
    regex = re.compile(regex_expression)
    # Check if the message text matches the regex above
    match = regex.match(message_text)
    # returns true if the match is not None (ie the regex had a match)
    return match != None 


# In[ ]:

def extract_station_name(message_text):
    '''
    Extract the station name. The regex relies on the question having a specific form
    '''
    regex_expression = 'how many bikes on (.+) station'
    regex= re.compile(regex_expression)
    matches = regex.finditer(message_text)
    for match in matches:
        return match.group(1)
    
    # if there were no matches, return None
    return None


# In[ ]:

def get_citibike_data(station_name):
    '''
    Returns a list of dictionaries with the station name and available bikes
    for all stations that have a matching station name
    '''
    url = 'http://www.citibikenyc.com/stations/json'
    data = requests.get(url).json()["stationBeanList"] 
    # Create a list of dictionaries. Each dictionary has two entries, the station name and available bikes
    result = [ {"station_name": entry["stationName"], "available": entry["availableBikes"]} 
            for entry in data if station_name in entry["stationName"]]
    return result


# In[ ]:

def create_message(username, station_name):
    '''
    This function takes as input the username of the user that asked the question,
    and the station_name that we managed to extract from the question (potentially it can be None)
    We check the Citibike API and respond with the status of the Citibike stations.
    '''
    
    if station_name != None:
        # We want to address the user with the username. Potentially, we can also check
        # if the user has added a first and last name, and use these instead of the username
        message = "Thank you @{u} for asking about the station on {s}.\n".format(u=username, s=station_name)

        # Let's get the data from the Citibike API
        matching_stations = get_citibike_data(station_name)
        # If we cannot find any matching station
        if len(matching_stations) == 0:
            message += "I could not find any matching station.\n"
        # If there are multiple matching stations
        if len(matching_stations) > 1:
            message += "We have multiple matching stations.\n"
        # Add the information for each station
        for station in matching_stations:
            address = station['station_name']
            bikes = station['available']
            message += "The station at {a} has {b} available bikes.\n".format(a=address, b=bikes)
    else:
        message =  "Thank you @{u} for asking. ".format(u=username)
        message += "Unfortunately I did not understand what is the station you are asking for.\n"
        message += "Ask me _how many bikes on XXXXX station_ and I will try to answer."
        
    return message


# In[ ]:

# Read the access token from the file and create the Slack Client
import json

secrets_file = 'slack_secret.json'
f = open(secrets_file, 'r') 
content = f.read()
f.close()

auth_info = json.loads(content)
auth_token = auth_info["access_token"]
bot_user_id = auth_info["user_id"]

from slackclient import SlackClient
sc = SlackClient(auth_token)



# In[ ]:

# Connect to the Real Time Messaging API of Slack and process the events

if sc.rtm_connect():
    # We are going to be polling the Slack API for recent events continuously
    while True:
        # We are going to wait 1 second between monitoring attempts
        time.sleep(1)
        # If there are any new events, we will get a response. If there are no events, the response will be empty
        response = sc.rtm_read()
        for item in response:
            # Check that the event is a message. If not, ignore and proceed to the next event.
            if item.get("type") != 'message':
                continue
                
            # Check that the message comes from a user. If not, ignore and proceed to the next event.
            if item.get("user") == None:
                continue
            
            # Check that the message is asking the bot to do something. If not, ignore and proceed to the next event.
            message_text = item.get('text')
            if not message_matches(bot_user_id, message_text):
                continue
                
            # Get the username of the user who asked the question
            response = sc.api_call("users.info", user=item["user"])
            username = response['user'].get('name')
            
            # Extract the station name from the user's message
            station_name = extract_station_name(message_text)

            # Prepare the message that we will send back to the user
            message = create_message(username, station_name)

            # Post a response to the #bots channel
            sc.api_call("chat.postMessage", channel="#assignment2_bots", text=message)
                
        


# In[ ]:



