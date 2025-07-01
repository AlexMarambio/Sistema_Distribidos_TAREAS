FROM python:3.10-slim

RUN apt-get update && \
    pip install "elasticsearch<8.0.0" pymongo && \
    rm -rf /var/lib/apt/lists/*

ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$PATH:$HADOOP_HOME/bin
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app
COPY ../ /app

CMD ["bash", "elastic/wait.sh"]
