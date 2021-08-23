from rest_framework import serializers
from .models import Payload



class PayloadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payload
        fields = ['id', 'payload_json', 'sensor', 'created']
