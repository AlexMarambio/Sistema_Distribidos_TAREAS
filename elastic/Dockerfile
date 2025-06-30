FROM python:3.10-slim

RUN apt-get update && \
    pip install elasticsearch pymongo && \
    rm -rf /var/lib/apt/lists/*

ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin

WORKDIR /app
COPY ../ /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["bash", "-c", "python elastic/mongo_to_elastic.py && python elastic/hdfs_to_elastic.py"]
