# cache/Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY cacheElastic.py .

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir flask redis

CMD ["python", "cacheElastic.py"]
