from storage.esUploader import get_alerts
import json
import sys
import os
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, ROOT_DIR)


from storage.esUploader import get_alerts


output_path = "pig/alerts.json"

data = get_alerts(limit=10000)

with open(output_path, 'w') as f:
    for alert in data:
        json.dump(alert, f)
        f.write('\n')

print(f"Exportadas {len(data)} alertas a {output_path}")
