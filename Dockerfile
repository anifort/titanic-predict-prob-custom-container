FROM python:3.7.5-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./model.joblib /app/model.joblib
COPY ./prediction-service.py /app/prediction-service.py

ENV FLASK_APP=/app/prediction-service.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000
ENV FLASK_DEBUG=1

ENTRYPOINT ["flask", "run"]