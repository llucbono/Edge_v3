from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
# Create your views here.

from rest_framework import viewsets
from .models import Payload, AppData
from .serializers import PayloadSerializer, AppDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import request
from django.http import JsonResponse
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action

# Make it from generic point of view
def sensor_validation(data):
    msg= "OK"
    bol=True
    """
    if data['payload_json']['type']=='BATDIMMER':
        msg, bol =batdimmer_validation(data)
    elif data['payload_json']['type']=='BATMETER':
        msg, bol =batmeter_validation(data)
    elif data['payload_json']['type']=='BATMETERTRI':
        msg, bol =batmetertri_validation(data)
    elif data['payload_json']['type']=='BATPLUG':
        msg, bol =batplug_validation(data)
    elif data['payload_json']['type']=='BATSENSE':
        msg, bol =batsense_validation(data)
    elif data['payload_json']['type']=='BATSTREETLIGHT':
        msg, bol=batstreetlight_validation(data)
    """
    return msg, bol

def batdimmer_validation(data):
    if not data['payload_json']['dimming']:
        msg="Missing Dimming value in Batdimmer with IP:"+str(data['payload_json']['ip'])
        bol=False
    elif int(data['payload_json']['dimming'])>100:
        msg="Dimming value out of range in Batdimmer with IP:"+str(data['payload_json']['ip'])
        bol=False
    else:
        msg= "Batdimmer OK"
        bol=True
    return msg, bol

def batmeter_validation(data):
    msg= "HELLO"
    bol=True
    #if error 1 msg = 1000 code
    return msg, bol

def batmetertri_validation(data):
    msg= "HELLO"
    bol=True
    #if error 1 msg = 1000 code
    return msg, bol

def batplug_validation(data):
    #if error 1 msg = 1000 code
    msg="HELLO"
    bol=True
    return msg, bol

def batsense_validation(data):
    if not 0 <= int (data['payload_json']['values']['BAT']) <=4800:
        msg= "BAT value out of range of Batsense with IP:"+str(data['payload_json']['ip'])
        bol=False
    else:
        msg="Batsense OK"
        bol=True
    #if error 1 msg = 1000 code
    return msg, bol

def batstreetlight_validation(data):

    if not 20 <= int (data['payload_json']['values']['TEMP']) <=60:
        msg= "TEMP value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
        bol=False
    #if error 1 msg = 1000 code
    elif not 0 <= int (data['payload_json']['values']['DIM']) <=100:
        msg= "DIM value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
        bol=False
    elif not 0 <= int (data['payload_json']['values']['LUM']) <=1023:
        msg= "LUM value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
        bol=False
    else:
        msg="Batstreetlight OK"
        bol=True
    return msg, bol

class AppDataViewSet(viewsets.ModelViewSet):
    queryset = AppData.objects.all()
    serializer_class = AppDataSerializer

    @action(detail=False, methods=['post','get','delete'])
    def appUse(self, request):
        if request.method=='GET':
            if 'type' not in request.query_params:
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                name = request.query_params['type']
                print('ASK FOR USE OF:',name)
                queryset = AppData.objects.filter(type='appUse')
                serializer = AppDataSerializer(queryset,many=True)
                for elem in serializer.data:
                    if(elem['values'][0]['value']["APPNAME"]==name):
                        cpu = elem['values'][0]['value']["CPU"]
                        ram = elem['values'][0]['value']["RAM"]
                        return Response({"status": "success", "data": (cpu, ram)}, status=status.HTTP_200_OK)
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method=='POST':
            serializer = AppDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                _appIP = serializer.data['ip']
                _appName = serializer.data['values'][0]['value']
                print('APP DATA:', _appName)
                print('APP IP RECEIVED:', _appIP)
                
                return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)

        elif request.method=='DELETE':
            name = request.query_params['type']
            print('DELETING APP:',name)
            queryset = AppData.objects.filter(type='appUse')
            if queryset.count() > 0:
                queryset.delete()
                return Response({"status": "success", "data": "Item Deleted"},status=status.HTTP_200_OK)
        
        else:
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['post','get','delete'])
    def appIP(self, request):
        # TO GET THE IP OF AN APOP GIVEN ITS NAME
        if request.method=='GET':
            if 'type' not in request.query_params:
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                name = request.query_params['type']
                print('ASK FOR IP OF:',name)
                queryset = AppData.objects.filter(type='appIP')
                serializer = AppDataSerializer(queryset,many=True)
                for elem in serializer.data:
                    if(elem['values'][0]['value']==name):
                        return Response({"status": "success", "data": elem['ip']}, status=status.HTTP_200_OK)
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        # FOR THE APP TO POST THEIR IP ON START
        elif request.method=='POST':
            serializer = AppDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                _appIP = serializer.data['ip']
                _appName = serializer.data['values'][0]['value']
                print('APP DATA:', _appName)
                print('APP IP RECEIVED:', _appIP)
                
                return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)

        # FOR THE APP TO REMOVE THEY IP FROM THE DATABASE
        elif request.method=='DELETE':
            name = request.query_params['type']
            print('DELETING APP:',name)
            queryset = AppData.objects.filter(type='appIP')
            if queryset.count() > 0:
                queryset.delete()
                return Response({"status": "success", "data": "Item Deleted"},status=status.HTTP_200_OK)
        
        else:
            #test how to read values from serializer data for ranges
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post','get','delete'])
    def appModel(self, request):
        # TO GET THE AI MODEL 
        if request.method=='GET':
            if 'type' not in request.query_params:
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                ipasked = request.query_params['type']
                print('ASK FOR MODEL OF:', ipasked)
                queryset = AppData.objects.filter(type='model_struct')
                queryset2 = AppData.objects.filter(type='model_weight')
                serializer = AppDataSerializer(queryset,many=True)
                serializer2 = AppDataSerializer(queryset2,many=True)
                for elem_struct in serializer.data:
                    if(elem_struct["ip"]== ipasked):
                        struct = elem_struct['values'][0]['value']
                for elem_weight in serializer2.data:
                    if(elem_weight["ip"]== ipasked):
                        weight = elem_weight['values'][0]['value']
                if(struct != None and weight != None):
                    return Response({"status": "success", "data": (struct, weight)}, status=status.HTTP_200_OK)
                return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)

        # FOR THE APP TO POST THEIR TRAINED AI MODEL
        elif request.method=='POST':
            serializer = AppDataSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                _appIP = serializer.data['ip']
                _appName = serializer.data['values'][0]['value']
                print('APP IP RECEIVED:', _appIP)
                print('APP MODEL:', _appName)
                return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
                    #call function to check empty fields and ranges
                    
        # FOR THE APP TO REMOVE THE AI TRAINED MODEL
        elif request.method=='DELETE':
            typee = request.query_params['type']
            print('DELETING MODEL:', typee)
            if(typee=='model_struct'):
                queryset1 = AppData.objects.filter(type='model_struct')
            elif(typee=='model_weight'):
                queryset2 = AppData.objects.filter(type='model_weight')
            if queryset1.count() > 0:
                queryset1.delete()                
                return Response({"status": "success", "data": "Item Deleted"},status=status.HTTP_200_OK)
            elif queryset2.count() > 0:
                queryset2.delete()
                return Response({"status": "success", "data": "Item Deleted"},status=status.HTTP_200_OK)
        
        else:
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = []

