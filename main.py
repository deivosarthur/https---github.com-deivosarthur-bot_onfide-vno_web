from sheets_reader import obtener_access_ids
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

from onfide_scraper import *


COMENTARIOS_NO_REQUIEREN_POPUP = [
    "No se ha detectado afectación de servicio en el puerto",
    "initial status"
]


def ejecutar_bot(driver, log=print):

    if driver is None:
        log("ERROR: driver es None (no inicializado)")
        return False

    wait = WebDriverWait(driver, 15)

    log("Validando ONFIDE...")

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[.//ion-icon[@name='options-outline']]")
            )
        )
    except TimeoutException:
        log("ONFIDE no está listo")
        return False

    log("Leyendo Google Sheets...")

    registros, sheet = obtener_access_ids()

    log(f"Se encontraron {len(registros)} registros")

    if len(registros) == 0:
        return False

    # 🔥 SOLO UNA VEZ
    abrir_filtros(driver)
    seleccionar_access_id(driver)

    for i, registro in enumerate(registros, start=1):

        access_id = registro["access_id"]
        fila = registro["fila"]

        if not access_id:
            continue

        log(f"\nAccessID {i}/{len(registros)} → {access_id}")

        buscar_access_id(driver, access_id)

        access_id_busqueda = f"02-{access_id}"

        try:
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.CSS_SELECTOR, "#dataTable tbody tr td:nth-child(3)"),
                    access_id_busqueda
                )
            )

            comentario = obtener_comentario_tabla(driver, access_id)

            if not any(x in comentario for x in COMENTARIOS_NO_REQUIEREN_POPUP):

                log("Abriendo popup")

                encontrado = abrir_resultado(driver)

                if encontrado:
                    comentario = obtener_comentario_estado(driver)
                    cerrar_orden(driver)

        except TimeoutException:
            log("No encontrado en ONFIDE")
            comentario = "No encontrado en ONFIDE"

        log("Comentario:")
        log(comentario)

        actualizar_comentario(sheet, fila, comentario)

        time.sleep(1)
        
        limpiar_filtro_access_id(driver)

        time.sleep(1)

        # 🔥 REACTIVAR FILTRO
        abrir_filtros(driver)
        seleccionar_access_id(driver)

    log("Ciclo finalizado")

    return True