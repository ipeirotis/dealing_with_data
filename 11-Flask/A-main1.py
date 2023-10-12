# This is a minimal code snippet to get a web server up and running using Repl.it

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello Panos!"
  
app.run(host='0.0.0.0', port=5000)
