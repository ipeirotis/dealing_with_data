import base64
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, text

app = Flask(__name__)

# This code creates a connection to the database
conn_string = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
    host='db.ipeirotis.org',
    user='student',
    db='citibike_fall2017',
    password='dwdstudent2015',
    encoding='utf8mb4')

engine = create_engine(conn_string)


@app.route('/citibike_api', methods=['GET'])
def citibike_stations():

  sql = "SELECT DISTINCT id, name, capacity, lat, lon  FROM status_fall2017"
  # Connect to the database, execute the query, and get back the results
  with engine.connect() as connection:
    stations = pd.read_sql(text(sql), con=connection)

  # Create the response. We will put the retrieved data as a list of
  # dictionaries, under the key "stations".
  list_of_stations = stations.to_dict(orient='records')

  api_results = {"stations": list_of_stations}

  # We JSON-ify our dictionary and return it as the API response
  return jsonify(api_results)


@app.route('/station_map', methods=['GET'])
def station_map():

  # Connect to the database, execute the query, and get back the results
  sql = "SELECT DISTINCT id, name, capacity, lat, lon  FROM status_fall2017"
  with engine.connect() as connection:
    stations = pd.read_sql(text(sql), con=connection)

  fig, ax = plt.subplots()
  ax = stations.plot(kind='scatter', x='lon', y='lat', ax=ax)

  buf = BytesIO()
  fig.savefig(buf, format="png")
  # Embed the result in the html output.
  data = base64.b64encode(buf.getbuffer()).decode("ascii")

  # Create the response. We will put the retrieved data as a list of
  # dictionaries, under the key "stations".
  results = {"image": data}

  # We JSON-ify our dictionary and return it as the API response
  return jsonify(results)

  # return f"<img src='data:image/png;base64,{data}'/>"


@app.route('/station_status')
def station_status():

  param = request.args.get('station_id')
  try:
    param_value = int(param)
  except:
    return jsonify({"error": "No station_id parameter given or other problem"})

  sql = '''SELECT available_bikes,
                      available_docks,
                      capacity,
                      available_bikes / capacity AS percent_full,
                      communication_time
               FROM status_fall2017
               WHERE id = %(station_id)s'''

  with engine.connect() as con:
    station_status = pd.read_sql(sql,
                                 con=con,
                                 params={"station_id": param_value})

  station_status_over_time = station_status.to_dict(orient='records')

  api_results = {
      "station_id": param_value,
      "status_over_time": station_status_over_time
  }

  # We JSON-ify our dictionary and return it as the API response
  return jsonify(api_results)


# Main page
@app.route("/")
def index():
  page = '''
  <html>
  <body>
    <a href="/citibike_api">Citibike API</a>
    <p>
    <a href="/station_map">Citibike Map as API call</a>
    <p>
    <a href="/station_status?station_id=72">Status of Station 72</a>
  </body>
  </html>
  '''

  return page


app.run(host='0.0.0.0', port=5000)
