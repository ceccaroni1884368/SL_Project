#!/usr/bin/env python
# coding: utf-8

import Tools
import datetime
import os
import time



while True:
    currentDT = datetime.datetime.now()
    print('Current datetime: ' + str(currentDT)+'\n\n')
    
    Tools.download()
    time.sleep(3588)
    

