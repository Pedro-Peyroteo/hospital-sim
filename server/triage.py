import time
import json
import threading

from .symptom_severity import RED_SYMPTOMS, YELLOW_SYMPTOMS
from .patient import Patient
from .state import triage_queue, waiting_patients, MAX_QUEUE_SIZE, MAX_WAIT_TIME
from .dashboard_handler import broadcast_to_dashboards

def evaluate_patient(patient: Patient):
    # Creates a patient set() to be iterated and compared.
    symptoms_set = set(patient.symptoms)
    
    # Checks if the patient's symptoms intersect with any RED symptoms, assign RED urgency.
    if symptoms_set & set(RED_SYMPTOMS):
        patient.urgency = "RED"
    elif symptoms_set & set(YELLOW_SYMPTOMS):
        patient.urgency = "YELLOW"
    else:
        patient.urgency = "GREEN"
       
    # Dictionary-based mapping that assigns a numeric priority value based on the patient's urgency level.
    patient.priority = {"RED": 1, "YELLOW": 2, "GREEN": 3}[patient.urgency]
    
    
    
def timeout_monitor(patient: Patient):    
    time.sleep(MAX_WAIT_TIME)
    
    if patient.pid in waiting_patients:
        print(f"[Timeout] Patient {patient.pid} timed out and left.")
        waiting_patients.pop(patient.pid, None) 
        
    # Try to remove from triage_queue if still present.
    try:
        with triage_queue.mutex:
            triage_queue.queue = [p for p in triage_queue.queue if p.pid != patient.id]
    except Exception:
        pass
        
    broadcast_to_dashboards(json.dumps({
        "type": "patient_timeout",
        "timestamp": time.time(),
        "payload": {
            "patient_id": patient.pid,
            "name": patient.name,
            "urgency": patient.urgency
        }
    }))

def add_to_queue(patient: Patient):
    evaluate_patient(patient) 
    
    if triage_queue.qsize() >= MAX_QUEUE_SIZE:
        print(f"[Triage] Queue full. Patient {patient.pid} rejected.")
        return False
    
    triage_queue.put(patient) # Adds evaluated patient to the triage queue
    waiting_patients[patient.pid] = patient
    print(f"[Triage] Patient {patient.pid} {patient.name} ({patient.urgency}) added to queue.")
    
    threading.Thread(target=timeout_monitor, args=(patient,), daemon=True).start()
    
    return True