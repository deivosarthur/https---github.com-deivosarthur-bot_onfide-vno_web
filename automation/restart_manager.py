from pathlib import Path
import subprocess
import sys
import os
import time

from bot_controller import (
    get_driver,
    cerrar_driver
)

BASE_DIR = Path(__file__).resolve().parent.parent
APP_PATH = BASE_DIR / "main.py"


def reinicio_completo():

    print("[RESTART] Ejecutando reinicio completo...")

    try:

        driver = get_driver()

        cerrar_driver(driver)

    except Exception as e:

        print(
            f"[WARNING] Error cerrando driver: {e}"
        )

    time.sleep(2)

    subprocess.Popen(

        [
            sys.executable,
            str(APP_PATH)
        ],

        cwd=str(BASE_DIR)

    )

    print(
        "[RESTART] Cerrando proceso actual..."
    )

    os._exit(0)