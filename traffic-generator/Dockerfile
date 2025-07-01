# traffic-generator/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY ../ /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "traffic-generator/trafficGenerator.py"]
