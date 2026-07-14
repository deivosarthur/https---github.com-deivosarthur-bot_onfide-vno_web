from datetime import datetime

BOT_STATE = {

    "bot": "ONFIDE",

    "version": "1.0",

    "estado": "INICIANDO",

    "mensaje": "",

    "ultima_actualizacion": "",

    "ultima_descarga": "",

    "ciclos_ok": 0,

    "errores": 0,

    "errores_consecutivos": 0,

    "alerta_error_enviada": False,

    "session_recovery": 0,

    "reinicios": 0,

    "pid_bot": None,

    "pid_chromedriver": None,

    "pid_chrome": None,

    "uptime_inicio": datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

}