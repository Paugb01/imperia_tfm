FROM python:3.9-slim

RUN pip install apache-beam[gcp] google-cloud-storage google-cloud-bigquery

COPY pipeline.py /app/pipeline.py

ENTRYPOINT ["python", "/app/pipeline.py"]

