from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Iniciar navegador con configuración por defecto (visualmente)
driver = webdriver.Chrome()

try:
    driver.get("https://www.waze.com/es-419/live-map/")

    # Espera fija (puedes reemplazarla con espera dinámica luego)
    time.sleep(5)

    # Buscar elementos por clase
    elementos = driver.find_elements(By.CLASS_NAME, "wm-rgeocoding")

    print(f"Se encontraron {len(elementos)} elementos:")
    for i, el in enumerate(elementos, 1):
        print(f"{i}. {el.text}")

finally:
    driver.quit()
