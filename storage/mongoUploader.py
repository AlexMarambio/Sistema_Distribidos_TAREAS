from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["waze-alerts"]
alerts_collection = db["alerts"]

def get_amount(min_datos=10000):
    client.admin.command("ping")
    cantidad = alerts_collection.estimated_document_count()
    print(f"\033[38;5;208mActualmente hay {cantidad} documentos\033[0m")
    if cantidad >= min_datos:
        print("\033[38;5;208mMongoDB listo con suficientes datos - Se cancela Scrapeo\033[0m")
        return False
    else:
        return True


def insert_alerts(alert_list):
    if alert_list:
        alerts_collection.insert_many(alert_list)
        print(f"Se insertaron {len(alert_list)} alertas.")
    else:
        print("No hay alertas para insertar.")

def get_alerts(limit=100):
    return list(alerts_collection.find().limit(limit))
