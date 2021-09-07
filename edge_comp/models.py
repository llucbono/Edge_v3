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
    payload_json = models.JSONField()
    sensor = models.IntegerField(choices=SENSORS,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)

