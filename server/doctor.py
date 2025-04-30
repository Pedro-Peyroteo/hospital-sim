import json
import time
import random
from .state import triage_queue
from .dashboard_handler import broadcast_to_dashboards

def doctor_worker(doctor_id):
    while True:
        if not triage_queue.empty():
            patient = triage_queue.get()
            
            print(f"[DOCTOR {doctor_id}] Treating patient {patient.pid} ({patient.urgency})...")
            broadcast_to_dashboards(json.dumps({
                "type": "patient_in_treatment",
                "timestamp": time.time(),
                "payload": {
                    "doctor_id": doctor_id,
                    "patient_id": patient.pid,
                    "urgency": patient.urgency
                }
            }))
            
            treatment_time = random.randint(2,5)
            time.sleep(treatment_time)
            
            print(f"[Doctor {doctor_id}] Finished patient {patient.pid} after {treatment_time}s.")
            broadcast_to_dashboards(json.dumps({
                "type": "patient_treated",
                "timestamp": time.time(),
                "payload": {
                    "doctor_id": doctor_id,
                    "patient_id": patient.pid,
                    "urgency": patient.urgency,
                    "duration": treatment_time
                }
            }))
        else:
            time.sleep(1)