FROM python:3.10-slim

WORKDIR /app

COPY trafficGenerator.py .

RUN pip install pymongo numpy

CMD ["python", "trafficGenerator.py"]
