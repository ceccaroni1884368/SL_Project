#!/usr/bin/env python
# coding: utf-8

import requests
import pandas as pd
import numpy as np
import datetime
import threading
import time


# Settings
base_url = "https://api.waqi.info"
token = open('waqitoken.txt').read()  # https://aqicn.org/api/
cities_list = ['Rome', 'London', 'Barcelona']
WAIT_TIME_SECONDS = 10800  # 10800 -> 3 hour


def city_request(city):
    r = requests.get(base_url + f"/feed/{city}/?token={token}")
    return r


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


def save(df):
    df.to_pickle('data.pkl')


def load():
    return pd.read_pickle('data.pkl')


def make_dataframe(record):
    global df
    df = pd.concat([pd.DataFrame(record).transpose(),df],axis=0, sort=False, ignore_index=True)
    save(df)


def data_collect_application():
    global df, cities_list
    
    try:
        df = load()
    except:
        df = pd.DataFrame()

    for city in cities_list:
        make_dataframe(make_record(city_request(city)))
    
    print('Last update: ' + time.ctime())


def main():

    ticker = threading.Event()
    while not ticker.wait(WAIT_TIME_SECONDS):
        data_collect_application()


if __name__ == '__main__':
    main()




