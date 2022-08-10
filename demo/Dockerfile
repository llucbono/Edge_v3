FROM python:3.8

RUN apt-get update
RUN pip install flask flask-restful numpy pandas darts

WORKDIR /usr/src/app

COPY . .

CMD python demoAppPrediction.py 