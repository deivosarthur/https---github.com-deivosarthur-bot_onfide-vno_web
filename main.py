import time
import os

from automation.proceso_onfide import ejecutar_bot
from onfide_scraper import iniciar_driver

from bot_controller import set_driver

from bot_state import BOT_STATE

from heartbeat import guardar_estado
from datetime import datetime
from automation.session_manager import (
    validar_sesion
)
from onfide_scraper import iniciar_driver

from automation.restart_manager import (
    reinicio_completo
)
from monitoring.command_listener import (
    procesar_comandos
)
if __name__ == "__main__":

    driver = iniciar_driver()
    
    set_driver(driver)

    BOT_STATE["pid_bot"] = os.getpid()

    BOT_STATE["pid_chromedriver"] = (
        driver.service.process.pid
    )

    BOT_STATE["pid_chrome"] = (
        driver.capabilities["goog:processID"]
    )

    BOT_STATE["estado"] = "INICIANDO"

    BOT_STATE["mensaje"] = "Inicializando ONFIDE"

    guardar_estado()

   

    while True:
        
        try:
        
            comando = procesar_comandos()

            if comando:

                print(
                    "Comando recibido correctamente"
                )

                BOT_STATE["reinicios"] += 1

                BOT_STATE["mensaje"] = (
                    "Reinicio remoto"
                )

                guardar_estado()

                reinicio_completo()
            

            BOT_STATE["estado"] = "VALIDANDO"

            BOT_STATE["mensaje"] = "Validando sesión"
            

            guardar_estado()

            validar_sesion(driver)
            
            BOT_STATE["estado"] = "PROCESANDO"

            BOT_STATE["mensaje"] = "Ejecutando proceso"

            guardar_estado()

            

            ejecutado = ejecutar_bot(driver)

            if ejecutado:

                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = "Proceso completado"

                BOT_STATE["ciclos_ok"] += 1
                

            else:

                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = "Sin datos"

                BOT_STATE["ciclos_ok"] += 1
                
            guardar_estado()

        except Exception as e:

            BOT_STATE["estado"] = "ERROR"

            BOT_STATE["mensaje"] = str(e)

            BOT_STATE["errores"] += 1

            print(e)

            guardar_estado()
        

        for _ in range(10):

            BOT_STATE["ultima_actualizacion"] = (
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )

            guardar_estado()

            time.sleep(1)

        