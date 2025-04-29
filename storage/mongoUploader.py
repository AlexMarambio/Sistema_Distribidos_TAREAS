from pymongo import MongoClient
import os

# URI de MongoDB Atlas (configurar bien)
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://joaquinsilva:eAIk2hvP0MXb9WpX@sisdis1.so1vzho.mongodb.net/?retryWrites=true&w=majority&appName=SisDis1")

client = MongoClient(MONGO_URI)
db = client["waze_alerts_db"]
alerts_collection = db["alerts"]

def insert_alerts(alert_list):
    if alert_list:
        alerts_collection.insert_many(alert_list)
        print(f"Se insertaron {len(alert_list)} alertas.")
    else:
        print("No hay alertas para insertar.")

def get_alerts(limit=100):
    return list(alerts_collection.find().limit(limit))
