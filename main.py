from sheets_reader import obtener_access_ids
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from onfide_scraper import *

print("🚀 Iniciando bot ONFIDE")

print("📄 Leyendo Google Sheets...")

resultado = obtener_access_ids()
registros = resultado[0]
sheet = resultado[1]

print(f"🔢 Se encontraron {len(registros)} registros")

driver = iniciar_driver()

esperar_login()

abrir_filtros(driver)

time.sleep(2)

seleccionar_access_id(driver)

for registro in registros[:5]:

    access_id = registro["access_id"]
    fila = registro["fila"]

    if not access_id:
        print("⚠ AccessID vacío, saltando...")
        continue

    print(f"\n🔎 Procesando AccessID: {access_id}")

    buscar_access_id(driver, access_id)

    time.sleep(3)

    encontrado = abrir_resultado(driver)

    if encontrado:

        time.sleep(2)

        comentario = obtener_comentario_estado(driver)

        actualizar_comentario(sheet, fila, comentario)

        cerrar_orden(driver)

        time.sleep(2)

    else:

        actualizar_comentario(sheet, fila, "No encontrado en ONFIDE")

    time.sleep(2)

    limpiar_filtro_access_id(driver)

    time.sleep(2)

    abrir_filtros(driver)

    time.sleep(1)

    seleccionar_access_id(driver)

    time.sleep(1)