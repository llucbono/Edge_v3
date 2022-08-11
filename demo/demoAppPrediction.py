# Abstraction for send and get data from application
from appInterface import ApplicationInterface

# For prediction task
import pandas as pd
import datetime as dt
from darts import TimeSeries
from darts.models import ExponentialSmoothing

# For the application to be called by the API or others nodes
from flask import Flask
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
docker image build -t project .\demo\
docker run project

requests.get('http://127.0.0.1:5000/query-example').text
requests.get('http://127.0.0.1:5000/run-app').content

https://github.com/jbaudru & https://github.com/llucbono
========================================================
"""
# TO CONNECT TO API to get or post DATA
URL = "http://192.168.0.219:8000/ec/payloads"
LOCAL_IP = "0.0.0.0"
interface = ApplicationInterface(URL)

# TO LISTEN FROM CALL FROM API
app = Flask(__name__)

def startCommunication(app):
    server = Process(target=app.run(host=LOCAL_IP, debug= True, port=5000))
    server.start()

def stopCommunication(server):
    server.terminate()
    server.join()

@app.route('/hi')
def query_example():
    return 'Hello there'

@app.route('/run-app')
def run_app():
    try:
        # YOUR CODE HERE
        print("[+] Getting data")
        res = interface.getListOfMessageFromSensorType("deg")
        data = res['data']
        res = str(makePrediction(data))
    except:
        res = "Application does not seem to have worked properly :/"
    return res

def main():
    interface.postInit(LOCAL_IP) # SEND THE IP OF THE APP TO THE API
    startCommunication(app)

# Just a random function to demonstrate the principle
# YOUR CODE HERE
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
