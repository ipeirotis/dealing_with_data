#!/usr/bin/python3

# In this cell, we configure our example web server. 
# We will show in the next cell how to configure this
# web server to handle the OAuth2 calls.

# Flask is a webserver
from flask import Flask, request

# We add a global variable that will be used to count the visitors to a specific URL
visitor_counter = 0
# Initialize the embedded web server
webserver = Flask("MyFirstWebServer")

import datetime
import time
# Go to http://<your IP>:5000/ to see the response
@webserver.route('/')
def hello_world():
    # stop_server()
    return 'Hello Panos, it is now ' + str(datetime.date.today()) 

# Go to http://<your IP>:5000/testNYU to see the different message
@webserver.route('/testNYU')
def hello_nyu():
    # stop_server()
    global visitor_counter
    visitor_counter += 1
    return 'Hello! You are visitor #{i}'.format(i=visitor_counter)

def start_server():
    global visitor_counter
    visitor_counter = 0
    webserver.run(host='0.0.0.0', port=5000)
    return
    
def stop_server():
    shutdown_after_request = request.environ.get('werkzeug.server.shutdown')
    shutdown_after_request()
    return

start_server()