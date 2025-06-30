import requests
import time
import os
from storage.mongoUploader import insert_alerts  # Importa la función de inserción de Mongo
from storage.mongoUploader import get_alerts
from storage.mongoUploader import get_amount

# Bounding boxes
BOUNDING_BOXES = [
    (-33.4188559, -33.5792955, -70.7085688, -70.5392420),
    (-33.4135807, -33.5740302, -70.8267516, -70.6574248),
    (-33.3332676, -33.4938655, -70.7789843, -70.6096575),
    (-33.3353337, -33.4959278, -70.6478988, -70.4785720),
]

# Función para obtener alertas de la API
def obtain_alerts(b, l, t, r):
    url = f"https://www.waze.com/live-map/api/georss?bottom={b}&left={l}&top={t}&right={r}&env=row&types=alerts,traffic"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("alerts", [])
    else:
        print(f"\033[91mError {response.status_code} al obtener: {url}\033[0m")
        return []

# Función principal
def main():
    not_ready = True
    total_alerts = 0
    box_index = 0

    not_ready = get_amount(60000)
# Cambiar numeros antes de enviar la tarea 3 60000 dbería bastar
    while total_alerts < 60000 and not_ready:
        t, b, l, r = BOUNDING_BOXES[box_index]
        alerts = obtain_alerts(b, l, t, r)

        filtered_alerts = [{k: v for k, v in alert.items() if k != "comments"} for alert in alerts]
        insert_alerts(filtered_alerts)
        total_alerts += len(alerts)

        print(f"\033[96m[{box_index}] Acumulado: {total_alerts} alertas.\033[0m")
        box_index = (box_index + 1) % len(BOUNDING_BOXES)
        time.sleep(1)
    if not_ready:
        print(f"\033[94mScraping terminado. Se guardaron {total_alerts} alertas.\033[0m")
    else:
        print(f"\033[94mScraping cancelado con éxito\033[0m")

if __name__ == "__main__":
    print("Inciando scraping:")
    main()

