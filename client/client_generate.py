import socket
import random
import time

HOST = 'localhost'
PORT = 5000

urgency_levels = ["RED", "YELLOW", "GREEN"]

def send_patient(pid):
    urgency = random.choice(urgency_levels)
    patient_data = f"PatientID:{pid} urgency:{urgency}"
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(patient_data.encode('utf-8'))
        
        ack = s.recv(1024).decode('utf-8')
        print(f"[Client] Server acknowledgment: {ack}")
        
def client_generator():
    print("[Client] Generator started.")
    
    pid = 1
    
    while True:
        send_patient(pid)
        pid += 1
        time.sleep(random.uniform(0.5, 2))
        
if __name__ == "__main__":
    client_generator()