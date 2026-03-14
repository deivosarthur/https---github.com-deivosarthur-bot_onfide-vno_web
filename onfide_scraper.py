from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import pyperclip
from selenium.webdriver.common.action_chains import ActionChains

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


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


def esperar_login():
    input("🔐 Haz login en ONFIDE y presiona ENTER aquí...")


def abrir_filtros(driver):

    wait = WebDriverWait(driver, 20)

    boton = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[.//ion-icon[@name='options-outline']]"))
    )

    driver.execute_script("arguments[0].click();", boton)


def seleccionar_access_id(driver):

    wait = WebDriverWait(driver, 20)

    access = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[contains(text(),'AccessId')]")
        )
    )

    driver.execute_script("arguments[0].click();", access)


def buscar_access_id(driver, access_id):

    print("⌨ Enviando AccessID al navegador...")

    actions = ActionChains(driver)

    actions.send_keys(access_id).perform()

    print("✅ AccessID enviado")

    time.sleep(1)

    actions.send_keys(Keys.ENTER).perform()

    print("🔎 Búsqueda ejecutada")
    
def abrir_resultado(driver):

    print("🔎 Buscando resultados...")

    wait = WebDriverWait(driver, 10)

    try:

        fila = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "tbody tr")
            )
        )

        print("✅ Resultado encontrado")

        fila.click()

        print("📂 Orden abierta")

        return True

    except:

        print("❌ No se encontró el AccessID")

        return False
    
    
    
def obtener_comentario_estado(driver):

    print("📖 Buscando comentario de estado...")

    wait = WebDriverWait(driver, 10)

    comentario = wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//*[contains(text(),'Comentarios de estado')]/following::div[1]")
        )
    )

    texto = comentario.text

    print("--- Comentario encontrado:")
    print(texto)

    return texto

def actualizar_comentario(sheet, fila, comentario):

    print("--- Guardando comentario en Google Sheets... ---")

    sheet.update_cell(fila, 12, comentario)

    print("---Comentario guardado en columna L ---")

def limpiar_filtro_access_id(driver):

    print("🧹 Limpiando filtro AccessId...")

    wait = WebDriverWait(driver, 5)

    try:
        boton_close = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//ion-icon[@name='close']")
            )
        )

        driver.execute_script("arguments[0].click();", boton_close)

        print("✅ Filtro eliminado")

    except:
        print("⚠ No había filtro activo")
       
       
       
def cerrar_orden(driver):

    print("🔙 Cerrando panel de orden...")

    try:

        driver.execute_script("""
        const boton = document.querySelector("button.app-button-clear");
        if(boton){
            boton.click();
        }
        """)

        print("✅ Panel cerrado")

    except Exception as e:

        print("⚠ No se pudo cerrar el panel")
        print(e)
        
        

if __name__ == "__main__":

    driver = iniciar_driver()

    esperar_login()

    print("---Login detectado---")

    abrir_filtros(driver)

    time.sleep(2)

    seleccionar_access_id(driver)

    time.sleep(3)

    buscar_access_id(driver, "1-3IOKEL31")

    time.sleep(3)

    encontrado = abrir_resultado(driver)

    if encontrado:

        time.sleep(2)

        comentario = obtener_comentario_estado(driver)

        print("Comentario final capturado:")
        print(comentario)

    input("Presiona ENTER para cerrar...")