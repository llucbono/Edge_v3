from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Payload
from .serializers import PayloadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import request


class PayloadViewSet(viewsets.ModelViewSet):
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer
    permission_classes = []

class PostView(viewsets.ModelViewSet):

    serializer_class = PayloadSerializer

    def post(self, request, format=None):
        serializer = PayloadSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes = []
