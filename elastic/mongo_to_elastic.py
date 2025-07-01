from pymongo import MongoClient
from elasticsearch import Elasticsearch
import os

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "waze-alerts"
COLLECTION_NAME = "alerts"

ES_HOST = os.getenv("ELASTIC_HOST", "https://es01:9200")
ES_USER = os.getenv("ELASTIC_USER", "elastic")
ES_PASS = os.getenv("ELASTIC_PASSWORD", "changeme")

# Conexiones
mongo_client = MongoClient(MONGO_URI)
collection = mongo_client[DB_NAME][COLLECTION_NAME]

es = Elasticsearch(
    ES_HOST,
    http_auth=(ES_USER, ES_PASS),
    verify_certs=False  # o True con certificados configurados correctamente
)

# Envío de documentos sucios a índice "raw_alerts"
for doc in collection.find():
    doc_id = str(doc.get("_id"))
    doc.pop("_id", None)
    es.index(index="raw_alerts", id=doc_id, document=doc)

print("✅ Datos sucios enviados a Elasticsearch (raw_alerts)")
