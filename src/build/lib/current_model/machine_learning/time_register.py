
from datetime import datetime
import numpy as np
import pandas as pd
import csv
import os
class TimeRegister:
    times = []
    dataset=[]
    cols = ['data_read','ML_training','ML_published','total']
    lastTime = datetime.now()
    
    @staticmethod
    def addTime():
        print("times = ",TimeRegister.times)
        if len(TimeRegister.times) ==0:
            TimeRegister.restartTime()
        time  = TimeRegister.getTimeDiff()
        TimeRegister.times.append(time)
        if len(TimeRegister.times) >=3:
            total = sum(TimeRegister.times)
            TimeRegister.times.append(total)
            print('mounting dataset time')
            TimeRegister.dataset = pd.DataFrame([TimeRegister.times], columns = TimeRegister.cols)
            TimeRegister.register('data_time_registration.csv')

    def restartTime():
        TimeRegister.lastTime = datetime.now()
    def getTimeDiff():
        timeNow = datetime.now()
        result = timeNow-TimeRegister.lastTime
        TimeRegister.restartTime()
        return result.total_seconds()
        
    def register(fileName):        
        exists = os.path.exists(fileName)
        print('starting registring time file')
        try:
            with open(fileName,'a') as datasetFile:
                writer = csv.writer(datasetFile)
                if exists is False:
                    writer.writerow(TimeRegister.dataset.columns)
                for i in np.arange(int(TimeRegister.dataset.shape[0])):
                    writer.writerow(TimeRegister.dataset.iloc[i,])
            print('finishing registring time file')
            TimeRegister.times=[]
        except:
            print('Falha ao registrar tempo')  
        
       