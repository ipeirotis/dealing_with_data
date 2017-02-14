#!/usr/bin/python3

# This part creates a web server that will "receive" the requests by Slack
# in the `redirect_uri`

# In this cell, we just configure the server. We can start it, 
# using the start_server() function

# Flask is a webserver library
from flask import Flask, request

# We will use the requests library to to issue a request to Slack
# and the json library to parse it
import requests
import json

SLACK_URL = "https://slack.com/oauth/authorize"

# Get these after registering an app with Slack
# These are to communicate to Slack that the requests come
# from a legitimate, registered app. Ensure that you 
# put your own client details here
CLIENT_ID = '132047100118.137144102401'
CLIENT_SECRET = '71b7d5e4e062f9c12b864f472f1e2e4e'
# You need to put your own IP address here and register it under "OAuth & Permissions"
REDIRECT = 'http://ipython.ipeirotis.com:5000/slack' 
PERMISSIONS = 'client'

# This is the location where we will store the authentication data from Slack
OAUTH_FILE = 'slack_secret.json'

    
# Initialize the Flask web server
# We create a folder "plots" where we are going to store
# plots to post them (later on) as messages to Slack channels
webserver = Flask("SlackOAuth", static_folder='plots')

# This URL will just have a link that the user clicks to install
# the Slack bot
@webserver.route("/install")
def install_bot():
    url = (SLACK_URL + 
    '?response_type=code' + 
    '&client_id='+ CLIENT_ID + 
    '&scope=' + PERMISSIONS +
    '&redirect_uri=' + REDIRECT )
    
    return '<html><body><a href="'+url+'"><b>Install Slack Bot</b></a></body></html>'

# This is the place where the webserver will receive the call from Slack
# The call from Slack will have a parameter "code"
@webserver.route("/slack")
def oauth_helper():
    code = request.args.get('code')
    
    # Now that we got the code 
    # we request the access token from Slask. Notice that we 
    # use the client_secret to prove that the app is the real one
    # that was registered with the Slack API
    url = "https://slack.com/api/oauth.access"
    params = {"grant_type": "authorization_code", 
              "client_id": CLIENT_ID, 
              "client_secret": CLIENT_SECRET, 
              "code": code,
              "redirect_uri": REDIRECT}
    resp = requests.get(url, params=params)
    data = json.loads(resp.text)
    userid = data["user_id"]
    
    # We store the code in a file as the webserver does not interact with the 
    # rest of the Python code, and we also want to reuse the code in the future
    # (Typically, we would store the access_token in a database.)
    f = open(OAUTH_FILE, 'w') # Store the code as a file
    f.write(resp.text)
    f.close()
    
    # If we start the server just to get the code, it is safe (and convenient) 
    # to shut down the web server after this request. 
    stop_server()
    
    # What we return here has no real impact on the functionality of the code
    return '<html><body>Code: <b>'+code+'</b><p>Response:<b>'+resp.text+'</b></body></html>'


# This allows us to server files (in our case, images)
# that we create on the server.
# You can start the server from a notebook using
# the "%run WebServer_Receive_Slack_Authentication.py" command
@webserver.route('/plots/<path:path>')
def static_proxy(path):
    return webserver.send_static_file(path)


def start_server():
    webserver.run(host='0.0.0.0', port=5000)
    return
    
def stop_server():
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    return
    


    
# And now start the webserver so that we can receive the answer from Slack API
start_server()
