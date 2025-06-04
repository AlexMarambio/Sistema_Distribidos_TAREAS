import csv
from pymongo import MongoClient
from datetime import datetime

def export_to_csv():
    client = MongoClient('mongodb://mongo:27017/')
    db = client['waze_alerts']
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
            if '_id' in doc_copy:
                del doc_copy['_id']
            if 'location' in doc_copy:
                doc_copy['location_x'] = doc_copy['location']['x']
                doc_copy['location_y'] = doc_copy['location']['y']
                del doc_copy['location']
            if 'pubMillis' in doc_copy:
                doc_copy['pubMillis'] = str(doc_copy['pubMillis'])
            
            writer.writerow(doc_copy)

if __name__ == '__main__':
    export_to_csv()
    print("CSV export completed successfully.")