from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["waze-alerts"]
alerts_collection = db["alerts"]

def insert_alerts(alert_list):
    if alert_list:
        alerts_collection.insert_many(alert_list)
        print(f"Se insertaron {len(alert_list)} alertas.")
    else:
        print("No hay alertas para insertar.")

def get_alerts(limit=100):
    return list(alerts_collection.find().limit(limit))
