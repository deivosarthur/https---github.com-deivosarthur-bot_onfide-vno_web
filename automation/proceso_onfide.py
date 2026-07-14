from sheets_reader import obtener_access_ids
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import TimeoutException

from consulta_vecino_repository import registrar_access_id
from consulta_vecino_rules import COMENTARIOS_CONSULTA_VECINO


from onfide_scraper import (
    abrir_filtros,
    seleccionar_access_id,
    buscar_access_id,
    obtener_comentario_tabla,
    abrir_resultado,
    obtener_comentario_estado,
    cerrar_orden,
    actualizar_comentario,
    limpiar_filtro_access_id
)


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
        orden_de_trabajo = registro["orden_de_trabajo"]
        observacion = registro["observacion"]

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

        # ------------------------------------------
        # Registrar Access_ID para Consulta Vecino
        # ------------------------------------------

        if any(
            texto.lower() in comentario.lower()
            for texto in COMENTARIOS_CONSULTA_VECINO
        ):

            log(f"📌 Comentario requiere Consulta Vecino ({access_id})")

            try:
            

                registrado = registrar_access_id(access_id, orden_de_trabajo, observacion)

                if registrado:

                    log(f"✅ Access_ID registrado: {access_id}")

                else:

                    log(f"ℹ Access_ID ya existía: {access_id}")

            except Exception as e:

                log(f"⚠ Error registrando Access_ID: {e}")

        # No detener el flujo

        # ------------------------------------------
        # Flujo normal del bot
        # ------------------------------------------

        actualizar_comentario(sheet, fila, comentario)

        time.sleep(1)
        
        limpiar_filtro_access_id(driver)

        time.sleep(1)

        # 🔥 REACTIVAR FILTRO
        abrir_filtros(driver)
        seleccionar_access_id(driver)

    log("Ciclo finalizado")

    return True