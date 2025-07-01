from flask import Flask, request, jsonify
import redis
import json
import os
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Conexión a Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    db=0
)

# Conexión a Elasticsearch
es = Elasticsearch([os.getenv("ELASTIC_HOST", "http://elasticsearch:9200")])

@app.route('/cache/<key>', methods=['GET'])
def get_cache(key):
    value = redis_client.get(key)
    if value:
        app.logger.info(f"Cache hit para clave: {key}")
        return jsonify({"key": key, "value": json.loads(value), "hit": True})
    else:
        app.logger.info(f"Cache miss para clave: {key}")

        # Buscar en Elasticsearch por clave (por ejemplo, en el campo "id")
        try:
            es_response = es.search(index="tu_indice", body={
                "query": {
                    "match": {
                        "id": key  # o el campo que uses
                    }
                }
            })

            if es_response["hits"]["hits"]:
                first_result = es_response["hits"]["hits"][0]["_source"]
                # Cachear el resultado por 60 segundos
                redis_client.setex(key, 60, json.dumps(first_result))
                return jsonify({"key": key, "value": first_result, "hit": False})
            else:
                return jsonify({"key": key, "hit": False, "error": "No encontrado en Elasticsearch"}), 404

        except Exception as e:
            app.logger.error(f"Error al consultar Elasticsearch: {str(e)}")
            return jsonify({"error": "Error consultando Elasticsearch", "details": str(e)}), 500

@app.route('/cache/<key>', methods=['POST'])
def set_cache(key):
    data = request.get_json()
    ttl = data.get("ttl", 60)
    value = data.get("value")
    if value is None:
        return jsonify({"error": "No se proporcionó 'value'"}), 400
    redis_client.setex(key, ttl, json.dumps(value))
    app.logger.info(f"Set cache para {key} con TTL {ttl}")
    return jsonify({"key": key, "status": "set"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
