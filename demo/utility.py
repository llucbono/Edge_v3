import matplotlib.pyplot as plt
import pandas as pd
import os
import json

class Utility:
    
    def __init__(self):
        self.lstX = []
        self.lstY = []
        self.lstTitle = []
    
    def getLocalData(self, path):
        f = open(path)
        values = json.load(f)
        return values
    
    def dumpData(self, dict):
        return json.dumps(dict, indent = 4)
    
    def plotAllResponseTime(self):
        fig = plt.figure(figsize = (12, 5))
        for i in range(0, len(self.lstY)):
            plt.plot(self.lstX[i], self.lstY[i], label=self.lstTitle[i])
        plt.ylabel("Time (s)")
        plt.xlabel("Request")
        plt.title("All request response time")
        plt.xticks(rotation = 45, fontsize=8)
        plt.legend()
        plt.subplots_adjust(bottom=0.2)
        name = os.getcwd() +"/res/comparison.png"
        try:
            plt.savefig(name)
        except:
            print("[-] Error - Unable to save the chart")
    
    def plotResponseTime(self, NB_REQUEST, lst_x, lst_y, title):
        self.lstX.append(lst_x)
        self.lstY.append(lst_y)
        self.lstTitle.append(title)
        data = pd.DataFrame(lst_y)
        t_average = data.rolling(NB_REQUEST//20).mean()
        fig = plt.figure(figsize = (12, 5))
        plt.plot(lst_x, lst_y, color ='cornflowerblue', label="Response time")
        plt.plot(lst_x, t_average, color ='red', label="Average")
        plt.ylabel("Time (s)")
        plt.xlabel("Request")
        plt.title(title)
        plt.xticks(rotation = 45, fontsize=8)
        plt.legend()
        plt.subplots_adjust(bottom=0.2)
        name = os.getcwd() +"/res/" + title + ".png"
        try:
            plt.savefig(name)
        except:
            print("[-] Error - Unable to save the chart")