# 🚀 Bot de Automatización ONFIDE – Consulta Vecino

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)
![SQL Server](https://img.shields.io/badge/Database-SQL_Server-red)
![Arquitectura](https://img.shields.io/badge/Arquitectura-Procesamiento_en_cola-purple)
![Estado](https://img.shields.io/badge/Estado-Producción-success)

---

## 🎯 Descripción General

Sistema de automatización desarrollado en Python para ejecutar consultas de **estado vecino en ONFIDE**, reemplazando procesos manuales por un flujo **automatizado, escalable y controlado desde base de datos**.

El bot opera de forma continua, procesando registros según prioridad y asegurando trazabilidad completa.

---

## 💼 Impacto en el Negocio

* ⏱️ Reducción de tiempo operativo en **~90%**
* 🔄 Ejecución continua sin intervención manual
* 📊 Mayor volumen de procesamiento
* 🧠 Eliminación de tareas repetitivas
* 📈 Base para escalabilidad y automatización de nuevos procesos

---

## 🧠 Arquitectura del Sistema

```text
SQL Server (cola) → Bot (Selenium) → ONFIDE → SQL Server (resultados)
```

### Modelo de procesamiento

* Procesamiento tipo cola (`TOP 1`)
* Priorización automática (P1 → P2 → P3)
* Control de estados en base de datos

---

## ⚙️ Funcionalidades

* ✅ Automatización completa con Selenium
* ✅ Extracción de datos dinámicos (Angular)
* ✅ Integración directa con SQL Server
* ✅ Procesamiento basado en prioridad
* ✅ Ejecución en paralelo (multi-bot)
* ✅ Manejo de errores
* ✅ Trazabilidad completa (relación entre tablas)

---

## 🔄 Flujo de ejecución

1. Obtiene el siguiente registro pendiente desde SQL
2. Marca el registro como `REVISANDO`
3. Ejecuta la consulta en ONFIDE
4. Extrae datos estructurados
5. Guarda resultados en SQL
6. Marca como `REVISADO`
7. Repite el proceso automáticamente

---

## ⚡ Rendimiento

| Bots   | Procesamiento    |
| ------ | ---------------- |
| 1 bot  | ~2 registros/min |
| 2 bots | ~4 registros/min |
| 3 bots | ~6 registros/min |

⏱️ Tiempo promedio: **25–30 segundos por Access_ID**

---

## 🗄️ Modelo de Datos

### 🔹 Tabla origen

`toa_ahora_CV_estado`

Campos clave:

* ID
* Access_ID
* Prioridad
* REV
* OBSERVACION

---

### 🔹 Tabla destino

`consulta_ticket_vecino_onfide`

Incluye:

* Datos técnicos
* Potencias ópticas
* Estado de puerto
* 🔗 `relacion_ID` (relación con tabla origen)

---

## 🧪 Manejo de errores

* Captura de excepciones
* Registro de estado en base de datos
* Continuidad del proceso (no se detiene el bot)

Estados:

* `REVISANDO`
* `REVISADO`
* `ERROR`

---

## 🖥️ Ejecución

```bash
python app.py
```

---

## ⚡ Ejecución rápida (.bat)

```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate
python app.py
pause
```

---

## ⚠️ Requisitos

* Python 3.11
* Google Chrome
* ODBC Driver SQL Server
* Acceso a ONFIDE

---

## 🔐 Seguridad

No se almacenan credenciales en el código.

Se recomienda uso de variables de entorno:

```python
import os

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
```

---

## 📈 Escalabilidad

El sistema permite:

* Ejecución en múltiples instancias
* Distribución de carga mediante SQL
* Expansión a nuevos procesos automatizados

---

## 🔮 Mejoras futuras

* 📊 Dashboard de monitoreo
* 🔁 Reintentos automáticos
* 🚀 Ejecución como servicio
* ☁️ Despliegue en la nube

---

## 👨‍💻 Autor

Adolfo
Analista de Datos | Automatización

---

## 🏁 Estado del proyecto

🟢 En producción
🚀 Multi-bot activo
📈 Escalable

---

## 💡 Nota final

Este proyecto representa la transición desde procesos manuales hacia una **arquitectura automatizada, escalable y orientada a datos**, mejorando eficiencia operativa y reduciendo errores humanos.



