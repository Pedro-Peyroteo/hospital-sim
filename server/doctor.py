import time
import random
from .state import triage_queue

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