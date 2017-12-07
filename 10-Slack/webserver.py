#!/usr/bin/python3

# Flask is a webserver library
from flask import Flask, request, render_template

# We will use the requests library to to issue a request to Slack
# and the json library to parse it
import requests
import json

SLACK_URL = "https://slack.com/oauth/authorize"

# Edit this file to add your own client details in the slack_app.json file
CONFIG_FILE = 'slack_app.json'
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
    
    return render_template("install_slack_app.html", url=url)

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
    
    # We store the code in a file as the webserver does not interact with the 
    # rest of the Python code, and we also want to reuse the code in the future
    # (Typically, we would store the access_token in a database.)
    f = open(OAUTH_FILE, 'w') # Store the code as a file
    f.write(resp.text + '\n')
    f.close()
    
    # If we start the server just to get the code, it is safe (and convenient) 
    # to shut down the web server after this request. 
    # stop_server()
    
    # What we return here has no real impact on the functionality of the code
    # Normally, we would just redirect the user to a "Thank you" page.
    return '<html><body>Code: <b>'+code+'</b><p>Response:<b>'+resp.text+'</b></body></html>'

def stop_server():
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    return

# This allows us to server files (in our case, images)
# that we create on the server.
@webserver.route('/plots/<path:path>')
def static_proxy(path):
    return webserver.send_static_file(path)
    

if __name__ == '__main__':
    
    # We open the CONFIG file here and read the details for the app
    f = open(CONFIG_FILE, 'r') 
    content = f.read()
    f.close()
    config= json.loads(content)
    CLIENT_ID = config['CLIENT_ID']
    CLIENT_SECRET = config['CLIENT_SECRET']
    REDIRECT = config['REDIRECT']
    PERMISSIONS = config['PERMISSIONS']
    webserver.run(host='0.0.0.0', port=5000, debug=True)

    
   

