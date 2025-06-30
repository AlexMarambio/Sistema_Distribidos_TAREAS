import csv
import os
from pymongo import MongoClient, errors
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
CSV_FILE_PATH = "/data/waze_data.csv"
DB_NAME = "waze-alerts"
COLLECTION_NAME = "alerts"

def sanitize_document(doc, fieldnames):
    """
    Prepara un documento para escritura en CSV.
    - Elimina _id
    - Convierte listas y dicts en strings
    """
    sanitized = {}
    for field in fieldnames:
        value = doc.get(field, "")
        if isinstance(value, (dict, list)):
            sanitized[field] = str(value)
        else:
            sanitized[field] = value
    return sanitized

def export_to_csv():
    try:
        # Conexión a MongoDB
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.server_info()  # Fuerza verificación de conexión
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]

        # Obtener todos los documentos
        documents = list(collection.find())
        if not documents:
            print("La colección está vacía. No se exportará nada.")
            return

        # Determinar todos los campos presentes
        fieldnames = set()
        for doc in documents:
            fieldnames.update(doc.keys())
        fieldnames.discard("_id")
        fieldnames = list(fieldnames)

        # Escribir CSV
        with open(CSV_FILE_PATH, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for doc in documents:
                sanitized = sanitize_document(doc, fieldnames)
                writer.writerow(sanitized)

        print(f"\n✅ Exportación completada: {CSV_FILE_PATH}")

    except errors.ServerSelectionTimeoutError:
        print("❌ Error: No se pudo conectar a MongoDB. Revisa MONGO_URI o que el servicio esté en ejecución.")
    except errors.PyMongoError as e:
        print(f"❌ Error de MongoDB: {e}")
    except IOError as e:
        print(f"❌ Error al escribir el archivo CSV: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    export_to_csv()
