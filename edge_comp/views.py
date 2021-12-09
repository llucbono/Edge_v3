from django.shortcuts import render
from django.shortcuts import get_object_or_404
import json
# Create your views here.

from rest_framework import viewsets
from .models import Payload
from .serializers import PayloadSerializer
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

"""
    @action(detail=False, methods=['delete'])

    def sensor(self, request):
        if 'ip' not in request.query_params:
            queryset = Payload.objects.all()
            serializer = PayloadSerializer(queryset,many=True)
        else:
            ip = request.query_params['ip']
            queryset = Payload.objects.filter(ip=ip)
            serializer = PayloadSerializer(queryset,many=True)
        return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)

"""




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
