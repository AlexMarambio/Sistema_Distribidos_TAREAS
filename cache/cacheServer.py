import redis
import json
import os

# Conexión a Redis
redis_client = redis.Redis(host=os.getenv("REDIS_HOST", "redis"), port=6379, db=0)

def get_from_cache(key):
    value = redis_client.get(key)
    if value:
        print(f"Cache hit para clave: {key}")
        return json.loads(value)
    else:
        print(f"Cache miss para clave: {key}")
        return None

def set_to_cache(key, value, ttl=60):
    redis_client.setex(key, ttl, json.dumps(value))
