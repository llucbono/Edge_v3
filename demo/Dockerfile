FROM python:3.8

RUN apt-get update
RUN pip install flask flask-restful numpy pandas darts
RUN mkdir /app
COPY ./demoAppPrediction.py /app/demoAppPrediction.py

CMD python /app/demoAppPrediction.py 