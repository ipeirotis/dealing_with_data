# A slighlty more advanced version of a webserver
# We have two pages (/ and /hello)

from datetime import datetime
from flask import Flask

app = Flask(__name__)

# We add a global variable that will be used to count the visitors to a specific URL
visitor_counter = 0

# Go to http://<your IP>/hello to see the message
@app.route('/hello')
def hello_visitor():
    global visitor_counter
    visitor_counter += 1
    return '<H1>Hello! You are visitor #{i}</H1>'.format(i=visitor_counter)
  
# The function simply returns a message with the 
# current date and time.
def get_time_message():
    datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    time = datetime.now().strftime('%H:%M:%S')
    message = f"<P>The date is {date}<P>The time is {time}"
    return message


# Augmenting the basic "Hello world" with a message 
# that shows the date and time
@app.route("/")
def home():
    message = get_time_message()
    return "<H1>Hello World!" + message +"</H1>"

app.run(host='0.0.0.0', port=5000)




