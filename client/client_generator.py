import socket
import random
import time
import json

from patient_factory import generate_patient

HOST = 'hospital'
PORT = 5000

# Formats patient data into a structured string message.
# Message will be sent to hospital server containing all the patient's data.
def format_patient_data(patient: dict) -> str:
     return (
        f"PatientID:{patient['patient_id']} "
        f"Name:{patient['name']} "
        f"Age:{patient['age']} "
        f"Gender:{patient['gender']} "
        f"Address:{patient['address']} "
        f"BloodType:{patient['blood_type']} "
        f"insurance:{patient['insurance']} "
        f"Language:{patient['language']} "
        f"Symptoms:{patient['symptoms']}"  
    )

# Creates a new patient, processes data and sends to hospital socket connection.
def send_patient(pid):
    patient = generate_patient(pid)
    message = format_patient_data(patient)
    
    print(f"[Client] Sending: {message}")
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(message.encode('utf-8'))
        
        ack = s.recv(1024).decode('utf-8').strip()
        
        try:
            ack_data = json.loads(ack)
            status = ack_data.get("status")
            
            if status == "ACCEPTED":
                print(f"[ACK-Client] Accepted: ID={ack_data['patient_id']} Urgency={ack_data['urgency']}")
            elif status == "REJECTED":
                print(f"[ACK-Client] Rejected: ID={ack_data['patient_id']} Reason={ack_data['reason']}")
            else:
                print(f"[ACK-Client] Unknown response: {ack}")
        except Exception as e:
            print(f"[ERROR-Client] Failed to parse ACK: {ack} ({e})")

# Keeps generating and sending patients to the hospital within a set delta time.
def client_generator():
    print("[Client] Generator started.")
    print("[Client] Waiting for server to be ready...")
    time.sleep(5)  # Waits 5 seconds for the hospital server to start
    
    pid = 1
    
    while True:
        send_patient(pid)
        pid += 1
        time.sleep(random.uniform(1.5, 3))
        
if __name__ == "__main__":
    client_generator()