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
    
    def postDataFromMultipleDevice(self, jsonfile):
        url = self.URL + "/multiple/"
        DATA = self.uti.getLocalData(jsonfile)
        json_object = self.uti.dumpData(DATA)
        return self.post(url, json_object)
    
    
    def post(self, url, json_object):
        resp = requests.post(url=url, headers=self.headers, data=json_object)
        if(resp.status_code in [204,200,201]):
            return resp.content
        else:
            return None
        
    def delete(self, url):
        resp = requests.delete(url=url, headers=self.headers)
        if(resp.status_code in [204,200,201]):
            return resp.content
        else:
            return None
        
    def get(self, url):
        resp = requests.get(url=url, headers=self.headers)
        if(resp.status_code in [204,200,201]):
            return resp.content
        else:
            return None