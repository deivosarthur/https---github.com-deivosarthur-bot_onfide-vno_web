from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from config import USUARIO_ONFIDE, PASSWORD_ONFIDE
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException


URL_ONFIDE = "https://onfide-vno.onnetfibra.cl/vno/service-requests"


def sesion_activa(driver):

    try:

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//ion-icon[@name='options-outline']]")
            )
        )

        return True

    except:
        return False

def reautenticar(driver):

    print("🔒 Sesión expirada")

    try:

        # ventana login ONFIDE
        botones = driver.find_elements(
            By.CSS_SELECTOR,
            "ion-button"
        )

        if botones:

            driver.execute_script(
                "arguments[0].click();",
                botones[0]
            )

            print("✅ Botón login ONFIDE presionado")

        WebDriverWait(driver, 10).until(
            lambda d: len(d.window_handles) > 1
        )

        # cambiar a ventana WSO2
        ventana_principal = driver.current_window_handle

        if len(driver.window_handles) > 1:

            driver.switch_to.window(
                driver.window_handles[-1]
            )

            print("✅ Ventana WSO2 detectada")

        else:
            print("❌ No se abrió ventana WSO2")
            return

        wait = WebDriverWait(driver, 15)

        # usuario
        usuario = wait.until(
            EC.presence_of_element_located(
                (By.ID, "usernameUserInput")
            )
        )
        print("URL WSO2:", driver.current_url)
        usuario.clear()
        usuario.send_keys(USUARIO_ONFIDE)
        driver.execute_script(
            """
            document.getElementById('username').value = arguments[0];
            """,
            USUARIO_ONFIDE
        )
        print("✅ Usuario ingresado")

        # password
        password = driver.find_element(
            By.ID,
            "password"
        )

        password.clear()
        password.send_keys(PASSWORD_ONFIDE)

        print("✅ Password ingresada")
        
        # DEBUG
        print(
            "usernameUserInput:",
            driver.find_element(
                By.ID,
                "usernameUserInput"
            ).get_attribute("value")
        )

        print(
            "username hidden:",
            driver.find_element(
                By.ID,
                "username"
            ).get_attribute("value")
        )

        print(
            "password largo:",
            len(
                driver.find_element(
                    By.ID,
                    "password"
                ).get_attribute("value")
            )
        )
        cerrar_banner_cookies(driver)
        # recordar equipo
        recordar = driver.find_element(
            By.ID,
            "chkRemember"
        )

        if not recordar.is_selected():
            recordar.click()

        print("✅ Recordarme activado")

        # botón login
        boton_login = driver.find_element(
            By.ID,
            "sign-in-button"
        )

        boton_login.click()
        
        print("✅ Login enviado")
        ##############################
        time.sleep(5)

        print("Ventanas abiertas:", len(driver.window_handles))

        login_exitoso = False

        for i, handle in enumerate(driver.window_handles):

            driver.switch_to.window(handle)

            url = driver.current_url

            print(f"Ventana {i}: {url}")

            if "onfide-vno.onnetfibra.cl" in url:
                login_exitoso = True

        if login_exitoso:
            print("✅ Login exitoso")
        else:
            print("❌ Login falló")
        ########################################
        #driver.close()

        #driver.switch_to.window(
        #    ventana_principal
        #)

    except Exception as e:

        print("❌ Error reautenticando:", e)
        
        
        
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
    
    


def cerrar_banner_cookies(driver):

    try:

        boton = WebDriverWait(driver, 3).until(

            EC.element_to_be_clickable(

                (
                    By.CSS_SELECTOR,
                    "button[data-testid='cookie-consent-banner-confirm-button']"
                )

            )

        )

        boton.click()

        print("✅ Banner de cookies cerrado")

        time.sleep(1)

    except TimeoutException:

        pass