#  API EC

## Introduction

This API aims to facilitate communication between the different entities in an IoT
architecture. It provides a generic data schema for any type of sensor and methods
to exchange data according to pre-established protocols.
In addition, all the necessary resources for its execution are included in the directory,
as well as a Dockerfile that allows the application to be deployed directly on any
machine after installing Docker.

## Installation
The execution of this application only requires the download of the directory and its
execution via Docker Compose.
So once you have made sure that Docker is installed on the machine where it is to
be run, simply run the two following command in the terminal:
```
docker-compose -f local.yml build
docker-compose -f local.yml up
```
To call the API via any **Python** program you should use the following interface: https://github.com/jbaudru/RESTful-app-and-interface/blob/main/appInterface.py

The documentation of the interface is available here: https://github.com/jbaudru/RESTful-app-and-interface/blob/main/Interface%20Documentation.pdf  

## Scheme
The scheme of this API only contains one generic model. This model aims to
represent any instance of data for an individual sensor. Therefore, the specific values
that are case-dependent (parameters of the specific sensor) are contained in the
field Values.

## Tutorial 
You can find a use case of the API with an example of application via this link : https://github.com/jbaudru/RESTful-app-and-interface

In this example, it is about an application sending random data to the API and another one making predictions on the data received by the API.

## Methods
Several methods are initially proposed and try to capture the main uses of these applications
in this context. Therefore, there are methods for: posting data (single or multiple; getting data
(single or multiple, as well as generic queries); deleting data (single or multiple) in order to
empty the database when the data is no longer needed on that device

### Example of POST
```
curl --request POST \
--url http://localhost:8000/ec/payloads \
--header 'Content-Type: application/json' \
--data '{
"ip": "b216::1a10:4e00:501:15",
"date": 1637678232454,
"type": "BatSense",
"values": [
{
"id": "b216::1a10:4e00:501:14-PAPP1637678232454",
"date": 1637678232454,
"parameterId": "b216::1a10:4e00:501:14-PAPP",
"value": 0
}]
```

### Example of GET
```
curl --request GET \
--url http://localhost:8000/ec/payloads/1 \
--header 'Content-Type: application/json'
```