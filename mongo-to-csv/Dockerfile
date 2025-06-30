FROM python:3.9-slim

WORKDIR /app
COPY ../ /app

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN pip install pymongo pandas

CMD ["python", "mongo-to-csv/converter.py"]