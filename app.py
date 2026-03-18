import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import time

from main import ejecutar_bot
from onfide_scraper import iniciar_driver


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

    if driver is None:
        log("Abriendo ONFIDE...")
        driver = iniciar_driver()
        log("Haz login y presiona 'YA HICE LOGIN'")

    threading.Thread(target=loop_bot, daemon=True).start()


def confirmar_login():
    global login_listo
    login_listo = True
    log("Login confirmado")


def detener_bot():
    global bot_activo
    bot_activo = False
    log("Bot detenido")


def loop_bot():
    global bot_activo, login_listo

    while bot_activo:

        if not login_listo:
            time.sleep(3)
            continue

        try:
            ejecutado = ejecutar_bot(driver, log)

            if ejecutado:
                log("Proceso completado")
            else:
                log("Sin datos")

        except Exception as e:
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