#!/usr/bin/python

# coding: utf-8

# In[1]:

import requests
import json

# Connect to the Citibike API and fetch the data
def getCitibikeData():
    ''' 
    Connects to the API, and returns back a list
    of dictionaries, each dictionary corresponding
    to a Citibike station
    '''
    # Let's get the data from the Citibike API
    url = 'http://www.citibikenyc.com/stations/json'
    resp = requests.get(url)
    results = json.loads(resp.text)
    data = results["stationBeanList"]
    return data

citibike_data = getCitibikeData()


# In[2]:

import MySQLdb as mdb
import sys

# Setup the database in which we will store the Citibike data
def connectDB():
    con = mdb.connect(host = 'localhost', 
                      user = 'root', 
                      passwd = 'dwdstudent2015', 
                      charset = 'utf8', use_unicode=True);
    return con

def createCitibikeDB(con, db_name):
    ''' 
    Connects to the database and creates (if it does not exist)
    the database and the tables needed to store the data
    '''
    # Query to create a database
    create_db_query = "CREATE DATABASE IF NOT EXISTS {0} DEFAULT CHARACTER SET 'utf8'".format(db_name)

    # Create a database
    cursor = con.cursor()
    cursor.execute(create_db_query)
    cursor.close()
    pass

def createTimeInvariantTable(con, db_name, table_name):
    cursor = con.cursor()
    # Create a table
    # The {0} and {1} are placeholders for the parameters in the format(....) statement
    create_table_query = '''CREATE TABLE IF NOT EXISTS {0}.{1} 
                                    (station_id int, 
                                    station_name varchar(250), 
                                    latitude float,
                                    longitude float,
                                    total_docks int,
                                    PRIMARY KEY(station_id)
                                    )'''.format(db_name, table_name)
    cursor.execute(create_table_query)
    cursor.close()
    
def createTimeVaryingTable(con, db_name, table_name):
    cursor = con.cursor()
    # Create a table
    # The {0} and {1} are placeholders for the parameters in the format(....) statement
    create_table_query = '''CREATE TABLE IF NOT EXISTS {0}.{1} 
                                    (station_id int,
                                    date datetime,
                                    availableDocks int,
                                    status varchar(40),
                                    availableBikes int,
                                    testStation int,
                                    PRIMARY KEY(station_id, date)
                                    )'''.format(db_name, table_name)
    cursor.execute(create_table_query)
    cursor.close()

con = connectDB()
db_name = 'citibike'
createCitibikeDB(con, db_name)
station_table = 'station_info'
createTimeInvariantTable(con, db_name, station_table)
station_table = 'station_status'
createTimeVaryingTable(con, db_name, station_table)


# In[3]:

# Go over the Citibike data and store the time-invariant
# data into the appropriate table in the database
def storeTimeInvariantData(con, citibike_data):
    '''
    Accepts as a parameter a list of dictionaries, where
    each dictionary is a Citibike station.
    Goes over these dictionaries, and stores in the database
    the entries that are time invariant.
    We need to check if Citibike station entry exists,
    and if it does not, store it in the database
    '''
    db_name = 'citibike'
    table_name = 'station_info'
    
    for station in citibike_data:
        station_id = station["id"]
        stationName = station["stationName"]
        total_docks = station["totalDocks"]
        lat = station["latitude"]
        lon = station["longitude"]
        insertStation(con, db_name, table_name, 
                      station_id, stationName, total_docks, lat, lon)
    
    # Writes the data in the database, for sure
    con.commit()
    return
 
def insertStation(con, db_name, table_name, 
                  station_id, stationName, total_docks, lat, lon):
    query_template = '''INSERT IGNORE INTO {0}.{1}(station_id, 
                                    station_name, 
                                    latitude,
                                    longitude,
                                    total_docks) 
                VALUES (%s, %s, %s, %s, %s)'''.format(db_name, table_name)

    cursor = con.cursor()
    query_parameters = (station_id, stationName, lat, lon, total_docks)
    cursor.execute(query_template, query_parameters)
    cursor.close()


storeTimeInvariantData(con, citibike_data)


# In[4]:

from datetime import datetime

# Go over the Citibike data and store the time-varying
# data into the appropriate table in the database
def storeTimeVaryingData(con, citibike_data):
    '''
    Accepts as a parameter a list of dictionaries, where
    each dictionary is a Citibike station.
    Goes over these dictionaries, and stores in the database
    the entries that are time invariant.
    We need to check if Citibike station entry, together
    with the matching "lastCommunication" timestamp exists,
    and if it does not, store it in the database
    '''
    db_name = 'citibike'
    table_name = 'station_status'
    
    for station in citibike_data:
        station_id = station["id"]
        date_str = station["lastCommunicationTime"]
        date  =  datetime.strptime(date_str, '%Y-%m-%d %I:%M:%S %p')
        available_docks = station["availableDocks"]
        status = station["statusValue"]
        available_bikes = station["availableBikes"]
        testStation = station["testStation"],
        insertStatus(con, db_name, table_name, 
            station_id, date, available_docks, status, available_bikes, testStation)

    con.commit()
    
    return
        
def insertStatus(con, db_name, table_name, 
                  station_id, date, available_docks, status, available_bikes, testStation):
    query_template = '''INSERT IGNORE INTO {0}.{1}(station_id, 
                                    date,
                                    availableDocks, 
                                    status,
                                    availableBikes,
                                    testStation) 
                VALUES (%s, %s, %s, %s, %s, %s)'''.format(db_name, table_name)

    cursor = con.cursor()
    query_parameters = (station_id, date, available_docks, status, 
                        available_bikes, testStation)
    cursor.execute(query_template, query_parameters)
    cursor.close()

    return

storeTimeVaryingData(con, citibike_data)


# In[ ]:



