import random
import time
import os
import numpy as np
from pymongo import MongoClient

# Conexión a MongoDB local o Atlas
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/")
client = MongoClient(MONGO_URI)

db = client["waze-alerts"]
alerts_collection = db["alerts"]

# Función para obtener un evento aleatorio
def obtener_evento_aleatorio():
    count = alerts_collection.count_documents({})
    if count == 0:
        return None
    skip = random.randint(0, count - 1)
    return alerts_collection.find().skip(skip).limit(1)[0]

# Generador de tráfico
def generar_trafico(duracion_segundos=20, tasa_poisson=5, media_exponencial=1.0):
    tiempo_inicio = time.time()
    evento_id = 0

    print("Iniciando simulación de tráfico...\n")

    while (time.time() - tiempo_inicio) < duracion_segundos:
        modelo = random.choice(["poisson", "exponencial"])

        if modelo == "poisson":
            n = np.random.poisson(tasa_poisson)
            print(f"[Poisson] Generando {n} eventos")
            for _ in range(n):
                evento = obtener_evento_aleatorio()
                if evento:
                    print(f"Evento #{evento_id}: {evento.get('uuid', 'sin UUID')}")
                    evento_id += 1
        else:
            intervalo = np.random.exponential(media_exponencial)
            print(f"[Exponencial] Esperando {intervalo:.2f} segundos")
            time.sleep(intervalo)
            evento = obtener_evento_aleatorio()
            if evento:
                print(f"Evento #{evento_id}: {evento.get('uuid', 'sin UUID')}")
                evento_id += 1

        time.sleep(1)

    print(f"\nFinalizado. Se simularon {evento_id} eventos.")

if __name__ == "__main__":
    generar_trafico(duracion_segundos=30)
