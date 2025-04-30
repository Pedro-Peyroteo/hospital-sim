import socket
import threading
from .patient import Patient
from .dashboard_handler import start_dashboard_listener, broadcast_to_dashboards
from .triage import add_to_queue
from .doctor import doctor_worker
from .state import triage_queue

# TODO: REFRACTOR ADD_TO_QUEUE

HOST = '0.0.0.0'
PORT = 5000
MAX_DOCTORS = 5
        
def handle_patient(conn, addr):
    try:
       # Gets data from connection.
        data = conn.recv(1024).decode('utf-8')
        
        # Checks if connection as data. 
        if data:
            print(f"[Hospital] Received from {addr}: {data}")
            
            # Parse patient info.
            parts = data.strip().split()
            pid = parts[0].split(":")[1]
            urgency = parts[1].split(":")[1]
            
            patient = Patient(pid, urgency)
            triage_queue.put(patient)
            
            conn.sendall("ACK from Hospital".encode('utf-8'))
            broadcast_to_dashboards(f"Patient {pid} queued ({urgency})")
            
            
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
        threading.Thread(target=handle_patient, args=(conn, addr), daemon=True).start() # Starts 

if __name__ == "__main__":
    start_dashboard_listener(host='0.0.0.0', port=5999)
    hospital_server()