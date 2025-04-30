from pymongo import MongoClient
import os

# URI de MongoDB Atlas (configurar bien)
MONGO_URI = os.getenv("MONGO_URI")

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client["waze-alerts"]
alerts_collection = db["alerts"]

# Función para insertar alertas
def insert_alerts(alert_list):
    if alert_list:
        alerts_collection.insert_many(alert_list)
        print(f"Se insertaron {len(alert_list)} alertas.")
    else:
        print("No hay alertas para insertar.")

# Función para obtener alertas
def get_alerts(limit=100):
    return list(alerts_collection.find().limit(limit))
