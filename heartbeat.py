import json
from pathlib import Path
from datetime import datetime

from bot_state import BOT_STATE


HEARTBEAT_PATH = (
    Path(__file__).parent
    / "heartbeat.json"
)


def guardar_estado():

    BOT_STATE["ultima_actualizacion"] = (
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )

    with open(
        HEARTBEAT_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            BOT_STATE,
            f,
            indent=4,
            ensure_ascii=False
        )