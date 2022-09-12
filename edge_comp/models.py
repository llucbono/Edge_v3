from django.db import models

# Create your models here.


SENSORS = [
    (1, 'BATDIMMER'),
    (2, 'BATMETER'),
    (3, 'BATMETERTRI'),
    (4, 'BATPLUG'),
    (5, 'BATSENSE'),
    (6, 'BATSTREETLIGHT'),
]

SENSORS_2=['BATDIMMER','BATMETER','BATMETERTRI','BATPLUG','BATSENSE','BATSTREETLIGHT']

class Payload(models.Model):
    #payload_json = models.JSONField()
    #sensor = models.IntegerField(choices=SENSORS,null=True,blank=True)
    #item_id = models.AutoField(primary_key=True)
    created = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(null=False)
    ip = models.CharField(max_length=200,default='0')
    type = models.CharField(max_length=200,default='BatPlug')
    date = models.BigIntegerField(default=0)
    values = models.JSONField()


class AppData(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(null=False)
    ip = models.CharField(max_length=200,default='0')
    type = models.CharField(max_length=200,default='BatPlug')
    date = models.BigIntegerField(default=0)
    values = models.JSONField()

"""
TODO:

Add id field
type as sensor:


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
