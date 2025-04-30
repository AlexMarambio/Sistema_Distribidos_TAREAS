# traffic-generator/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY trafficGenerator.py .

ENV PYTHONUNBUFFERED=1

# Agrega requests aquí
RUN pip install pymongo numpy requests

CMD ["python", "trafficGenerator.py"]
