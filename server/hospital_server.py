import socket
import threading
import time
import queue
import random

HOST = '0.0.0.0'
PORT = 5000
MAX_DOCTORS = 5

urgency_priority = {"RED": 1, "YELLOW": 2, "GREEN":3}

triage_queue = queue.PriorityQueue()



class Patient:
    def __init__(self, pid, urgency):
        self.pid = pid
        self.urgency = urgency
        self.priority = urgency_priority.get(urgency.upper(), 3)
        
    def __lt__(self, other):
        return self.priority < other.priority
  # PriorityQueue uses this to sort



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
            
            print(f"[Triage] Patient {pid} with urgency {urgency} added to queue.")
            conn.sendall("ACK from Hospital".encode('utf-8'))
        
    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        conn.close()
        
        
def doctor_worker(doctor_id):
    while True:
        if not triage_queue.empty():
            patient = triage_queue.get()
            
            print(f"[DOCTOR {doctor_id}] Treating patient {patient.pid} ({patient.urgency})...")
            
            treatment_time = random.randint(2,5)
            time.sleep(treatment_time)
            
            print(f"[Doctor {doctor_id}] Finished patient {patient.pid} after {treatment_time}s.")
        else:
            time.sleep(1)


def hospital_server():
    # Starts doctor workers.
    for i in range(MAX_DOCTORS):
        t = threading.Thread(target=doctor_worker, args=(i+1,), daemon=True) # Initializes worker thread as an object.
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
    hospital_server()