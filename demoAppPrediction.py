# Abstraction for send and get data from application
from appInterface import ApplicationInterface

# For prediction task
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from darts import TimeSeries
from darts.models import ExponentialSmoothing

# For the application to be called by the API or others nodes
from flask import Flask, jsonify
from flask_restful import Resource, Api
from multiprocessing import Process
"""
========================================================
Note: 
------
The purpose of this application is to show how
to use the python interface to interact with the API.

The goal of this application is to take data from 
a node, make calculations (here prediction on future 
data) and send the results back to a node.

Command:
--------
requests.get('http://127.0.0.1:5000/query-example').text
 requests.get('http://127.0.0.1:5000/run-app')

https://github.com/jbaudru & https://github.com/llucbono 
========================================================
"""

# TO LISTEN FROM CALL FROM API
app = Flask(__name__)
# TO CONNECT TO API to get or post DATA
URL = "http://localhost:8000/ec/payloads"
interface = ApplicationInterface(URL)

def startCommunication(app):
    #server = Process(target=app.run(host="0.0.0.0", debug= True, port=5000))
    server = Process(target=app.run(debug= True, port=5000))
    server.start()    

def stopCommunication(server):
    server.terminate()
    server.join()    

@app.route('/query-example')
def query_example():
    return 'Query String Example'

@app.route('/run-app')
def run_app():
    try:
        # YOUR CODE HERE BELOW
        print("[+] Getting data")
        res = interface.getListOfMessageFromSensorType("deg")
        data = res['data']
        res = str(makePrediction(data))
    except:
        res = "Application does not seem to have worked properly :/"
    return res

def main():
    interface.postInit()
    startCommunication(app)


def makePrediction(data):
    print("[+] Making predictions")
    temp = []; date = []; df = pd.DataFrame()
    for dat in data:
        temp.append(dat['values'][0]['value'])
        dat = dt.datetime.fromtimestamp(dat['values'][0]['date']).strftime('%Y-%m-%d')
        date.append(dat)
    df["date"]=date; df["temp"]=temp
    df = df.drop_duplicates(subset=['date'])
    size_pred = 7 # Number of day

    end = str(dt.date(2000,4,9) + dt.timedelta(days=14)).replace("-","")
    times = pd.date_range('20000101', end, freq="D")
    
    series = TimeSeries.from_dataframe(df, 'date', 'temp', fill_missing_dates=True, freq=None)
    train, val = series[:-size_pred], series[-size_pred:]

    model = ExponentialSmoothing()
    
    print("[+] Fitting model for timeseries prediction")
    model.fit(train)
    prediction = model.predict(len(val), num_samples=len(times))
        
    return prediction.values()[-1][0]
    #series.plot(color="blue")
    #prediction.plot(label='forecast', color="purple", low_quantile=0.05, high_quantile=0.95)
    #plt.legend()
    #plt.show()


if __name__ == '__main__':
    main()