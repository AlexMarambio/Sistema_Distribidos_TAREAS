from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import math

#----------------------------------- Funcs

# Cierra el pop up que dice entendido
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

# Zoom al mapa
def double_zoom(drv):
    map_area = drv.find_element(By.CLASS_NAME, "wm-map")
    click_action = ActionChains(drv).move_to_element(map_area)
    click_action.double_click().perform()
    time.sleep(0.5)
    click_action.double_click().perform()
    time.sleep(0.5)
    click_action.double_click().perform()
    print("\033[94mTriple zoom.\033[0m")


#Buscar las distintas alertas
def search_alerts(drv):
    alert_popups = drv.find_element(By.CLASS_NAME, "leaflet-map-pane") #"wm-alert-details")

    # Encuentra todos los divs dentro del contenedor
    divs = alert_popups.find_elements(By.TAG_NAME, "div")
    filtered_divs = [d for d in divs if "wm-alert-icon" in d.get_attribute("class")]

    # Clickear cada uno
    actions = ActionChains(drv)
    for i, div in enumerate(filtered_divs, 1):
        try:
            actions.move_to_element(div).click().perform()
            element = drv.find_element(By.CLASS_NAME, "wm-alert-details")
            print(
            drv.find_element(By.CLASS_NAME, "wm-alert-details__title").text,
            drv.find_element(By.CLASS_NAME, "wm-alert-details__address").text,
            drv.find_element(By.CLASS_NAME, "wm-alert-details__description").text,
            drv.find_element(By.CLASS_NAME, "wm-alert-details__reporter-name").text,
            drv.find_element(By.CLASS_NAME, "wm-alert-details__time").text
            )
            #time.sleep(1)
            #actions.move_to_element(element.find_element(By.CLASS_NAME,"leaflet-popup-close-button")).click().perform()
            time.sleep(0.5)  # espera entre clics para no sobrecargar
        except:
            pass

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
        action.move_to_element_with_offset(map_area,initial_x,initial_y) \
            .click_and_hold() \
            .pause(1) \
            .move_by_offset(dx, dy) \
            .pause(1) \
            .move_by_offset(dx, dy) \
            .release().perform()
        time.sleep(0.5)
    except Exception as e:
        print(f"Error al mover de ({initial_x}, {initial_y}) a ({dx}, {dy}): {e}")

def move_and_search(drv):
    for i in range(30):
        search_alerts(drv)
        time.sleep(2)
        drag_map(drv,"v",True)

def remove_elements_by_class(drv, class_name):
    script = f"""
    var elements = document.getElementsByClassName("{class_name}");
    while(elements.length > 0) {{
        elements[0].parentNode.removeChild(elements[0]);
    }}
    """
    drv.execute_script(script)

#----------------------------------- Main
# Iniciar navegador
# Configurar opciones
chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")  # Pantalla completa (modo F11)

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.waze.com/es-419/live-map/")
    time.sleep(3)  # Espera inicial para que cargue el contenido básico

    wait = WebDriverWait(driver, 2) # Espera al popup inicial

    # Funcion creada arriba
    close_popup(driver, wait)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wz-livemap")))
    remove_elements_by_class(driver,"notification-portal")
    remove_elements_by_class(driver,"wz-header")
    remove_elements_by_class(driver,"wm-cards")
    remove_elements_by_class(driver,"leaflet-control-container")

    # Acá se ejecutan distintas acciones, ver funciones arriba
    # Hace zoom
    time.sleep(1)
    double_zoom(driver)

    time.sleep(1)
    move_and_search(driver)

finally:
    driver.quit()