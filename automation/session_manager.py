from bot_state import BOT_STATE
from heartbeat import guardar_estado

from onfide_scraper import (
    sesion_activa,
    reautenticar
)


def validar_sesion(driver):

    print("Validando sesión...")

    if sesion_activa(driver):

        return

    print("No hay sesión activa.")

    BOT_STATE["estado"] = "LOGIN"

    BOT_STATE["mensaje"] = "Realizando autenticación"

    guardar_estado()

    reautenticar(driver)

    if not sesion_activa(driver):

        BOT_STATE["estado"] = "ERROR"

        BOT_STATE["mensaje"] = "No fue posible iniciar sesión"

        guardar_estado()

        raise Exception(
            "No fue posible iniciar sesión."
        )

    print("Sesión lista.")