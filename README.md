# 🤖 BOT ONFIDE AUTOMATION

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)
![Status](https://img.shields.io/badge/Status-Production-success)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)

---

## 🚀 Descripción

Bot de automatización desarrollado en Python para la gestión de tickets en ONFIDE, con integración a Google Sheets y control mediante interfaz gráfica.

El bot funciona en ejecución continua, detectando nuevos registros y procesándolos automáticamente.

---

## ⚡ Rendimiento

- ⏱️ Tiempo promedio por AccessID: **1 – 3 segundos**
- 🔁 Frecuencia de revisión de Google Sheets: **cada 10 segundos**
- 📊 Procesamiento optimizado usando:
  - Lectura directa desde tabla principal
  - Uso de popup solo cuando es necesario

---

## ⚙️ Configuración (IMPORTANTE)

### 🔹 Intervalo de ejecución (loop)

En `app.py`:

```python
time.sleep(10)


### 🔹Lógica de comentarios (uso de popup)


En `main.py`:

```python
COMENTARIOS_NO_REQUIEREN_POPUP = [
    "No se ha detectado afectación de servicio en el puerto",
    "initial status"
]

El bot funciona en ejecución continua, detectando nuevos registros y procesándolos automáticamente.
-------------

🧠 Flujo de funcionamiento

<img width="360" height="280" alt="image" src="https://github.com/user-attachments/assets/db28fb3a-95b1-4656-a556-d37519bd96bf" />

------------
🖥️ Interfaz

- ▶️ INICIAR BOT
- 🔐 YA HICE LOGIN
- ⛔ APAGAR BOT
- 📟 Consola en tiempo real

<img width="879" height="460" alt="image" src="https://github.com/user-attachments/assets/b411eb59-cc09-4bf7-8371-16be7ee3d873" />




