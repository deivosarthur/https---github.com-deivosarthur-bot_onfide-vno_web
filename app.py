import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import time

from automation.proceso_onfide import ejecutar_bot
from onfide_scraper import iniciar_driver
import os

from bot_state import BOT_STATE
from heartbeat import guardar_estado
from datetime import datetime
from bot_controller import set_driver

from monitoring.command_listener import procesar_comandos

from automation.restart_manager import reinicio_completo

bot_activo = False
driver = None
login_listo = False


def log(msg):
    consola.insert(tk.END, msg + "\n")
    consola.see(tk.END)


def iniciar_bot():
    global bot_activo, driver
    
    if bot_activo:
        return

    bot_activo = True

    BOT_STATE["estado"] = "INICIANDO"

    BOT_STATE["mensaje"] = "Inicializando ONFIDE"

    BOT_STATE["pid_bot"] = os.getpid()
    
    if driver is None:
        log("Abriendo ONFIDE...")
        driver = iniciar_driver()
        set_driver(driver)
        
        
        BOT_STATE["pid_chromedriver"] = (
            driver.service.process.pid
        )

        BOT_STATE["pid_chrome"] = (
            driver.capabilities["goog:processID"]
        )
        
        guardar_estado()
        
        log("Haz login y presiona 'YA HICE LOGIN'")

    threading.Thread(target=loop_bot, daemon=True).start()


def confirmar_login():
    global login_listo
    login_listo = True
    
    BOT_STATE["estado"] = "LOGIN"

    BOT_STATE["mensaje"] = "Login confirmado"

    guardar_estado()
    
    log("Login confirmado")


def detener_bot():
    global bot_activo
    bot_activo = False
    
    BOT_STATE["estado"] = "DETENIDO"

    BOT_STATE["mensaje"] = "Bot detenido"

    guardar_estado()
    
    log("Bot detenido")


def loop_bot():
    global bot_activo, login_listo
    
    

    while bot_activo:
        
        BOT_STATE["ultima_actualizacion"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
            )
        )

        guardar_estado()

        comando = procesar_comandos()

        if comando:

            log("📨 Reinicio remoto solicitado")

            BOT_STATE["reinicios"] += 1

            BOT_STATE["mensaje"] = "Reinicio remoto"

            guardar_estado()

            reinicio_completo()
        
        
        if not login_listo:
            time.sleep(3)
            continue

        try:
            ejecutado = ejecutar_bot(driver, log)

            if ejecutado:

                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = "Proceso completado"

                BOT_STATE["ciclos_ok"] += 1

                guardar_estado()

                log("Proceso completado")
                
            else:

                BOT_STATE["estado"] = "OK"

                BOT_STATE["mensaje"] = "Sin datos"

                guardar_estado()

                log("Sin datos")
                

        except Exception as e:
            
            BOT_STATE["estado"] = "ERROR"

            BOT_STATE["mensaje"] = str(e)

            BOT_STATE["errores"] += 1

            guardar_estado()
            
            log(f"Error: {e}")

        time.sleep(10)


root = tk.Tk()
root.title("BOT ONFIDE")
root.geometry("900x450")

consola = ScrolledText(root, bg="black", fg="white")
consola.place(x=20, y=20, width=600, height=380)


def btn(txt, cmd, y):
    tk.Button(root, text=txt, command=cmd, width=22).place(x=670, y=y)


btn("INICIAR BOT", iniciar_bot, 90)
btn("YA HICE LOGIN", confirmar_login, 160)
btn("DETENER BOT", detener_bot, 230)

root.mainloop()