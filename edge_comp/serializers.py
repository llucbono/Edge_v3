from rest_framework import serializers
from .models import Payload, SENSORS



class PayloadSerializer(serializers.ModelSerializer):
    valid = serializers.BooleanField(default= True)
    class Meta:
        model = Payload
        fields = ['id', 'payload_json', 'sensor', 'created','valid']



