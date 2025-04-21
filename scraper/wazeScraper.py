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
        print("\033[92mPopup cerrado dinámicamente con movimiento.\033[0m")
    except:
        print("No apareció el popup.")

# Zoom al mapa
def double_zoom(drv):
    map_area = drv.find_element(By.CLASS_NAME, "wm-map")
    click_action = ActionChains(drv).move_to_element(map_area)
    click_action.double_click().perform()
    time.sleep(1)
    click_action.double_click().perform()
    print("\033[94mDoble zoom.\033[0m")


#Buscar las distintas alertas
def search_alerts(drv):
    alert_popups = drv.find_element(By.CLASS_NAME, "leaflet-pane") #"wm-alert-details")

    # Encuentra todos los divs dentro del contenedor
    divs = alert_popups.find_elements(By.TAG_NAME, "div")
    print(f"\033[93mSe encontraron {len(divs)} marcadores para clickear.\033[0m")

    # Clickear cada uno
    actions = ActionChains(driver)
    for i, div in enumerate(divs, 1):
        try:
            actions.move_to_element(div).click().perform()
            print(f"✅ Click en el marcador #{i}")
            time.sleep(0.5)  # espera entre clics para no sobrecargar
        except Exception as e:
            print(f"⚠️ No se pudo clickear el marcador #{i}: {e}")

# Moverse en circulos por la RM
def move_in_circle(drv):
    # Encontrar el canvas del mapa o contenedor
    map_area = drv.find_element(By.CLASS_NAME, "wm-map")

    actions = ActionChains(drv)

    center_x = 0
    center_y = 0
    radius = 100  # en píxeles
    steps = 20    # número de puntos en la circunferencia

    # Recolectar elementos múltiples veces
    for i in range(steps):
        angle = 2 * math.pi * (i / steps)
        dx = int(radius * math.cos(angle))
        dy = int(radius * math.sin(angle))

        actions.move_to_element(map_area).click_and_hold().move_by_offset(dx, dy).release().perform()
        print(f"Movido a offset ({dx}, {dy})")
        time.sleep(2) 



#----------------------------------- Main
# Iniciar navegador
# Configurar opciones
chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")  # Pantalla completa (modo F11)

driver = webdriver.Chrome(options=chrome_options)

try:
    driver.get("https://www.waze.com/es-419/live-map/")
    time.sleep(5)  # Espera inicial para que cargue el contenido básico

    wait = WebDriverWait(driver, 5) # Espera al popup inicial

    # Funcion creada arriba
    close_popup(driver, wait)

    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "wz-livemap")))

    # Acá se ejecutan distintas acciones, ver funciones arriba
    # Hace zoom
    time.sleep(2)
    double_zoom(driver)

    time.sleep(2)
    search_alerts(driver)

finally:
    driver.quit()