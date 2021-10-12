from rest_framework import serializers
from .models import Payload, SENSORS



class PayloadSerializer(serializers.ModelSerializer):
    valid = serializers.BooleanField(default= True)
    class Meta:
        model = Payload
        fields = ['id', 'payload_json', 'sensor', 'created','valid']

#LOGIC FUNCTIONS TO DEVELOP FOR MAINTENANCE TASKS
"""
def batdimmer_validation(p):
    if int(p['dimming'])>100:
        raise serializers.ValidationError('Dimming Value out of range')
    elif not p['ip']:
        raise serializers.ValidationError('IP field is empty')
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return

def batmeter_validation(p):
    if not p['ip']:
        raise serializers.ValidationError('IP field is empty')
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return


def batmetertri_validation(p):
    if not p['ip']:
        raise serializers.ValidationError('IP field is empty')
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return


def batplug_validation(p):
    if not p['ip']:
        print("IP ERROR")
        raise serializers.ValidationError('IP field is empty, ID is '+str(p['id']))
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return

def batsense_validation(p):
    if not p['ip']:
        raise serializers.ValidationError('IP field is empty')
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return

def batstreetlight_validation(p):
    if not p['ip']:
        raise serializers.ValidationError('IP field is empty')
    elif not p['id']:
        raise serializers.ValidationError('ID field is empty')
    return
"""
"""
    def validate_payload_json(self, value):
        if value['type']=='BATDIMMER':
            print("this is Batdimmer!")
            batdimmer_validation(value)
        elif value['type']=='BATMETER':
            print("this is Batmeter!")
            batmeter_validation(value)
        elif value['type']=='BATMETERTRI':
            print("this is Batmetertri!")
            batmetertri_validation(value)
        elif value['type']=='BATPLUG':
            print("this is Batplug!")
            batplug_validation(value)
        elif value['type']=='BATSENSE':
            print("this is Batsense!")
            batsense_validation(value)
        elif value['type']=='BATSTREETLIGHT':
            print("this is Batstreetlight!")
            batstreetlight_validation(value)
        return value
"""

