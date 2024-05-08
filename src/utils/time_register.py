
from datetime import datetime
import numpy as np
import pandas as pd
import csv
import os
class TimeRegister:
    times = []
    dataset=[]
    cols = ['Event Description',"Event Time","Event Duration"]
    eventTime = datetime.now()
    lastTime = datetime.now()
    fileName = "register_time"
    
    @staticmethod
    def addTime(message):
       # print("times = ",TimeRegister.times)
        if len(TimeRegister.times) ==0:
            TimeRegister.restartTime()
        duration  = TimeRegister.getTimeDiff()
        TimeRegister.times.append([message,duration])
        TimeRegister.dataset = pd.DataFrame([[message,TimeRegister.eventTime,str(duration)+"s"]], columns = TimeRegister.cols)
        TimeRegister.register()
        TimeRegister.restartTime()
        

    @staticmethod
    def restartTime():
        TimeRegister.lastTime = TimeRegister.eventTime
        
    @staticmethod
    def getTimeDiff():
        TimeRegister.eventTime = datetime.now()
        result = TimeRegister.eventTime-TimeRegister.lastTime
        return result.total_seconds()
    
    @staticmethod   
    def register():    
        fileName = TimeRegister.fileName
        if ".csv" not in fileName:
            fileName = fileName+".csv"  
        exists = os.path.exists(fileName)
       # print('starting registring time file')
        try:
            with open(fileName,'a') as datasetFile:
                writer = csv.writer(datasetFile)
                if exists is False:
                    writer.writerow(TimeRegister.dataset.columns)
                for i in np.arange(int(TimeRegister.dataset.shape[0])):
                    writer.writerow(TimeRegister.dataset.iloc[i,])
          # print('finishing registring time file')
            TimeRegister.times=[]
        except:
            print('Falha ao registrar tempo')  
        
       