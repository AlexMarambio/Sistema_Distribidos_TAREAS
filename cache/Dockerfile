# cache/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY cacheServer.py .
RUN pip install redis
CMD ["python", "cacheServer.py"]
