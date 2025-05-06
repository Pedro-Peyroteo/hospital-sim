import socket
import threading
import json
import time
import re
from .patient import Patient
from .dashboard_handler import broadcast_to_dashboards
from .triage import add_to_queue
from .doctor import doctor_worker
from .state import triage_queue

HOST = '0.0.0.0'
PORT = 5000
MAX_DOCTORS = 5

def parse_patient_message(message: str) -> dict:
    '''
        This regex safely extracts key:value pairs from the patient message.
        It handles values with spaces (like names and addresses).

        Example: "Name:John Doe Address:123 Elm Street"
        -> {'Name': 'John Doe', 'Address': '123 Elm Street'}

        Breakdown:
        - (\w+)         -> captures the key (word characters before ':')
        - :             -> matches the colon separator
        - ([^:]+?)      -> captures the value (non-greedy, until the next key or end)
        - (?=\s+\w+:|$) -> lookahead for next key or end of string (doesn't consume characters, just checks where to stop matching the value)
    '''
    pattern = r'(\w+):([^:]+?)(?=\s+\w+:|$)'
    return dict(re.findall(pattern, message))
    
def handle_patient(conn, addr):
    try:
        # Gets data from connection.
        data = conn.recv(1024).decode('utf-8')
        
        # Checks if connection as data. 
        if data:
            print(f"[Hospital] Received from {addr}: {data}") 
            
            parts = parse_patient_message(data)
            
            patient = Patient(
                pid=parts["PatientID"],
                name=parts.get("Name"),
                age=int(parts.get("Age", 0)),
                gender=parts.get("Gender"),
                address=parts.get("Address"),
                blood_type=parts.get("BloodType"),
                insurance=parts.get("insurance"),
                language=parts.get("Language"),
                symptoms=parts.get("Symptoms", "").split(","),
                urgency=None  # Triage will assign this field.
            )
            
            add_to_queue(patient)
            
            conn.sendall("ACK from Hospital".encode('utf-8'))
            broadcast_to_dashboards(json.dumps({
                "type": "patient_queued",
                "timestamp": time.time(),
                "payload": {
                    "patient_id": patient.pid,
                    "urgency": patient.urgency,
                    "name": patient.name,
                    "age": patient.age,
                    "symptoms": patient.symptoms
                }
            }))
                    
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()

def hospital_server():
    # Starts doctor workers.
    print("[Hospital Server] Starting doctor threads...")
    for i in range(MAX_DOCTORS):
        t = threading.Thread(target=doctor_worker, args=(i + 1,), daemon=True) # Initializes worker thread as an object.
        t.start() # Starts worker thread
    
    # Start TCP server.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[Hospital Server] Listening on {HOST}:{PORT}")
    
    # Listens and awaits a connection.
    while True:
        conn, addr = server_socket.accept() # Accepts connection request.

        # 'daemon=True' - Marks the thread as "background", when main program exits, so will these.
        thread = threading.Thread(
            target=handle_patient,
            args=(conn, addr),
            daemon=True,
            name=f"patient_thread_{addr[1]}"
        )
        
        thread.start()