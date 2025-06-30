FROM python:3.9-slim

WORKDIR /app

RUN pip install pymongo pandas

COPY converter.py .

CMD ["python", "converter.py"]