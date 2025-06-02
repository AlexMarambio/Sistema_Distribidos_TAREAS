from elasticsearch import Elasticsearch
import os
import uuid

# URL del host de Elasticsearch
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

# Conexión al cliente de Elasticsearch
es = Elasticsearch(ES_HOST)

INDEX_NAME = "waze-alerts"

# Función para insertar alertas
def insert_alerts(alert_list):
    if alert_list:
        for alert in alert_list:
            alert_id = str(uuid.uuid4())
            es.index(index=INDEX_NAME, id=alert_id, document=alert)
        print(f"Se insertaron {len(alert_list)} alertas en Elasticsearch.")
    else:
        print("No hay alertas para insertar.")

# Función para obtener alertas
def get_alerts(limit=100):
    response = es.search(index=INDEX_NAME, size=limit, query={"match_all": {}})
    return [hit["_source"] for hit in response["hits"]["hits"]]
