import argparse
from cProfile import label
import requests
from requests.structures import CaseInsensitiveDict
import json
import matplotlib.pyplot as plt
import pandas as pd
import time
import os
from tqdm import tqdm

URL = "http://localhost:8000/ec/payloads"
NB_REQUEST = 100

def main(args):  
    lst_getDataNodeById = []; lst_getMessageByIP = []; lst_sendNodeData = []; lst_request = []; lst_deleteFromID = []
    pbar = tqdm(total=NB_REQUEST)
    count = 0
    while(count < NB_REQUEST):
        if(args.v == 1): print("[+] Request : " + str(count))
        
        st = time.time()
        getDataNodeById(0, args.v) # get test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getDataNodeById.append(ed - st)
        
        st = time.time()
        deleteFromID(0, args.v) # get test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_deleteFromID.append(ed - st)
        
        st = time.time()
        sendNodeData(URL, args.v) # send test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_sendNodeData.append(ed - st)
        
        st = time.time()
        getMessageByIP("192.168.56.1", args.v) # send test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getMessageByIP.append(ed - st)
        
        lst_request.append(count)
        count += 1
        pbar.update(1)
    pbar.close()
    
    plotResponseTime(lst_request, lst_getDataNodeById, "getDataNodeById")
    plotResponseTime(lst_request, lst_sendNodeData, "sendNodeData")
    plotResponseTime(lst_request, lst_getMessageByIP, "getMessageByIP")
    plotResponseTime(lst_request, lst_deleteFromID, "deleteFromID")

def getDataNodeById(ID, verbose=0):
    url= URL + "/" + str(ID)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.get(url=url, headers=headers)
    if(verbose==1):
        print(resp.status_code)

def getMessageByIP(IP, verbose=0):
    url= URL + "/" + str(IP)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.get(url=url, headers=headers)
    if(verbose==1):
        print(resp.status_code)

def deleteFromID(ID, verbose=0):
    url= URL + "/" + str(ID)
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.delete(url=url, headers=headers)
    if(verbose==1):
        print(resp.status_code)

def sendNodeData(URL="http://localhost:8000/ec/payloads", verbose=0):
    # STRING
    ip = "0.0.0.0:8000"
    # INTEGER
    date = 1637678232454
    # STRING
    type = "BatSense"
    # LIST
    val = getLocalData("data.json")
    # defining a params dict for the parameters to be sent to the API
    DATA = {'ip':ip, 'date':date, 'type':type, 'values':val["values"]}
    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.post(url=URL, headers=headers, data=DATA)
    if(verbose==1):
        print(resp.status_code)
        print(DATA)

def getLocalData(path):
    f = open(path)
    values = json.load(f)
    return values

def plotResponseTime(lst_x, lst_y, title):
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
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process args for edge computing project")
    parser.add_argument("--v", help="Verbose (0/1)", type=int, default=0)
    args = parser.parse_args()
    main(args)