# 🚑 Hospital Emergency Room Simulation

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Python Version](https://img.shields.io/badge/python-3.11+-blue)
![License](https://img.shields.io/badge/License-Academic-lightgrey)
![Status](https://img.shields.io/badge/Project-Active-brightgreen)

A concurrent system that simulates the flow of patients through a hospital emergency room, prioritizing urgency and managing resources (doctors) with shared memory and multithreaded processing.

> 📚 Developed as part of a practical evaluation in Operating Systems focusing on process communication and synchronization.

---

## 🚀 Project Highlights

- ⚙️ **Multithreaded TCP server**: handles up to 20 patient clients concurrently
- 🧠 **Triage system**: RED > YELLOW > GREEN priority queue
- 👨‍⚕️ **Doctor simulation**: up to 5 concurrent doctors treating patients
- 🧵 **Thread-safe** architecture
- 🧩 Modular Python codebase
- 🔄 Upcoming: Flask-based live dashboard and Docker deployment

---

## 🧱 Architecture

### 🏥 Hospital Server

- Listens for TCP connections from patients
- Parses and enqueues patient data by urgency level
- Assigns doctors to patients in order of priority

### 🧑‍🤝‍🧑 Client Generator

- Simulates patients arriving randomly with different urgency levels
- Connects to the server and sends data (Patient ID + Urgency)

### 🔄 Modular Design

- `hospital_server.py` → Entry point / TCP listener
- `patient.py` → Patient class with priority logic
- `triage.py` → Triage queue handling
- `doctor.py` → Doctor worker threads
- `state.py` → Shared memory, settings, and global queue

---

## ✅ Requirements Met

- ✅ Shared memory between processes (`multiprocessing.Manager().Queue()`)
- ✅ Triage queue based on urgency
- ✅ Doctor concurrency limit (5 max)
- ✅ Patient arrival via TCP
- ✅ Extensible logging and monitoring

---

## 📦 Running the Simulation

### 🔧 Local setup

```bash
# Start the hospital server
python3 server/hospital_server.py

# In a new terminal, start the client generator
python3 client/client_generator.py
```

Patients will be enqueued and treated by available doctors in order of urgency.

---

## 📊 Coming Soon

- 🌐 **HTTP Dashboard (Flask/FastAPI)** to visualize triage queue and doctor workload
- 🧾 Logging system for audit and analysis
- 🐳 Docker support with `docker-compose` to run both server and client in containers

---

## 📂 Project Layout

```
hospital-emergency-simulation/
├── server/
│   ├── hospital_server.py   # TCP server entry point
│   ├── doctor.py            # Doctor threads
│   ├── triage.py            # Triage queue management
│   ├── patient.py           # Patient class
│   └── state.py             # Shared shared memory and constants
├── client/
│   └── client_generator.py  # Simulates patient arrivals
├── dashboard/ (coming soon)
│   └── app.py               # HTTP server
└── README.md
```

---

## 📚 References

- "Operating System Concepts" – Silberschatz, Galvin, Gagne
- Python Docs – `threading`, `socket`, `multiprocessing`

---

## 🧑‍💻 Author & Maintainer

Made with ❤️ and _a lot_ of coffee by **Pedro Peyroteo** for **SO** class - **EIA** - **ESTGA 2024/2025**.

---

> 💡 Ready to expand! This system is built to scale, modularize, and impress — whether in a classroom, a demo, or a Docker container.
