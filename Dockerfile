FROM python:3.7.5-slim

RUN pip install --upgrade pip

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# We could pack the container with the model but we want to have a more
# generic implementation where the user passes the model gs:// uri as a parameter
# during startup
# COPY ./model.joblib /app/model.joblib 
COPY ./prediction-service.py /app/prediction-service.py

ENTRYPOINT ["python", "/app/prediction-service.py"]