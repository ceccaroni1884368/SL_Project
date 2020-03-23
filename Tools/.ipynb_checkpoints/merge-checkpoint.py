#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from os import listdir
from os.path import isfile, join

def merge():
    df = pd.DataFrame()
    onlyfiles = [f for f in listdir('./data') if isfile(join('./data', f)) and '.csv' in f and f != 'dataframe.csv']

    for file in onlyfiles:
        df = pd.concat([df,pd.read_csv('./data/' + file)],axis=0,ignore_index=True)

    df = df.drop_duplicates()
    df.to_csv('./data/dataframe.csv')

    print('Creato: ./data/dataframe.csv')

#merge()