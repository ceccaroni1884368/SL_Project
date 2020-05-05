#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join

df = pd.DataFrame()
onlyfiles = [f for f in listdir('./') if isfile(join('./', f)) and '.csv' in f and f != 'dataframe.csv']

for file in onlyfiles:
    df = pd.concat([df,pd.read_csv('./' + file)],axis=0,ignore_index=True)

print('shape_pre:',df.shape)


# drop duplicates
idx = df[['local date','lat','lon']].drop_duplicates().index.tolist()
df = df.iloc[idx].reset_index(drop=True)

# drop NA location
df = df.dropna(subset=['location'])

# drop local time
df = df.drop(['local time'], axis=1)

# drop location
df = df.drop(['location'], axis=1)

# drop dew
df = df.drop(['dew'], axis=1)


# location for date
location_for_date={}
for i in range(len(df)):
    if df.iloc[i]['local date'] in location_for_date:
        location_for_date[df.iloc[i]['local date']].append((df.iloc[i]['lat'],df.iloc[i]['lon']))
    else:
        location_for_date[df.iloc[i]['local date']] = [(df.iloc[i]['lat'],df.iloc[i]['lon'])]
        
dates = df['local date'].drop_duplicates().tolist()

min_number_location = set(location_for_date['2020-03-30'])
max_number_location = set(location_for_date['2020-03-30'])
for date in dates:
    min_number_location = min_number_location.intersection(set(location_for_date[date]))
    max_number_location = max_number_location.union(set(location_for_date[date]))
    
# inserisco posti mancanti per data
for date in location_for_date:
    for lat_lon in max_number_location:
        if lat_lon not in location_for_date[date]:
            df = df.append(pd.DataFrame([{'local date': date, 'lat': lat_lon[0], 'lon': lat_lon[1]}]))
            
df = df.sort_values(by='local date').reset_index(drop=True)

print('shape_post',df.shape)

print(df.head())

print('NA values:\n')
print(df.isnull().sum(axis = 0))

