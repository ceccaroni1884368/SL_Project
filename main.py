#!/usr/bin/env python
# coding: utf-8

# Library
import requests
import pandas as pd
import numpy as np
import datetime
import threading
import time
import json
import datetime
import os
import progressbar


# Settings
base_url = "https://api.waqi.info"
token = open('public_waqitoken.txt').read()  # https://aqicn.org/api/
try:
    os.makedirs('data')
except FileExistsError:
    pass
with open('cities.txt', 'r') as f:
    cities = f.readlines()
cities_list = [line.rstrip('\n') for line in cities]


# City request
def city_request(city):
    r = requests.get(base_url + f"/feed/{city}/?token={token}")
    return r


# Make record
def make_record(r):
    """Extracts data from request r and returns a DataFrame."""
    item = r.json()
    rows = []
    
    if item['status'] == 'ok':
        # Date
        try:
            rows.append(datetime.datetime.strptime(item['data']['time']['s'], '%Y-%m-%d %H:%M:%S').date())
        except: 
            rows.append(np.nan)
        # Hour
        try:
            rows.append(datetime.datetime.strptime(item['data']['time']['s'], '%Y-%m-%d %H:%M:%S').time())
        except: 
            rows.append(np.nan)
        # City Name
        try:
            rows.append(item['data']['city']['name'])
        except: 
            rows.append(np.nan)  
        # Latitude
        try:
            rows.append(item['data']['city']['geo'][0])
        except: 
            rows.append(np.nan)
        # Longitude
        try:
            rows.append(item['data']['city']['geo'][1])
        except: 
            rows.append(np.nan)
        # AQI
        try:
            rows.append(item['data']['aqi'])
        except: 
            rows.append(np.nan)
        # Create record
        record = pd.Series(rows, index=['local date','local time', 'city', 'lat', 'lon', 'aqi'])
        # I AQI
        try:
            record = record.append(pd.DataFrame(item['data']['iaqi']).iloc[0])
        except:
            pass
        
        return record
    else:
        return np.nan


# Save Dataframe
def save(df):
    name = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    df.to_csv('data/' + name + '.csv', index = False)
    print('Saved file: data/' + name + '.csv')


# Make DataFrame
def make_dataframe(record):
    global df
    if type(record) != float:
        df = pd.concat([pd.DataFrame(record).transpose(),df],axis=0, sort=False, ignore_index=True)


# Application
def main():
    global df, cities_list
    df = pd.DataFrame()
    bar = progressbar.ProgressBar()
    for i in bar(range(len(cities_list))):
        make_dataframe(make_record(city_request(cities_list[i])))
 
    save(df)


if __name__ == '__main__':
    main()
