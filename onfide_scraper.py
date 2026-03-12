from selenium import webdriver
from selenium.webdriver.chrome.service import Service
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
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(),'AccessId')]"))
    )

    access.click()

def buscar_access_id(driver, access_id):

    wait = WebDriverWait(driver, 20)

    campo = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Buscar']"))
    )

    campo.clear()

    campo.send_keys(access_id)

    campo.send_keys(Keys.ENTER)


if __name__ == "__main__":

    driver = iniciar_driver()

    esperar_login()

    print("✅ Login detectado")

    abrir_filtros(driver)

    seleccionar_access_id(driver)

    buscar_access_id(driver, "1-3IOKEL31")

    input("Presiona ENTER para cerrar...")