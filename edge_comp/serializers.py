from rest_framework import serializers
from .models import Payload, SENSORS



class PayloadSerializer(serializers.ModelSerializer):
    valid = serializers.BooleanField(default= True)
    class Meta:
        model = Payload
        fields = ['ip','date', 'type', 'created','valid','values']



"""
---BatPlug---
{
"id":"b216::1a10:4e00:501:14",
"date":1637678232454,
"type":"BatPlug",
"values":[
{"id":"b216::1a10:4e00:501:14-PAPP1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-PAPP","value":0.0},
{"id":"b216::1a10:4e00:501:14-EAPP1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-EAPP","value":417.0},
{"id":"b216::1a10:4e00:501:14-PACT1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-PACT","value":0.0},
{"id":"b216::1a10:4e00:501:14-IL1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-IL","value":0.0},
{"id":"b216::1a10:4e00:501:14-UL1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-UL","value":229.0},
{"id":"b216::1a10:4e00:501:14-EACT1637678232454","date":1637678232454,"parameterId":"b216::1a10:4e00:501:14-EACT","value":141.0}
]
}

"""
