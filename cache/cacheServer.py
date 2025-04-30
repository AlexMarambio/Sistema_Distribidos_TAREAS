from flask import Flask, request, jsonify
import redis
import json
import os

app = Flask(__name__)

# Conexión a Redis. Usamos "redis" como hostname porque en docker-compose 
# el servicio se llamará "redis".
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

@app.route('/cache/<key>', methods=['GET'])
def get_cache(key):
    value = redis_client.get(key)
    if value:
        app.logger.info(f"Cache hit para clave: {key}")
        # Decodifica el valor y retorna el objeto JSON
        return jsonify({"key": key, "value": json.loads(value), "hit": True})
    else:
        app.logger.info(f"Cache miss para clave: {key}")
        return jsonify({"key": key, "hit": False}), 404

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
