import requests
from requests.structures import CaseInsensitiveDict
from utility import Utility

class ApplicationInterface:        
    def __init__(self, url):
        self.uti = Utility()
        self.URL = url
        self.headers = CaseInsensitiveDict()
        self.headers["Content-Type"] = "application/json"
    
    def getDataFromID(self, ID):
        url= self.URL + "/" + str(ID)
        return self.get(url)

    def getListOfMessageFromDeviceIP(self, IP):
        url= self.URL + "/sensor/?ip=" + str(IP)
        return self.get(url)
    
    def getListOfMessageByDate(self, date):
        url= self.URL + "/offload/?date=" + str(date)
        return self.get(url)
    
    def getListOfMessageFromSensorType(self, typ):
        url= self.URL + "/sensor_type/?type=" + str(typ)
        return self.get(url)

    def getListOfMessageWithValidation(self, val):
        url= self.URL + "/valid_items/?valid=" + str(val)
        return self.get(url)
    
    def deleteDataFromID(self, ID):
        url= self.URL + "/" + str(ID)
        return self.delete(url)
    
    def deleteListOfMessageByDate(self, date):    
        url= self.URL + "/offload/?date=" + str(date)
        return self.delete(url)
    
    def postDataFromSingleDevice(self, ip: str, date: int, type: str, jsonfile: str):
        url = self.URL + "/"
        val = self.uti.getLocalData(jsonfile)
        DATA = {'ip':ip, 'date':date, 'type':type, 'values':val["values"]}
        json_object = self.uti.dumpData(DATA)
        return self.post(url, json_object)

    def postDataFromSingleDeviceDict(self, ip: str, date: int, type: str, dict: dict):
        url = self.URL + "/"
        try:
            DATA = {'ip':ip, 'date':date, 'type':type, 'values':dict["values"]}
            json_object = self.uti.dumpData(DATA)
            return self.post(url, json_object)
        except:
            print("[Error] - Dict must have the following form: {'values': [{'id': str, 'date': int, 'parameterId': str, 'value': any}]}")
            return None
        
    def postIP(self, ip: str, date: int, type: str, appname: str):
        url = self.URL + "/appIP/"
        dict = {'values': [{'id': "0", 'date': 0, 'parameterId': "0", 'value': appname}]}
        try:
            DATA = {'ip':ip, 'date':date, 'type':type, 'values':dict["values"]}
            json_object = self.uti.dumpData(DATA)
            return self.post(url, json_object)
        except:
            print("[Error] - Dict must have the following form: {'values': [{'id': str, 'date': int, 'parameterId': str, 'value': any}]}")
            return url
    
    def deleteAppIPbyName(self, name):
        url = self.URL + "/appIP/?type=" + name
        return self.delete(url)
    
    def getAppIPbyName(self, name):
        url = self.URL + "/appIP/?type=" + name
        return self.get(url)
    
    def postDataFromMultipleDevice(self, jsonfile):
        url = self.URL + "/multiple/"
        DATA = self.uti.getLocalData(jsonfile)
        json_object = self.uti.dumpData(DATA)
        return self.post(url, json_object)
    
    
    def post(self, url, json_object):
        try:
            resp = requests.post(url=url, headers=self.headers, data=json_object)
            if(resp.status_code in [204,200,201]):
                return resp.json()
            else:
                return None
        except Exception as inst:
            print("[Error] - ", type(inst))
            return None
        
    def delete(self, url):
        try:
            resp = requests.delete(url=url, headers=self.headers)
            if(resp.status_code in [204,200,201]):
                return resp.json()
            else:
                return None
        except Exception as inst:
            print("[Error] - ", type(inst))
            return None
        
    def get(self, url):
        try:
            resp = requests.get(url=url, headers=self.headers)
            if(resp.status_code in [204,200,201]):
                return resp.json()
            else:
                return None
        except Exception as inst:
            print("[Error] - ", type(inst))
            return None
    