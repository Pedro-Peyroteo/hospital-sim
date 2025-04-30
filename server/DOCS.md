# TCP Server & Threads: Main Concepts Breakdown

This document explains the main concepts used in the multithreaded TCP-based hospital server, with a focus on networking (`socket`) and concurrency (`threading`).

---

## 🔌 Socket: The Networking Layer

### Code Example:

```python
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
conn, addr = server_socket.accept()
data = conn.recv(1024).decode('utf-8')
conn.sendall("ACK".encode('utf-8'))
conn.close()
```

### Breakdown:

| Line          | Purpose                             |
| ------------- | ----------------------------------- |
| `AF_INET`     | Use IPv4 (e.g., 127.0.0.1)          |
| `SOCK_STREAM` | Use TCP (reliable, ordered stream)  |
| `bind()`      | Bind to specific IP and port        |
| `listen()`    | Put the socket into listening mode  |
| `accept()`    | Accept a client connection (blocks) |
| `recv()`      | Receive data from the client        |
| `sendall()`   | Send data back to the client        |
| `close()`     | Close the connection                |

---

## 🧵 Threading: The Concurrency Layer

### Code Example:

```python
threading.Thread(target=handle_patient, args=(conn, addr), daemon=True).start()
```

### Purpose:

- Allows the server to handle **multiple patients simultaneously**.
- Each client is handled in **its own thread**, so one doesn't block others.

### Doctor Simulation:

```python
threading.Thread(target=doctor_worker, args=(doctor_id,), daemon=True).start()
```

- Background doctor threads pick patients from the triage queue and simulate treatment.

---

## 🧠 Visual Breakdown

```
[ TCP Socket Server ]
       |
       |---> [ Thread: handle_patient() for client 1 ]
       |---> [ Thread: handle_patient() for client 2 ]
       |---> [ Thread: handle_patient() for client 3 ]
       |
       |---> [ Thread: doctor_worker() for Doctor 1 ]
       |---> [ Thread: doctor_worker() for Doctor 2 ]
       |---> [ Thread: doctor_worker() for Doctor 3 ]
       |---> [ Thread: doctor_worker() for Doctor 4 ]
       |---> [ Thread: doctor_worker() for Doctor 5 ]
```

---

## ✅ Why Threads?

| Benefit      | Description                                              |
| ------------ | -------------------------------------------------------- |
| Non-blocking | Clients connect independently, no waiting on each other  |
| Scalable     | Easily supports many simultaneous patients               |
| Parallelism  | Doctors treat patients while new ones are still arriving |
| Simplicity   | Easier than multiprocessing for socket servers           |

---

## 🔜 Next Concepts

- Managing shared state (e.g., total treated count)
- Timeout handling for patient wait time
- Logging patient lifecycle to file
- Containerizing the system with Docker
