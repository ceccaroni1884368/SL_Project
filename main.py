#!/usr/bin/env python
# coding: utf-8

import Tools
import datetime
import os
import time

clear = lambda : os.system('cls')

while True:
    clear()
    print('SL_PROJECT DATAFRAME MANAGER\n')
    currentDT = datetime.datetime.now()
    print('Current datetime: ' + str(currentDT)+'\n\n')
    
    n = input('########### MENU ###########\n\n'+
               '1) Download dati giornalieri\n'+
               '2) Merge dataframe files\n'+
               'OTHER) Exit\n\nInserisci: ')
    if n == '1':
        Tools.download()
        time.sleep(5)
    elif n == '2':
        Tools.merge()
        time.sleep(5)
    else:
        break

