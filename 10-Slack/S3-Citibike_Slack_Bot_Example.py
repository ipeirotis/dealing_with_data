
# coding: utf-8

# In[1]:


import time
import arrow
import re
import requests
import json
import MySQLdb as mdb
import pandas as pd
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from slackclient import SlackClient


# In[2]:


def message_is_for_our_bot(user_id, message_text):
    '''
    Check if the username and the word 'bot' appears in the text
    '''
    regex_expression = '.*@' + user_id + '.*bot.*'
    regex = re.compile(regex_expression)
    # Check if the message text matches the regex above
    match = regex.match(message_text)
    # returns true if the match is not None (ie the regex had a match)
    return match != None 


# In[3]:


def extract_station_name(message_text):
    '''
    Extract the station name. The regex relies on the question following a given pattern, so that we
    can extract the name of the station. In a more realistic chatbot, we would add multiple such patterns
    to make the interaction with the user easier.
    '''
    regex_expression = 'how many bikes on (.+) station'
    regex= re.compile(regex_expression)
    matches = regex.finditer(message_text)
    for match in matches:
        # return the first captured phrase
        # which is between "on" and "station"
        return match.group(1)
    
    # if there were no matches, return None
    return None


# In[4]:


def get_current_citibike_data_from_api(station_name):
    '''
    Returns a list of dictionaries with the station name and available bikes
    for all stations that have a matching station name
    '''
    url = 'http://www.citibikenyc.com/stations/json'
    data = requests.get(url).json()["stationBeanList"] 
    # Create a list of dictionaries with the stations containing
    # station_name in their name. Each of the dictionaries in the result
    # has three entries, the station id, name, and available bikes
    result = [ { 
                    "station_id": entry["id"], 
                    "station_name": entry["stationName"], 
                    "available": entry["availableBikes"]
               } 
            for entry in data 
            if station_name in entry["stationName"] and entry['statusValue'] == "In Service"
    ]
    return result


# In[5]:


def get_historic_citibike_data(station_id):
    '''
    For a given station_id, we connect to the database and return average usage
    data over the hours of the day. Notice that we get average results only for the day of the week same as today.
    Notice that our query converts the UTC timestamp into NYC timezone. 
    We return back a Pandas DataFrame with two columns (hours and bikes_available)
    and we set hours to be the index of the dataframe (this makes plotting simpler).
    '''
    con = mdb.connect(host = 'ipython.ipeirotis.com', 
                  user = 'root',
                  database = 'citibike_new',
                  passwd = 'dwdstudent2015', 
                  charset='utf8', use_unicode=True)
    
    query_template = '''
        SELECT HOUR(CONVERT_TZ(last_reported, '+00:00','-04:00')) AS hour, 
               FLOOR(AVG(num_bikes_available)) AS bikes_available
        FROM Status 
        WHERE station_id = %s 
              AND DAYOFWEEK(CONVERT_TZ(last_reported, '+00:00','-04:00')) = DAYOFWEEK(CONVERT_TZ(NOW(), '+00:00','-04:00'))
        GROUP BY HOUR(CONVERT_TZ(last_reported, '+00:00','-04:00'))
        ORDER BY HOUR(CONVERT_TZ(last_reported, '+00:00','-04:00'))
    '''
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(query_template, (station_id,) )
    bikes_available = cur.fetchall()
    cur.close()
    con.close()
    df = pd.DataFrame( list(bikes_available) )
    
    return df.set_index('hour').sort_index() 


# In[6]:


def plot_station_data(station_id, address, bikes_available):
    '''
    This function takes as input the station_id and creates a plot of the historic data
    '''
    
    # We will create a plot and save it under "plots" to make it available over the web
    date_now = arrow.utcnow().to("US/Eastern")
    dow = date_now.format('dddd')
    hour = date_now.time().hour
    
    # Get the Pandas dataframe with the average historic data and create a plot
    df = get_historic_citibike_data(station_id)
    ax = df.plot(legend=False)

    # we plot a vertical red line at the current time
    ax.axvline(x=hour, color='r', linestyle='--')
    
    # we add a  marker on the current level of bike availability
    # we just plot a single market at the (x,y) = (hour, bikes_available) location
    # using a red circle marker (shape "o") with red color and blue edges
    ax.plot(hour, bikes_available, marker='o', color='r', markeredgecolor='b', markersize=10)
    
    # Various options, just to customize the plot
    plot_title = 'Station #'+ str(station_id) + ' on ' + address + '\nAverage Availability for '+ dow
    ax.set_title(plot_title)
    ax.set_xlabel("Hour")
    ax.xaxis.set_ticks([0,4,8,12,16,20,24]) # select which values to show on the x-axis
    ax.grid(b=True, linestyle='--', color='#cccccc') # We want a light gray grid with dotted lines
    ax.set_ylabel("Available Bikes")
    

    # Save the plot and return its url
    fig = ax.get_figure()
    filename = 'plots/'+str(station_id)+ '_' + dow + '_' + str(hour) + '.png'
    fig.savefig(filename)
    plt.close(fig)
    
    url = 'http://ipython.ipeirotis.com:5000/' + filename
    
    return url


