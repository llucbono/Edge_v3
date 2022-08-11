import argparse
import time
from tqdm import tqdm

from utility import Utility
from appInterface import ApplicationInterface # To access to the API

URL = "http://192.168.0.219:8000/ec/payloads"
NB_REQUEST = 1

uti = Utility()
interface = ApplicationInterface(URL)

def main(args):
    lst_getDataNodeById = []; lst_getMessageByIP = []; lst_getMessageDate = []
    lst_getMessageType = []; lst_sendNodeData = []; lst_getMessageByVal = []
    lst_deleteFromID = []; lst_deleteFromDate = []; lst_sendMultipleData = []
    lst_request = []

    count = 0
    pbar = tqdm(total=NB_REQUEST)
    while(count < NB_REQUEST):
        if(args.v == 1): print("[+] Request : " + str(count))

        st = time.time()
        interface.postDataFromSingleDevice("192.168.56.1", 9082022, "testType", "data.json")
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_sendNodeData.append(ed - st)

        st = time.time()
        interface.postDataFromMultipleDevice("datamul.json")
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_sendMultipleData.append(ed - st)

        st = time.time()
        interface.getDataFromID(150)
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getDataNodeById.append(ed - st)

        st = time.time()
        interface.getListOfMessageWithValidation(True)
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getMessageByVal.append(ed - st)

        st = time.time()
        interface.deleteDataFromID(150)
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_deleteFromID.append(ed - st)

        st = time.time()
        interface.deleteListOfMessageByDate(13021999) # get test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_deleteFromDate.append(ed - st)

        st = time.time()
        interface.getListOfMessageFromDeviceIP("69.69.69.69") # send test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getMessageByIP.append(ed - st)

        st = time.time()
        interface.getListOfMessageByDate("13021999") # send test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getMessageDate.append(ed - st)

        st = time.time()
        interface.getListOfMessageFromSensorType("testType") # send test
        ed = time.time()
        if(args.v == 1): print("     Time elapsed : " + str(ed - st))
        lst_getMessageType.append(ed - st)

        lst_request.append(count)
        count += 1
        pbar.update(1)
    pbar.close()

    uti.plotResponseTime(NB_REQUEST, lst_request, lst_getDataNodeById, "getDataById")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_getMessageByIP, "getMessageByIP")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_getMessageDate, "getMessageByDate")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_getMessageType, "getMessageByType")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_getMessageByVal, "getMessageByValidation")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_sendNodeData, "postDataSingleDevice")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_sendMultipleData, "postDataMutipleDevice")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_deleteFromID, "deleteFromID")
    uti.plotResponseTime(NB_REQUEST, lst_request, lst_deleteFromDate, "deleteFromDate")

    uti.plotAllResponseTime()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process args for edge computing project")
    parser.add_argument("--v", help="Verbose (0/1)", type=int, default=0)
    args = parser.parse_args()
    main(args)
