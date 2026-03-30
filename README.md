# 🚀 ONFIDE Neighbor Automation Bot

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green?logo=selenium)
![SQL Server](https://img.shields.io/badge/Database-SQL_Server-red)
![Architecture](https://img.shields.io/badge/Architecture-Queue_Processing-purple)
![Status](https://img.shields.io/badge/Status-Production-success)

---

## 🎯 Overview

Automation system designed to execute **Neighbor Status Queries in ONFIDE**, replacing manual operations with a **scalable, fault-tolerant, database-driven pipeline**.

The solution processes network access identifiers automatically, ensuring **continuous execution, prioritization, and full traceability**.

---

## 💼 Business Impact

* ⏱️ Reduced manual processing time by **~90%**
* 🔄 Continuous unattended execution (24/7 ready)
* 📊 Increased operational throughput with multi-bot execution
* 🧠 Eliminated human dependency in repetitive tasks
* 📈 Scalable architecture ready for expansion

---

## 🧠 System Architecture

```text
SQL Server (Queue) → Python Bot → ONFIDE → SQL Server (Results)
```

### Processing Model

* Queue-based processing (TOP 1)
* Priority-driven execution
* State-controlled lifecycle

---

## ⚙️ Core Features

* ✅ Automated navigation using Selenium
* ✅ Dynamic data extraction (Angular-based UI)
* ✅ SQL-based queue system
* ✅ Priority handling (P1 → P2 → P3)
* ✅ Multi-instance parallel execution
* ✅ Error handling and recovery
* ✅ Full data traceability (relational link)

---

## 🔄 Workflow

1. Fetch next pending record from SQL
2. Mark as `REVISANDO`
3. Execute ONFIDE neighbor query
4. Extract structured data
5. Store results in SQL
6. Mark as `REVISADO`
7. Repeat (continuous loop)

---

## ⚡ Performance

| Bots   | Throughput     |
| ------ | -------------- |
| 1 Bot  | ~2 records/min |
| 2 Bots | ~4 records/min |
| 3 Bots | ~6 records/min |

⏱️ Avg processing time: **25–30 seconds per Access_ID**

---

## 🗄️ Data Model

### Source Table

`toa_ahora_CV_estado`

* ID (Primary Key)
* Access_ID
* Prioridad
* REV (Status)
* OBSERVACION

---

### Target Table

`consulta_ticket_vecino_onfide`

* Network metrics
* Optical power data
* Port status
* 🔗 `relacion_ID` (foreign key reference)

---

## 🧪 Error Handling

* Try/catch implementation
* Automatic status update:

  * `REVISANDO`
  * `REVISADO`
  * `ERROR`
* Logging for traceability

---

## 🖥️ Execution

```bash
python app.py
```

---

## ⚡ Quick Start (.bat)

```bat
@echo off
cd /d %~dp0
call venv\Scripts\activate
python app.py
pause
```

---

## ⚠️ Requirements

* Python 3.11
* Google Chrome
* ODBC Driver 17/18 for SQL Server
* Network access to ONFIDE

---

## 🔐 Security

Credentials are NOT stored in the repository.

Recommended approach:

```python
import os

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
```

---

## 📈 Scalability

This system supports:

* Horizontal scaling (multiple bots)
* Load distribution via SQL queue
* Future orchestration (Docker / Scheduler / Cloud)

---

## 🔮 Future Improvements

* 📊 Monitoring dashboard
* 📡 Real-time metrics
* 🔁 Retry mechanism for failures
* 🧩 Modular microservices architecture
* ☁️ Cloud deployment

---

## 👨‍💻 Author

**Adolfo**
Data Analyst | Automation Engineer

---

## 🏁 Project Status

🟢 Production-ready
🚀 Multi-instance deployment
📈 Scalable architecture

---

## 💡 Final Note

This project represents a transition from **manual operations to intelligent automation**, enabling efficiency, scalability, and reliability in telecom workflows.



