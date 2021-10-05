from django.shortcuts import render
import json
# Create your views here.

from rest_framework import viewsets
from .models import Payload
from .serializers import PayloadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import request


# Make it from generic point of view
def sensor_validation(data):
    if data['payload_json']['type']=='BATDIMMER':
        msg=batdimmer_validation(data)
    elif data['payload_json']['type']=='BATMETER':
        msg=batmeter_validation(data)
    elif data['payload_json']['type']=='BATMETERTRI':
        msg=batmetertri_validation(data)
    elif data['payload_json']['type']=='BATPLUG':
        msg=batplug_validation(data)
    elif data['payload_json']['type']=='BATSENSE':
        msg=batsense_validation(data)
    elif data['payload_json']['type']=='BATSTREETLIGHT':
        msg=batstreetlight_validation(data)
    return msg

def batdimmer_validation(data):
    if not data['payload_json']['dimming']:
        msg="Missing Dimming value in Batdimmer with IP:"+str(data['payload_json']['ip'])
    elif int(data['payload_json']['dimming'])>100:
        msg="Dimming value out of range in Batdimmer with IP:"+str(data['payload_json']['ip'])
    else:
        msg= "Batdimmer OK"
    return msg
def batmeter_validation(data):
    msg= "HELLO"
    #if error 1 msg = 1000 code
    return msg
def batmetertri_validation(data):
    msg= "HELLO"
    #if error 1 msg = 1000 code
    return msg
def batplug_validation(data):
    msg= "HELLO"
    #if error 1 msg = 1000 code
    return msg
def batsense_validation(data):
    if not 0 <= int (data['payload_json']['values']['BAT']) <=4800:
        msg= "BAT value out of range of Batsense with IP:"+str(data['payload_json']['ip'])
    else:
        msg="Batsense OK"
    #if error 1 msg = 1000 code
    return msg
def batstreetlight_validation(data):
    if not 20 <= int (data['payload_json']['values']['TEMP']) <=60:
        msg= "TEMP value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
    #if error 1 msg = 1000 code
    elif not 0 <= int (data['payload_json']['values']['DIM']) <=100:
        msg= "DIM value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
    elif not 0 <= int (data['payload_json']['values']['LUM']) <=1023:
        msg= "LUM value out of range of batstreetlight with IP:"+str(data['payload_json']['ip'])
    else:
        msg="Batstreetlight OK"
    return msg

class PayloadViewSet(viewsets.ModelViewSet):
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer
    permission_classes = []


class PostView(APIView):

    def get(self, request, id=None):

        items = Payload.objects.all()
        serializer = PayloadSerializer(items, many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PayloadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            msg = sensor_validation(serializer.data)
            return Response(msg,status=status.HTTP_200_OK)
                #call function to check empty fields and ranges
            #return Response({ "alarm":"1000","data": serializer.data['payload_json']['dimming']}, status=status.HTTP_200_OK)
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
