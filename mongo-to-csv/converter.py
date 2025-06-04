import csv
from pymongo import MongoClient
from datetime import datetime
import os

MONGO_URI = os.getenv("MONGO_URI")

def export_to_csv():
    client = MongoClient(MONGO_URI)
    db = client['waze-alerts']
    collection = db['alerts']
    
    documents = collection.find()
    
    # Define CSV file path
    csv_file = '/data/waze_alerts.csv'
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        # Get fieldnames from the first document
        fieldnames = set()
        for doc in documents:
            fieldnames.update(doc.keys())
        fieldnames = list(fieldnames)
        
        if '_id' in fieldnames:
            fieldnames.remove('_id')
        
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        
        for doc in documents:
            doc_copy = doc.copy()
            print(f"PARSING doc: {doc_copy['_id']}")
            if '_id' in doc_copy:
                del doc_copy['_id']
            
            writer.writerow(doc_copy)

if __name__ == '__main__':
    export_to_csv()
    print("CSV export completed successfully.")