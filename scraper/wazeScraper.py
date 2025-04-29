from seleniumwire import webdriver  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import json
import time

#----------------------------------- Funcs

def close_popup(drv, wt):
    try:
        close_button = wt.until(EC.element_to_be_clickable((By.CLASS_NAME, "waze-tour-tooltip__acknowledge")))
        ActionChains(drv).move_to_element(close_button).click().perform()
        print("\033[92mPopup 'Entendido' cerrado.\033[0m")

        close_button = wt.until(EC.element_to_be_clickable((By.CLASS_NAME, "wz-downloadbar__close-button")))
        ActionChains(drv).move_to_element(close_button).click().perform()
        print("\033[92mPopup 'Download' cerrado.\033[0m")
    except:
        print("No apareció el popup.")

def drag_map(drv, direction="v", forward=True):
    map_area = drv.find_element(By.CLASS_NAME, "wm-map")
    action = ActionChains(drv)
    offset_x = (map_area.size["width"]//2)-10
    offset_y = (map_area.size["height"]//2)-10

    dx, dy, initial_x, initial_y = 0, 0, 0, 0
    if direction == "v":
        dy = offset_y if forward else -offset_y
        initial_y = -offset_y if forward else offset_y
    elif direction == "h":
        dx = offset_x if forward else -offset_x
        initial_x = -offset_x if forward else offset_x
    
    try:
        action.move_to_element_with_offset(map_area, initial_x, initial_y) \
            .click_and_hold() \
            .pause(1) \
            .move_by_offset(dx, dy) \
            .pause(1) \
            .move_by_offset(dx, dy) \
            .release().perform()
        time.sleep(1)
    except Exception as e:
        print(f"Error al mover de ({initial_x}, {initial_y}) a ({dx}, {dy}): {e}")

def remove_elements_by_class(drv, class_name):
    script = f"""
    var elements = document.getElementsByClassName("{class_name}");
    while(elements.length > 0) {{
        elements[0].parentNode.removeChild(elements[0]);
    }}
    """
    drv.execute_script(script)

#Busca el archivo georrss que que crea en network -> response, es un json con muchas alertas
#Es la forma más rápida de scrapear los 10k datos
def fetch_georrss_alerts(drv):
    print("\033[94mBuscando archivo GeoRSS...\033[0m")
    for request in drv.requests:
        if request.response and "georss" in request.url:
            print(f"\033[92mGeoRSS encontrado: {request.url}\033[0m")
            try:
                body_str = request.response.body.decode('utf-8')
                data = json.loads(body_str)
                alerts = data.get("alerts", [])
                
                for alert in alerts:
                    if "comments" in alert:
                        del alert["comments"]
                
                return alerts
            except Exception as e:
                print(f"\033[91mError procesando el GeoRSS: {e}\033[0m")
                return []
    else:
        print("\033[91mNo se encontró ningún GeoRSS.\033[0m")
        return []

def collect_alerts(drv, wait_alerts=10000):
    collected_alerts = []
    visited_uuids = set()

    # Definir secuencia de movimientos
    move_sequence = [("v", True),("h", True),("v", False),("h", False)]
    move_index = 0  # Para rotar en la secuencia

    while len(collected_alerts) < wait_alerts:
        alerts = fetch_georrss_alerts(drv)
        for alert in alerts:
            collected_alerts.append(alert)

        print(f"\033[93mAlerts acumulados: {len(collected_alerts)}\033[0m")

        if len(collected_alerts) >= wait_alerts:
            break

        # Mover el mapa en circulos
        direction, forward = move_sequence[move_index]
        drag_map(drv, direction=direction, forward=forward)
        move_index = (move_index + 1) % len(move_sequence)
        time.sleep(2)  # Esperar que lleguen nuevos requests

    # Guardar, cambiar por enviarlo a la bdd
    filename = f"alerts_10k_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_alerts, f, ensure_ascii=False, indent=2)

    print(f"\033[92mSe guardaron {len(collected_alerts)} alerts en '{filename}'\033[0m")


#----------------------------------- Main
chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.waze.com/es-418/live-map/")
    time.sleep(3)

    wait = WebDriverWait(driver, 5)

    close_popup(driver, wait)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wz-livemap")))
    remove_elements_by_class(driver,"notification-portal")
    remove_elements_by_class(driver,"wz-header")
    remove_elements_by_class(driver,"wm-cards")
    remove_elements_by_class(driver,"leaflet-control-container")
    time.sleep(2)

    collect_alerts(driver,700)

finally:
    driver.quit()