# In[7]:


def create_message(station_name):
    '''
    This function takes as input the username of the user that asked the question,
    and the station_name that we managed to extract from the question (potentially it can be None)
    We check the Citibike API and respond with the status of the Citibike stations.
    '''
    attachments = []
    if station_name != None:
        # We want to address the user with the username. Potentially, we can also check
        # if the user has added a first and last name, and use these instead of the username
        message = "Thank you for asking about the station on " + station_name + ". "

        # Let's get the data from the Citibike API
        # We search for stations that match "station_name"
        matching_stations = get_current_citibike_data_from_api(station_name)
        
        # If we cannot find any matching station...
        if len(matching_stations) == 0:
            message += "I could not find any matching station.\n"
        # If there are multiple matching stations
        if len(matching_stations) > 1:
            message += "We have multiple matching stations.\n"
            
        # Add the information for each station
        # For each station, we will return the current status
        # and a plot of historic averages which is computed
        # from our database.
        #
        # We return the plots as Slack message "attachments" 
        # See https://api.slack.com/docs/message-attachments
        # for details on the "attachment" object
        for station in matching_stations:
            station_id = station['station_id']
            address = station['station_name']
            bikes = station['available']
            # We get the plot from the historic data in our database
            # and we get the URL where we can access the plot
            url = plot_station_data(station_id, address, bikes)
            attachment = {
                "image_url": url,
                "title": "Historic data for station #{sid} at {a}".format(sid=station_id, a=address),
                "text": "Right now, it has {b} bikes available.".format(b=bikes)
            }
            attachments.append(attachment)
    else:
        message = "Unfortunately I did not understand the station you are asking for.\n"
        message += "Ask me `how many bikes on XXXXX station` and I will try to answer."
        
    return message, attachments


# In[8]:


def process_slack_event(event):
    '''
    The Slack RTM (real time messaging) generates a lot of events.
    We want to examine them all but only react to:
    1. Messages
    2. ...that come from a user
    3. ...that ask our bot to do something
    4. ...and act only for messages for which we can extract the data we need
    
    If we manage to extract a station name, we proceed to query the API and our database
    '''
    
    # Check that the event is a message. If not, ignore and proceed to the next event.
    if event.get("type") != 'message':
        return None

    # Check that the message comes from a user. If not, ignore and proceed to the next event.
    # We do not reply to bots, to avoid getting into infinite loops of discussions with other bots
    if event.get("user") == None:
        return None

    # Check that the message is asking the bot to do something. If not, ignore and proceed to the next event.
    message_text = event.get('text')
    if not message_is_for_our_bot(bot_user_id, message_text):
        return None

    # Extract the station name from the user's message
    station_name = extract_station_name(message_text)

    # Prepare the message that we will send back to the user
    message, attachments = create_message(station_name)

    return message, attachments


# In[9]:


# This is the beginning of the program. We just read read 
# the access token from the file and create the Slack Client
secrets_file = 'slack_secret.json'
f = open(secrets_file, 'r') 
content = f.read()
f.close()

auth_info = json.loads(content)
auth_token = auth_info["access_token"]
bot_user_id = auth_info["user_id"]

# Connect to the Real Time Messaging API of Slack and process the events
sc = SlackClient(auth_token)
sc.rtm_connect()


# In[10]:




# We are going to be polling the Slack API for recent events continuously
while True:
    # We are going to wait 1 second between monitoring attempts
    time.sleep(1)
    # If there are any new events, we will get a list of events. 
    # If there are no events, the response will be empty
    events = sc.rtm_read()
    for event in events:
        #print(event)
        # Check if we should generate a response for the event
        response = process_slack_event(event)
        if response:
            # Post a message to Slack with our response
            message, attachments = response
            sc.api_call("chat.postMessage", channel="#bots", text=message, attachments=attachments)

