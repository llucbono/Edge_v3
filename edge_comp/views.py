from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from .models import Payload
from .serializers import PayloadSerializer


class PayloadViewSet(viewsets.ModelViewSet):
    queryset = Payload.objects.all()
    serializer_class = PayloadSerializer
    permission_classes = []
