from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


URL_ONFIDE = "https://onfide-vno.onnetfibra.cl/vno/service-requests"


def iniciar_driver():

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    driver.get(URL_ONFIDE)

    return driver


def abrir_filtros(driver):
    wait = WebDriverWait(driver, 20)

    boton = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//ion-icon[@name='options-outline']]"))
    )

    driver.execute_script("arguments[0].click();", boton)


def seleccionar_access_id(driver):
    wait = WebDriverWait(driver, 20)

    access = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(),'AccessId')]"))
    )

    driver.execute_script("arguments[0].click();", access)


# 🔥 FUNCIÓN CLAVE (LA QUE FUNCIONA)
def buscar_access_id(driver, access_id):

    access_id_busqueda = f"02-{access_id}"

    print("⌨ Enviando AccessID...")
    print("Buscando:", access_id_busqueda)

    actions = ActionChains(driver)

    # 🔥 LIMPIEZA REAL (CLAVE)
    actions.send_keys(Keys.CONTROL + "a").perform()
    actions.send_keys(Keys.BACKSPACE).perform()

    time.sleep(0.3)

    # 🔥 escribir limpio
    actions.send_keys(access_id_busqueda).perform()
    actions.send_keys(Keys.ENTER).perform()

    print("✅ Búsqueda ejecutada")


def abrir_resultado(driver):

    wait = WebDriverWait(driver, 10)

    try:
        fila = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "tbody tr"))
        )

        fila.click()
        return True

    except:
        return False


def obtener_comentario_estado(driver):

    wait = WebDriverWait(driver, 10)

    comentario = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Comentarios de estado')]/following::div[1]")
        )
    )

    return comentario.text


def cerrar_orden(driver):

    try:
        driver.execute_script("""
        const boton = document.querySelector("button.app-button-clear");
        if(boton){ boton.click(); }
        """)
    except:
        pass


def obtener_comentario_tabla(driver, access_id):

    wait = WebDriverWait(driver, 10)

    access_id_busqueda = f"02-{access_id}"

    try:
        fila = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#dataTable tbody tr"))
        )

        celdas = fila.find_elements(By.CSS_SELECTOR, "td")

        if len(celdas) < 19:
            return "No encontrado en ONFIDE"

        if celdas[2].text.strip() != access_id_busqueda:
            return "No encontrado en ONFIDE"

        return celdas[18].text.strip()

    except:
        return "No encontrado en ONFIDE"

def limpiar_filtro_access_id(driver):

    print("🧹 Limpiando filtro AccessId...")

    try:
        # 🔥 buscar TODOS los botones de cerrar
        botones = driver.find_elements(By.XPATH, "//ion-icon[@name='close']")

        if botones:
            driver.execute_script("arguments[0].click();", botones[0])
            print("✅ Filtro eliminado")
            time.sleep(0.5)
        else:
            print("⚠ No se encontró botón de limpieza")

    except Exception as e:
        print("❌ Error limpiando filtro:", e)

def actualizar_comentario(sheet, fila, comentario):
    sheet.update_cell(fila, 12, comentario)