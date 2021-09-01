
from rest_framework.test import APITestCase
from edge_comp.models import Payload, SENSORS
from edge_comp.serializers import PayloadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import request
import datetime


class PayloadsTests(APITestCase):


    def setUp(self):
        pass


    def test_fracaso(self):
        assert False

    def test_expected_serialized_json(self):

        expected_results = {"id":2,"payload_json":{
                "id": "ip+timestamp",
                "ip": "ip",
                "type": "BATPLUG",
                "date": "date",
                "values" :
                        {
                    "state":0,
                    "meter":
                     {
                      "UL": 1,
                      "IL": 1,
                      "PACT": 1,
                      "PAPP": 1,
                      "EACT": 1,
                    "EAPP": 1
                             }}
                        }, "sensor":1,
                        'created': str(datetime.datetime.now())
                    }

        payload = Payload(**expected_results)

        print(payload)

        results = PayloadSerializer(payload).data

        assert results == expected_results




