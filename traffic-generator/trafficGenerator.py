import random
import time
import os
import numpy as np
import requests
from pymongo import MongoClient
from storage.mongoUploader import esperar_mongodb

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)
db = client["waze-alerts"]
alerts_collection = db["alerts"]

# Cache API
CACHE_URI = os.getenv("CACHE_URI", "http://cache:5000/cache")

def serializar_evento(evento):
    if "_id" in evento:
        evento["_id"] = str(evento["_id"])
    return evento

# Interacción con el servidor de caché
def get_from_cache(uuid):
    try:
        r = requests.get(f"{CACHE_URI}/{uuid}")
        if r.status_code == 200:
            print(f"Cache hit para evento {uuid}")
            return r.json()["value"]
        else:
            print(f"Cache miss para evento {uuid}")
            return None
    except requests.RequestException as e:
        print(f"Error al conectar con caché: {e}")
        return None

def set_to_cache(uuid, evento, ttl=60):
    try:
        r = requests.post(f"{CACHE_URI}/{uuid}", json={"value": evento, "ttl": ttl})
        if r.status_code == 201:
            print(f"Evento {uuid} almacenado en caché")
    except requests.RequestException as e:
        print(f"Error al guardar en caché: {e}")

# Función para obtener un evento aleatorio (de MongoDB)
def obtener_evento_aleatorio():
    count = alerts_collection.count_documents({})
    if count == 0:
        return None
    skip = random.randint(0, count - 1)
    return alerts_collection.find().skip(skip).limit(1)[0]


# Generador de tráfico con cache
def generar_trafico(duracion_segundos=20, tasa_poisson=5, media_exponencial=1.0):
    tiempo_inicio = time.time()
    evento_id = 0
    miss = 0

    print("Iniciando simulación de tráfico...\n")

    while (time.time() - tiempo_inicio) < duracion_segundos:
        modelo = random.choice(["poisson", "exponencial"])

        if modelo == "poisson":
            n = np.random.poisson(tasa_poisson)
            print(f"[Poisson] Generando {n} eventos")
            for _ in range(n):
                evento = obtener_evento_aleatorio()
                if evento:
                    uuid = evento.get("uuid", f"sin-uuid-{evento_id}")
                    reportBy = evento.get("reportBy", f"sin-reportBy-{evento_id}")
                    street = evento.get("street", f"sin-street-{evento_id}")
                    cached = get_from_cache(uuid)
                    if not cached:
                        set_to_cache(uuid, serializar_evento(evento))
                        miss +=1
                    print(f"Evento #{evento_id}: \033[38;5;93m{uuid}, \033[38;5;213m{reportBy}, \033[35m{street}\033[0m")
                    evento_id += 1
        else:
            intervalo = np.random.exponential(media_exponencial)
            print(f"[Exponencial] Esperando {intervalo:.2f} segundos")
            time.sleep(intervalo)
            evento = obtener_evento_aleatorio()
            if evento:
                uuid = evento.get("uuid", f"sin-uuid-{evento_id}")
                reportBy = evento.get("reportBy", f"sin-reportBy-{evento_id}")
                street = evento.get("street", f"sin-street-{evento_id}")
                cached = get_from_cache(uuid)
                if not cached:
                    set_to_cache(uuid, serializar_evento(evento))
                    miss +=1
                print(f"Evento #{evento_id}: \033[32;5;93m{uuid}, \033[32;5;213m{reportBy}, \033[31m{street}\033[0m")
                evento_id += 1

        time.sleep(2)

    print(f"\nFinalizado. Se simularon {evento_id} eventos.")
    print(f"\033[38;5;208mHitRate: {((evento_id-miss)/evento_id)*100}%\033[0m")

if __name__ == "__main__":
    esperar_mongodb(60000)
    generar_trafico(duracion_segundos=120)