class PayloadViewSet(viewsets.ModelViewSet):
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer

    @action(detail=False, methods=['post'])

    def multiple(self, request):
        serializer = PayloadSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data},status=status.HTTP_200_OK)
                #call function to check empty fields and ranges
        else:
            #test how to read values from serializer data for ranges
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])

    def valid_items(self, request):
        if 'valid' not in request.query_params:
            queryset = Payload.objects.all()
            serializer = PayloadSerializer(queryset,many=True)
        else:
            valid = request.query_params['valid']
            queryset = Payload.objects.filter(valid=valid)
            serializer = PayloadSerializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])

    def sensor_type(self, request):
        if 'type' not in request.query_params:
            queryset = Payload.objects.all()
            serializer = PayloadSerializer(queryset,many=True)
        else:
            type = request.query_params['type']
            queryset = Payload.objects.filter(type=type)
            serializer = PayloadSerializer(queryset,many=True)
            
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get','delete'])

    def offload(self, request):
        if request.method=='GET':
            if 'date' not in request.query_params:
                queryset = Payload.objects.all()
                serializer = PayloadSerializer(queryset,many=True)
            else:
                date = request.query_params['date']
                queryset = Payload.objects.filter(date=date)
                serializer = PayloadSerializer(queryset,many=True)
                if queryset.count()>0:
                    return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)

        elif request.method=='DELETE':
            date = request.query_params['date']
            queryset = Payload.objects.filter(date=date)
            if queryset.count() > 0:
                queryset.delete()
                return Response({"status": "success", "data": "Item Deleted"},status=status.HTTP_200_OK)
        return Response({"status": "fail", "data": "Item not found"}, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['delete'])
    def all(self, request):
        print("Delete all")
        if request.method=='DELETE':
            queryset = Payload.objects.all()
            if queryset.count() > 0:
                queryset.delete()
                return Response({"status": "success", "data": "All item deleted"},status=status.HTTP_200_OK)
        return Response({"status": "fail", "data": "No item at all"}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def sensor(self, request):
        if 'ip' not in request.query_params:
            queryset = Payload.objects.all()
            serializer = PayloadSerializer(queryset,many=True)
        else:
            ip = request.query_params['ip']
            queryset = Payload.objects.filter(ip=ip)
            serializer = PayloadSerializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    permission_classes = []


class PostView(APIView):

    def get(self, request):
        if 'valid' not in request.query_params:
            queryset = Payload.objects.all()
            serializer = PayloadSerializer(queryset,many=True)
        else:
            valid = request.query_params['valid']
            queryset = Payload.objects.filter(valid=valid)
            serializer = PayloadSerializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = PayloadSerializer(data=request.data)
        if serializer.is_valid():
            msg, bol = sensor_validation(serializer.validated_data)
            serializer.validated_data['valid']=bol
            serializer.save()

            return Response(msg,status=status.HTTP_200_OK)
                #call function to check empty fields and ranges
        else:
            #test how to read values from serializer data for ranges
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        item = Payload.objects.get(id=id)
        serializer = PayloadSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        item = get_object_or_404(Payload, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

    permission_classes = []


class ServerView(APIView):

    def get(self, request):
        id = request.query_params.get('id', None)
        if id is not None:
            queryset = Payload.objects.filter(id=id)
        else:
            queryset = Payload.objects.all()
        serializer = PayloadSerializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)


    def post(self, request):
        serializer = PayloadSerializer(data=request.data,many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
                #call function to check empty fields and ranges
        else:
            #test how to read values from serializer data for ranges
            return Response({"data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        item = Payload.objects.get(id=id)
        serializer = PayloadSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        item = get_object_or_404(Payload, id=id)
        item.delete()
        return Response({"status": "success", "data": "Item Deleted"})

    def delete(self, request):
        if 'date' in request.query_params:
            date = request.query_params['date']
            payloads = Payload.objects.filter(date=date)
            if payloads.count() > 0:
                payloads.delete()
                return Response("Femails deleted", status=status.HTTP_204_NO_CONTENT)
        return Response("Unable to find the femails.", status=status.HTTP_400_BAD_REQUEST)

    permission_classes = []
